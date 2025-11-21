import time
import random

def connect_gpu(intensity: int = 1):
    try:
        import pygame
    except ImportError:
        return {
            "success": False,
            "msg": "pygame not installed"
        }

    # Clamp intensity
    intensity = max(1, min(intensity, 5))

    resolutions = [256, 512, 1024, 2048, 4096]
    num_of_shapes = [100, 1000, 5000, 10000, 50000]

    # resolution + shape count based on intensity
    res = resolutions[intensity - 1]
    shapes = num_of_shapes[intensity - 1]

    pygame.init()
    screen = pygame.display.set_mode((res, res))
    pygame.display.set_caption("GPU Detuner Pygame Render")

    clock = pygame.time.Clock()
    running = True

    frame_limit = 10   # number of frames to render

    frames = 0
    while running and frames < frame_limit:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Draw random circles
        for _ in range(shapes):
            pygame.draw.circle(
                screen,
                (
                    random.random() * 255,
                    random.random() * 255,
                    random.random() * 255
                ),
                (
                    random.random() * resolutions[intensity - 1],
                    random.random() * resolutions[intensity - 1]
                ),
                10
            )

        pygame.display.flip()
        clock.tick(60)
        frames += 1

    pygame.quit()

    return {
        "success": True,
        "msg": f"Pygame render complete at intensity {intensity}",
        "resolution": res,
        "shapes_drawn": shapes * frame_limit
    }
