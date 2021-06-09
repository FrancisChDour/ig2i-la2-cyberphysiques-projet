import pygame

pygame.init()

while 1:
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_z:
                print("z")
            if event.key == pygame.K_s:
                print("s")
            if event.key == pygame.K_q:
                print("q")
            if event.key == pygame.K_d:
                print("d")
            if event.key == pygame.K_a:
                print("a")