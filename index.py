import pygame
import random

pygame.init()
pygame.display.set_caption("Tetris")
def mover(figura, dx, dy, width, height, fig_usadas):
    for bloco in figura:
        novo_x = bloco.x + dx
        novo_y = bloco.y + dy
        if novo_x < 0 or novo_x >= width or novo_y >= height:
            return False
        for bloco_usado in fig_usadas:
            if novo_x == bloco_usado.x and novo_y == bloco_usado.y:
                return False
    return True

def limpar_linhas(fig_usadas, height):
    linhas_completas = []
    for y in range(height):
        count = sum(1 for bloco in fig_usadas if bloco.y == y)
        if count == 10:
            linhas_completas.append(y)
    
    for linha in linhas_completas:
        fig_usadas[:] = [bloco for bloco in fig_usadas if bloco.y != linha]
        for bloco in fig_usadas:
            if bloco.y < linha:
                bloco.y += 1

def scoreboard(tela, pontos):
    text = fonte.render(f"Score: {pontos}", True, "white")
    tela.blit(text, (500, 700))

fonte= pygame.font.SysFont(None, size=36, bold=True)
barra_lateral = 200
width, height = 10, 20
tam_celula = 45
tela = pygame.display.set_mode(((width * tam_celula) + barra_lateral, height * tam_celula))
fps = pygame.time.Clock()
velocidade = pygame.USEREVENT + 1
pygame.time.set_timer(velocidade, 500)

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

# Transformando matrizes em listas de Rects
def nova_figura():
    modelo = random.choice(figuras_coor)
    largura_fig = len(modelo[0])
    off_x = (width // 2) - (largura_fig // 2)
    return [pygame.Rect(x + off_x, y, 1, 1) for y, row in enumerate(modelo) for x, val in enumerate(row) if val]

figura = nova_figura()
fig_usadas = []
running = True
pontos = 0

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        #Queda automática
        elif event.type == velocidade:
            if mover(figura, 0, 1, width, height, fig_usadas):
                for bloco in figura:
                    bloco.y += 1
            else:
                # Salva blocos atuais nos usados
                for bloco in figura:
                    fig_usadas.append(pygame.Rect(bloco.x, bloco.y, 1, 1))
                
                # Gera nova peça
                figura = nova_figura()
                
                # Checa Game Over
                if not mover(figura, 0, 0, width, height, fig_usadas):
                    print("Game Over")
                    running = False

        # Controles do jogador
        if event.type == pygame.KEYDOWN:
            # Movimento para a esquerda
            if event.key == pygame.K_LEFT:
                if mover(figura, -1, 0, width, height, fig_usadas):
                    for bloco in figura: bloco.x -= 1

            # Movimento para a direita
            if event.key == pygame.K_RIGHT:
                if mover(figura, 1, 0, width, height, fig_usadas):
                    for bloco in figura: bloco.x += 1

            #Movimento para baixo
            if event.key == pygame.K_DOWN:
                if mover(figura, 0, 1, width, height, fig_usadas):
                    for bloco in figura: bloco.y += 1

            # Rotacionar peça
            if event.key == pygame.K_UP:
                modelo = [[bloco.x - figura[0].x, bloco.y - figura[0].y] for bloco in figura]
                rotacionado = [pygame.Rect(-y + figura[0].x, x + figura[0].y, 1, 1) for x, y in modelo]
                if all(0 <= bloco.x < width and 0 <= bloco.y < height and all(bloco.x != usado.x or bloco.y != usado.y for usado in fig_usadas) for bloco in rotacionado):
                    figura = rotacionado
    tela.fill("black")
    scoreboard(tela, pontos)
    # Desenho da Grade
    for rect in grade:
        pygame.draw.rect(tela, (40, 40, 40), rect, 1)
        
    # Desenho da Peça Atual
    for bloco in figura:
        rect = pygame.Rect(bloco.x * tam_celula + 1, bloco.y * tam_celula + 1, tam_celula - 2, tam_celula - 2)
        pygame.draw.rect(tela, "cyan", rect)

    # Desenho dos Blocos Parados
    for bloco in fig_usadas:
        rect = pygame.Rect(bloco.x * tam_celula + 1, bloco.y * tam_celula + 1, tam_celula - 2, tam_celula - 2)
        pygame.draw.rect(tela, "gray", rect)

    limpar_linhas(fig_usadas, height)
    pygame.display.flip()
    fps.tick(60)

pygame.quit()