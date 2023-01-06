import time

import pygame
from world import *
from Render_Settings import *

if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((500, 500))


    world = World()
    world.Generate_world(Size=(200,200), Seed=434)

    Camera = Player_Camera(world, Rotation=45)
    Camera.x = 180
    Camera.z = 50
    start = time.perf_counter()

    Camera.Render(screen)

    end = time.perf_counter()
    print("Render Took:", round((end - start) * 1000), "ms")

    font = pygame.font.Font('freesansbold.ttf', 32)
    clock = pygame.time.Clock()

    Running = True
    while Running:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                Running = False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            Camera.Move_Forward(2)
        if keys[pygame.K_s]:
            Camera.Move_Forward(-2)
        if keys[pygame.K_a]:
            Camera.Rotation += -2
        if keys[pygame.K_d]:
            Camera.Rotation += 2

        Camera.Render(screen, UpdateScreen=False)

        if Display_FPS == True:
            text = font.render(str(round(clock.get_fps())) + ' FPS', True, (255, 255, 255))
            textRect = text.get_rect()
            screen.blit(text, textRect)

        pygame.display.flip()