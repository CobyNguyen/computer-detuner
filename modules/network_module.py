"""Network module with optional universal latency control.

`connect_network(intensity)` is the UI entrypoint. It toggles a system-wide
per-user proxy that delays relayed packets by a mapped latency value.

This single-file approach keeps all control within `modules/network_module.py`.
Use only on machines you control. The code modifies HKCU Internet Settings
and restores them when stopped.
"""
from __future__ import annotations

import threading
import socket
import time
import sys
from typing import Optional

IS_WINDOWS = sys.platform.startswith("win") or sys.platform == "cygwin"

# Internal proxy state
_proxy_thread: Optional[threading.Thread] = None
_server_socket: Optional[socket.socket] = None
_running = False
_latency_ms = 0
_listen_port: Optional[int] = None
_winreg_backup = {}


def _relay(src: socket.socket, dst: socket.socket, latency_s: float):
	try:
		while True:
			data = src.recv(4096)
			if not data:
				break
			if latency_s > 0:
				time.sleep(latency_s)
			dst.sendall(data)
	except Exception:
		pass
	finally:
		try:
			dst.shutdown(socket.SHUT_RDWR)
		except Exception:
			pass


def _handle_client(client_sock: socket.socket, addr, latency_s: float):
	try:
		client_sock.settimeout(5.0)
		buf = b""
		while b"\r\n\r\n" not in buf and len(buf) < 65536:
			data = client_sock.recv(4096)
			if not data:
				break
			buf += data
	except Exception:
		buf = b""

	if not buf:
		client_sock.close()
		return

	first_line = buf.split(b"\r\n", 1)[0].decode(errors="ignore")
	parts = first_line.split()
	if len(parts) >= 1 and parts[0].upper() == 'CONNECT' and len(parts) >= 2:
		target = parts[1]
		host, _, port_s = target.partition(":")
		port = int(port_s) if port_s else 443
		remote = None
		try:
			remote = socket.create_connection((host, port), timeout=5)
			client_sock.sendall(b"HTTP/1.1 200 Connection established\r\n\r\n")
			t1 = threading.Thread(target=_relay, args=(client_sock, remote, latency_s), daemon=True)
			t2 = threading.Thread(target=_relay, args=(remote, client_sock, latency_s), daemon=True)
			t1.start(); t2.start()
			t1.join(); t2.join()
		except Exception:
			pass
		finally:
			try:
				if remote:
					remote.close()
			except Exception:
				pass
			try:
				client_sock.close()
			except Exception:
				pass
		return

	headers = buf.decode(errors="ignore")
	host = None
	port = 80
	for line in headers.split('\r\n'):
		if line.lower().startswith('host:'):
			hostport = line.split(':', 1)[1].strip()
			if ':' in hostport:
				host, port = hostport.split(':', 1)
				port = int(port)
			else:
				host = hostport
			break

	if not host:
		client_sock.close()
		return

	remote = None
	try:
		remote = socket.create_connection((host, port), timeout=5)
		if latency_s > 0:
			time.sleep(latency_s)
		remote.sendall(buf)
		t1 = threading.Thread(target=_relay, args=(client_sock, remote, latency_s), daemon=True)
		t2 = threading.Thread(target=_relay, args=(remote, client_sock, latency_s), daemon=True)
		t1.start(); t2.start()
		t1.join(); t2.join()
	except Exception:
		pass
	finally:
		try:
			if remote:
				remote.close()
		except Exception:
			pass
		try:
			client_sock.close()
		except Exception:
			pass


def _proxy_loop(listen_host: str, listen_port: int, latency_ms: int):
	global _server_socket, _running
	latency_s = latency_ms / 1000.0
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	sock.bind((listen_host, listen_port))
	sock.listen(128)
	_server_socket = sock
	_running = True
	try:
		while _running:
			try:
				client, addr = sock.accept()
				t = threading.Thread(target=_handle_client, args=(client, addr, latency_s), daemon=True)
				t.start()
			except Exception:
				continue
	finally:
		try:
			sock.close()
		except Exception:
			pass


