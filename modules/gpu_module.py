import time

def connect_gpu(intensity: int = 1):
# Import here so Pylance doesn't freak out at file-level
try:
import pygame
except ImportError:
return {
"success": False,
"msg": "pygame is not installed"
}

# Clamp intensity
intensity = max(1, min(intensity, 5))

# Initialize pygame safely inside the function
pygame.init()

# Open a tiny window (low GPU load)
screen = pygame.display.set_mode((200, 200))
pygame.display.set_caption("GPU Detuner (Pygame)")

width, height = 200, 200
pixel_ops = intensity * 400 # safe GPU work

# Draw random pixels
for _ in range(pixel_ops):
x = pygame.math.randint(0, width-1)
y = pygame.math.randint(0, height-1)
color = (pygame.math.randint(0,255),
pygame.math.randint(0,255),
pygame.math.randint(0,255))
screen.set_at((x, y), color)

pygame.display.flip()

# Simulated GPU load delay
time.sleep(0.1 * intensity)

# No globals, no leaks
pygame.quit()

return {
"success": True,
"msg": f"Pygame GPU render at intensity {intensity}",
"pixels_drawn": pixel_ops
}
