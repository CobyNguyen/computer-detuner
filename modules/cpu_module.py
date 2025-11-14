"""CPU module implementation (placeholder).

Replace the internals with the real CPU-detuning implementation later.
This module exposes `connect_cpu(intensity:int) -> dict` so the UI can call it.
"""
import time


def connect_cpu(intensity: int = 5):
    """Simulate connecting to or initializing CPU detuner.

    Returns a dict with `success` and `message` keys so the UI can display status.
    """
    # Simulate some work proportional to intensity (bounded)
    delay = 0.4 + (intensity / 100.0) * 1.5
    time.sleep(min(delay, 5.0))
    return {"success": True, "message": f"CPU ready (intensity {intensity})"}