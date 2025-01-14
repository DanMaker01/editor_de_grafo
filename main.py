import pygame
import networkx as nx

# Configurações da janela
WIDTH, HEIGHT = 800, 600
NODE_RADIUS = 15

# Cores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (100, 149, 237)
RED = (220, 20, 60)
GRAY = (200, 200, 200)

# Inicializa o Pygame
pygame.init()
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Visualizador de Grafos Interativo")
clock = pygame.time.Clock()

def draw_hud(graph):
    """Desenha o HUD com informações sobre o grafo."""
    font = pygame.font.SysFont(None, 24)
    vertices_text = f"Vértices: {graph.number_of_nodes()}"
    edges_text = f"Arestas: {graph.number_of_edges()}"

    vertices_surface = font.render(vertices_text, True, BLACK)
    edges_surface = font.render(edges_text, True, BLACK)

    window.blit(vertices_surface, (10, 10))
    window.blit(edges_surface, (10, 40))

class InteractiveGraph:
    def __init__(self):
        self.graph = nx.DiGraph()
        self.positions = {}
        self.selected_node = None

    def add_node(self, node, position):
        self.graph.add_node(node)
        self.positions[node] = position

    def add_edge(self, parent, child):
        self.graph.add_edge(parent, child)

    def remove_node(self, node):
        if node in self.graph:
            self.graph.remove_node(node)
            self.positions.pop(node, None)

    def draw(self):
        """Desenha o grafo na tela."""
        window.fill(WHITE)

        # Desenha as arestas
        for edge in self.graph.edges():
            pygame.draw.line(window, BLACK, self.positions[edge[0]], self.positions[edge[1]], 2)

        # Desenha os nós e números
        for node, pos in self.positions.items():
            color = RED if node == self.selected_node else BLUE
            pygame.draw.circle(window, color, pos, NODE_RADIUS)

            # Desenha o número do vértice ao lado do nó
            font = pygame.font.SysFont(None, 24)
            text = font.render(str(node), True, BLACK)
            window.blit(text, (pos[0] + NODE_RADIUS + 5, pos[1] - NODE_RADIUS))

        # Desenha o botão
        pygame.draw.rect(window, GRAY, (WIDTH - 110, HEIGHT - 60, 100, 40))
        font = pygame.font.SysFont(None, 24)
        text = font.render("Reorganizar", True, BLACK)
        window.blit(text, (WIDTH - 100, HEIGHT - 50))

        pygame.display.flip()

    def get_node_at_position(self, pos):
        """Retorna o nó na posição do mouse (se houver)."""
        for node, node_pos in self.positions.items():
            dx, dy = pos[0] - node_pos[0], pos[1] - node_pos[1]
            distance = (dx**2 + dy**2)**0.5
            if distance <= NODE_RADIUS:
                return node
        return None

    def print_tree_in_order(self, node=None, depth=0):
        """Printa a árvore em ordem (DFS)."""
        if node is None:
            # Encontra o nó raiz (sem pais)
            roots = [n for n in self.graph.nodes() if self.graph.in_degree(n) == 0]
            if not roots:
                return
            node = roots[0]

        print("  " * depth + str(node))
        for child in self.graph.successors(node):
            self.print_tree_in_order(child, depth + 1)

    def measure_distance(self, node1, node2):
        """Calcula a distância euclidiana entre dois nós."""
        if node1 in self.positions and node2 in self.positions:
            x1, y1 = self.positions[node1]
            x2, y2 = self.positions[node2]
            return ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5
        return None

    def reposition_nodes(self):
        """Modifica a posição de todos os nós para evitar sobreposição."""
        nodes = list(self.positions.keys())
        for i, node1 in enumerate(nodes):
            for node2 in nodes[i + 1:]:
                x1, y1 = self.positions[node1]
                x2, y2 = self.positions[node2]
                distance = ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5
                if distance < 2 * NODE_RADIUS:
                    # Ajusta as posições para afastar os nós
                    dx, dy = x2 - x1, y2 - y1
                    if dx == 0 and dy == 0:
                        dx, dy = 1, 1
                    norm = (dx**2 + dy**2)**0.5
                    dx, dy = dx / norm, dy / norm
                    self.positions[node2] = (x2 + dx * NODE_RADIUS, y2 + dy * NODE_RADIUS)

    def get_overlapping_nodes(self):
        """Retorna uma lista de pares de nós que estão se sobrepondo."""
        overlapping_nodes = []
        nodes = list(self.positions.keys())
        for i, node1 in enumerate(nodes):
            for node2 in nodes[i + 1:]:
                x1, y1 = self.positions[node1]
                x2, y2 = self.positions[node2]
                distance = ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5
                if distance < 2 * NODE_RADIUS:
                    overlapping_nodes.append((node1, node2))
        return overlapping_nodes

    def are_edges_overlapping(self, edge1, edge2, positions):
        """Verifica se duas arestas se sobrepõem (se aproximam o suficiente)."""
        # Obter as posições dos nós das arestas
        (x1, y1), (x2, y2) = positions[edge1[0]], positions[edge1[1]]
        (x3, y3), (x4, y4) = positions[edge2[0]], positions[edge2[1]]

        # Função para calcular a orientação de 3 pontos
        def orientation(px, py, qx, qy, rx, ry):
            val = (qy - py) * (rx - qx) - (qx - px) * (ry - qy)
            if val == 0:
                return 0  # Colinear
            elif val > 0:
                return 1  # Horário
            else:
                return 2  # Antihorário

        # Função para verificar se um ponto está no segmento de reta
        def on_segment(px, py, qx, qy, rx, ry):
            return min(px, qx) <= rx <= max(px, qx) and min(py, qy) <= ry <= max(py, qy)

        # Calcula as orientações dos quatro pares de pontos
        o1 = orientation(x1, y1, x2, y2, x3, y3)
        o2 = orientation(x1, y1, x2, y2, x4, y4)
        o3 = orientation(x3, y3, x4, y4, x1, y1)
        o4 = orientation(x3, y3, x4, y4, x2, y2)

        # Se as arestas se intersectam
        if o1 != o2 and o3 != o4:
            return True

        # Casos especiais (colineares)
        if o1 == 0 and on_segment(x1, y1, x2, y2, x3, y3):
            return True
        if o2 == 0 and on_segment(x1, y1, x2, y2, x4, y4):
            return True
        if o3 == 0 and on_segment(x3, y3, x4, y4, x1, y1):
            return True
        if o4 == 0 and on_segment(x3, y3, x4, y4, x2, y2):
            return True

        # Se não houver interseção ou sobreposição
        return False


    def get_overlapping_edges(self):
        """Retorna uma lista de pares de arestas que estão se sobrepondo."""
        overlapping_edges = []
        edges = list(self.graph.edges())
        for i, edge1 in enumerate(edges):
            for edge2 in edges[i + 1:]:
                # Chama a função de verificação de sobreposição passando a posição dos nós corretamente
                if self.are_edges_overlapping(edge1, edge2, self.positions):
                    overlapping_edges.append((edge1, edge2))
        return overlapping_edges



