import pygame
import random
import networkx as nx
import math

class RandomWalker:
    def __init__(self, graph, screen, node_positions, delay=500):
        self.graph = graph
        self.screen = screen
        self.node_positions = node_positions
        self.current_node = random.choice(list(graph.nodes()))
        self.delay = delay
        self.last_move_time = pygame.time.get_ticks()

    def reset(self):
        """Reinicia o passeio aleatório"""
        self.current_node = random.choice(list(self.graph.nodes()))
        self.last_move_time = pygame.time.get_ticks()

    def avancar(self):
        """Avança manualmente para o próximo nó"""
        self.step()

    def step(self):
        neighbors = list(self.graph.successors(self.current_node))
        if not neighbors:
            return
        weights = [self.graph[self.current_node][nbr]['weight'] for nbr in neighbors]
        total = sum(weights)
        probs = [w / total for w in weights]
        self.current_node = random.choices(neighbors, probs)[0]

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_move_time > self.delay:
            self.step()
            self.last_move_time = now

    def draw(self):
        pos = self.node_positions[self.current_node]
        pygame.draw.circle(self.screen, (255, 0, 0), pos, 10)

# Funções auxiliares mantidas
def layout_positions(n, width=800, height=600):
    positions = {}
    radius = min(width, height) // 2.5
    center = (width // 2, height // 2)
    for i in range(n):
        angle = 2 * 3.1416 * i / n
        x = int(center[0] + radius * pygame.math.Vector2(1, 0).rotate_rad(angle).x)
        y = int(center[1] + radius * pygame.math.Vector2(1, 0).rotate_rad(angle).y)
        positions[i] = (x, y)
    return positions

def draw_graph(screen, G, positions):
    screen.fill((30, 30, 30))  # Fundo preto
    font = pygame.font.SysFont('Arial', 16)  # Fonte menor para pesos
    
    # Primeiro desenha todas as arestas
    for u, v, data in G.edges(data=True):
        start_pos = positions[u]
        end_pos = positions[v]
        
        # Desenha a linha da aresta
        pygame.draw.line(screen, (100, 100, 255), start_pos, end_pos, 2)
        
        # Calcula posição do texto do peso
        text_pos = calcular_posicao_texto(start_pos, end_pos)
        
        # Renderiza o texto com fundo para melhor legibilidade
        peso_texto = f"{data['weight']:.2f}"
        renderizar_texto_com_fundo(screen, font, peso_texto, text_pos, (255, 255, 255), (0, 0, 0, 128))
    
    # Depois desenha todos os nós por cima
    for node, pos in positions.items():
        pygame.draw.circle(screen, (200, 200, 200), pos, 20)
        node_font = pygame.font.SysFont('Arial', 24)  # Fonte maior para nós
        label = node_font.render(str(node), True, (0, 0, 0))
        screen.blit(label, (pos[0]-10, pos[1]-10))

def calcular_posicao_texto(start_pos, end_pos):
    """Calcula a posição do texto ao longo da aresta"""
    mx = (start_pos[0] + end_pos[0]) / 2
    my = (start_pos[1] + end_pos[1]) / 2
    
    # Vetor perpendicular à aresta
    dx = end_pos[0] - start_pos[0]
    dy = end_pos[1] - start_pos[1]
    length = max(1, math.hypot(dx, dy))  # Evita divisão por zero
    
    # Deslocamento perpendicular
    offset_x = (-dy / length) * 20
    offset_y = (dx / length) * 20
    
    return (int(mx + offset_x), int(my + offset_y))

def renderizar_texto_com_fundo(screen, font, texto, pos, cor_texto, cor_fundo):
    """Renderiza texto com fundo semi-transparente"""
    text_surface = font.render(texto, True, cor_texto)
    text_rect = text_surface.get_rect(center=pos)
    
    # Cria superfície para o fundo
    bg_surface = pygame.Surface((text_rect.width + 4, text_rect.height + 4), pygame.SRCALPHA)
    bg_surface.fill(cor_fundo)
    
    # Desenha fundo e depois texto
    screen.blit(bg_surface, (text_rect.x - 2, text_rect.y - 2))
    screen.blit(text_surface, text_rect)