"""Network module implementation (placeholder).

Expose `connect_network(intensity:int) -> dict` for the UI to call.
"""
import time


def connect_network(intensity: int = 50):
	delay = 0.4 + (intensity / 100.0) * 1.0
	time.sleep(min(delay, 5.0))
	return {"success": True, "message": f"Network ready (intensity {intensity})"}