def _set_windows_proxy(port: int):
	import winreg
	global _winreg_backup
	key_path = r"Software\Microsoft\Windows\CurrentVersion\Internet Settings"
	with winreg.OpenKey(winreg.HKEY_CURRENT_USER, key_path, 0, winreg.KEY_READ) as k:
		try:
			prev_enable, _ = winreg.QueryValueEx(k, 'ProxyEnable')
		except FileNotFoundError:
			prev_enable = 0
		try:
			prev_server, _ = winreg.QueryValueEx(k, 'ProxyServer')
		except FileNotFoundError:
			prev_server = ''
		try:
			prev_override, _ = winreg.QueryValueEx(k, 'ProxyOverride')
		except FileNotFoundError:
			prev_override = ''
	_winreg_backup['ProxyEnable'] = prev_enable
	_winreg_backup['ProxyServer'] = prev_server
	_winreg_backup['ProxyOverride'] = prev_override

	with winreg.OpenKey(winreg.HKEY_CURRENT_USER, key_path, 0, winreg.KEY_SET_VALUE) as k:
		winreg.SetValueEx(k, 'ProxyEnable', 0, winreg.REG_DWORD, 1)
		winreg.SetValueEx(k, 'ProxyServer', 0, winreg.REG_SZ, f'127.0.0.1:{port}')
		winreg.SetValueEx(k, 'ProxyOverride', 0, winreg.REG_SZ, '')
	try:
		import ctypes
		INTERNET_OPTION_SETTINGS_CHANGED = 39
		INTERNET_OPTION_REFRESH = 37
		ctypes.windll.wininet.InternetSetOptionW(0, INTERNET_OPTION_SETTINGS_CHANGED, 0, 0)
		ctypes.windll.wininet.InternetSetOptionW(0, INTERNET_OPTION_REFRESH, 0, 0)
	except Exception:
		pass


def _restore_windows_proxy():
	import winreg
	global _winreg_backup
	key_path = r"Software\Microsoft\Windows\CurrentVersion\Internet Settings"
	with winreg.OpenKey(winreg.HKEY_CURRENT_USER, key_path, 0, winreg.KEY_SET_VALUE) as k:
		try:
			winreg.SetValueEx(k, 'ProxyEnable', 0, winreg.REG_DWORD, int(_winreg_backup.get('ProxyEnable', 0)))
		except Exception:
			pass
		try:
			winreg.SetValueEx(k, 'ProxyServer', 0, winreg.REG_SZ, _winreg_backup.get('ProxyServer', ''))
		except Exception:
			pass
		try:
			winreg.SetValueEx(k, 'ProxyOverride', 0, winreg.REG_SZ, _winreg_backup.get('ProxyOverride', ''))
		except Exception:
			pass
	try:
		import ctypes
		INTERNET_OPTION_SETTINGS_CHANGED = 39
		INTERNET_OPTION_REFRESH = 37
		ctypes.windll.wininet.InternetSetOptionW(0, INTERNET_OPTION_SETTINGS_CHANGED, 0, 0)
		ctypes.windll.wininet.InternetSetOptionW(0, INTERNET_OPTION_REFRESH, 0, 0)
	except Exception:
		pass


def start_universal_latency(latency_ms: int = 300, listen_host: str = '127.0.0.1', listen_port: int = 0):
	global _proxy_thread, _running, _latency_ms, _listen_port
	if not IS_WINDOWS:
		raise RuntimeError('start_universal_latency is currently supported only on Windows')
	if _running:
		raise RuntimeError('Universal latency proxy is already running')

	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.bind((listen_host, listen_port))
	addr, port = s.getsockname()
	s.close()

	_latency_ms = int(latency_ms)
	_listen_port = port
	_running = True
	_proxy_thread = threading.Thread(target=_proxy_loop, args=(listen_host, port, _latency_ms), daemon=True)
	_proxy_thread.start()
	time.sleep(0.1)
	_set_windows_proxy(port)
	return port


def stop_universal_latency():
	global _running, _server_socket, _proxy_thread, _listen_port
	if not IS_WINDOWS:
		raise RuntimeError('stop_universal_latency is currently supported only on Windows')
	if not _running and _server_socket is None:
		try:
			_restore_windows_proxy()
		except Exception:
			pass
		return

	_running = False
	try:
		if _server_socket:
			_server_socket.close()
	except Exception:
		pass

	try:
		_restore_windows_proxy()
	except Exception:
		pass

	_proxy_thread = None
	_server_socket = None
	_listen_port = None


def status() -> dict:
	return {
		'running': bool(_running),
		'latency_ms': _latency_ms,
		'listen_port': _listen_port,
	}


def connect_network(intensity: int = 3):
	"""UI entrypoint: toggle universal latency using intensity mapping.

	If the proxy is stopped, start it with a latency mapped from intensity.
	If running, stop it.
	"""
	try:
		mapping = {1: 100, 2: 200, 3: 400, 4: 800, 5: 1200}
		latency = mapping.get(max(1, min(5, int(intensity))), 400)

		if status().get('running'):
			stop_universal_latency()
			return {"success": True, "message": "Universal latency stopped"}
		else:
			port = start_universal_latency(latency)
			return {"success": True, "message": f"Universal latency {latency}ms started on port {port}"}
	except Exception as e:
		return {"success": False, "message": str(e)}