# Instancia o grafo interativo
interactive_graph = InteractiveGraph()

# Adiciona nós e arestas iniciais
interactive_graph.add_node(0, (100, 100))
interactive_graph.add_node(1, (300, 200))
interactive_graph.add_node(2, (500, 400))
interactive_graph.add_node(3, (700, 150))
interactive_graph.add_node(4, (800, 150))
interactive_graph.add_edge(0, 1)
interactive_graph.add_edge(0, 2)
interactive_graph.add_edge(2, 3)
interactive_graph.add_edge(0, 4)

def main():
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Botão esquerdo do mouse
                    mouse_pos = event.pos
                    if WIDTH - 110 <= mouse_pos[0] <= WIDTH - 10 and HEIGHT - 60 <= mouse_pos[1] <= HEIGHT - 20:
                        print("Overlapping nodes:", interactive_graph.get_overlapping_nodes())
                        print("Overlapping edges:", interactive_graph.get_overlapping_edges())
                        interactive_graph.reposition_nodes()
                    else:
                        interactive_graph.selected_node = interactive_graph.get_node_at_position(mouse_pos)

            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:  # Botão esquerdo do mouse
                    interactive_graph.selected_node = None

            elif event.type == pygame.MOUSEMOTION:
                if interactive_graph.selected_node is not None:
                    # Atualiza a posição do nó selecionado
                    interactive_graph.positions[interactive_graph.selected_node] = event.pos

        interactive_graph.draw()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()
