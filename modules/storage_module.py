"""Storage module implementation (placeholder).

Expose `connect_storage(intensity:int) -> dict` for the UI to call.
"""
import time


def connect_storage(intensity: int = 5):
	delay = 0.4 + (intensity / 100.0) * 0.8
	time.sleep(min(delay, 5.0))
	return {"success": True, "message": f"Storage ready (intensity {intensity})"}
