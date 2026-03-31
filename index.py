import pygame

pygame.init()
pygame.display.set_caption("Tetris")

width, height = 10, 20
tam_celula = 45
tela = pygame.display.set_mode((width * tam_celula, height * tam_celula))
fps = pygame.time.Clock()

# Grade de fundo
grade = [pygame.Rect(x * tam_celula, y * tam_celula, tam_celula, tam_celula) for y in range(height) for x in range(width)]

# Matrizes das peças
figuras_coor = [
    [[1, 1, 1, 1]],           # I
    [[1, 1], [1, 1]],         # O
    [[0, 1, 0], [1, 1, 1]],   # T
    [[1, 0, 0], [1, 1, 1]],   # L
    [[0, 0, 1], [1, 1, 1]],   # J
    [[0, 1, 1], [1, 1, 0]],   # S
    [[1, 1, 0], [0, 1, 1]]    # Z
]

# Transformando matrizes em listas de Rects (Cálculo corrigido)
figuras = [[pygame.Rect(x + width // 2, y + 1, 1, 1) for y, row in enumerate(fig) for x, val in enumerate(row) if val] for fig in figuras_coor]

figuras_rect = pygame.Rect(0, 0, tam_celula - 2, tam_celula - 2)
figura = figuras[2]

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
    tela.fill("black")
    
    # Desenha a grade
    for rect in grade:
        pygame.draw.rect(tela, (40, 40, 40), rect, 1)
        
    # Desenha a peça atual
    for i in range(4):
        figuras_rect.x = figura[i].x * tam_celula + 1
        figuras_rect.y = figura[i].y * tam_celula + 1
        pygame.draw.rect(tela, "cyan", figuras_rect)
        
    pygame.display.flip()
    fps.tick(60)

pygame.quit()