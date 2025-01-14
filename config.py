# Configurações da janela
WIDTH, HEIGHT = 800, 600
NODE_RADIUS = 15

# Cores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (100, 149, 237)
RED = (220, 20, 60)
GRAY = (200, 200, 200)

import pygame
# Inicializa o Pygame
pygame.init()
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Visualizador de Grafos Interativo")
clock = pygame.time.Clock()