"""GPU module implementation (placeholder).

Expose `connect_gpu(intensity:int) -> dict` for the UI to call.
"""
import time


def connect_gpu(intensity: int = 50):
	delay = 0.4 + (intensity / 100.0) * 1.2
	time.sleep(min(delay, 5.0))
	return {"success": True, "message": f"GPU ready (intensity {intensity})"}
