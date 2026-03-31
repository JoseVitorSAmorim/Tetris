import pygame

pygame.init()
tela = pygame.display.set_mode((720, 1280))
fps = pygame.time.Clock()
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    tela.fill("black")

    pygame.display.flip()

    fps.tick(60)

pygame.quit()