import pygame
import networkx as nx
import random
from config import *

class InteractiveGraph:
    def __init__(self):
        self.graph = nx.DiGraph()
        self.positions = {}
        self.selected_nodes = []  # Lista de nós selecionados
        self.dragging_node = None

    def add_node(self, node, position):
        self.graph.add_node(node)
        self.positions[node] = position

    def add_edge(self, parent, child):
        self.graph.add_edge(parent, child)

    def remove_node(self, node):
        if node in self.graph:
            self.graph.remove_node(node)
            self.positions.pop(node, None)

    def inside_window(self):
        # verify if all the nodes are inside the window
        for node, pos in self.positions.items():
            if pos[0] < 0 or pos[0] > WIDTH or pos[1] < 0 or pos[1] > HEIGHT:
                return False
        return True

    def set_all_inside_window(self) -> None:
        """Ensures all nodes are inside the window."""
        for node, pos in self.positions.items():
            if pos[0] < 0 or pos[0] > WIDTH or pos[1] < 0 or pos[1] > HEIGHT:
                self.positions[node] = (random.randint(0, WIDTH), random.randint(0, HEIGHT))

    def reset_all_node_position(self):
        for node, pos in self.positions.items():
            self.positions[node] = (random.randint(0, WIDTH), random.randint(0, HEIGHT))    


    def draw(self):
        """Desenha o grafo na tela."""
        # Cria uma superfície temporária (buffer) para o grafo e HUD
        temp_surface = pygame.Surface((WIDTH, HEIGHT))
        temp_surface.fill(WHITE)  # Preenche o fundo com branco

        # Desenha as arestas
        for edge in self.graph.edges():
            pygame.draw.line(temp_surface, BLACK, self.positions[edge[0]], self.positions[edge[1]], 2)

        # Desenha os nós e números
        for node, pos in self.positions.items():
            color = RED if node in self.selected_nodes else BLUE
            pygame.draw.circle(temp_surface, color, pos, NODE_RADIUS)

            # Desenha o número do vértice ao lado do nó
            font = pygame.font.SysFont(None, 24)
            text = font.render(str(node), True, BLACK)
            temp_surface.blit(text, (pos[0] + NODE_RADIUS + 5, pos[1] - NODE_RADIUS))

        # Desenha o HUD (informações)

        # Blit o conteúdo do buffer na tela principal
        window.blit(temp_surface, (0, 0))
        # pygame.display.flip()

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
        # Função para calcular a orientação de 3 pontos
        def orientation(px, py, qx, qy, rx, ry):
            val = (qy - py) * (rx - qx) - (qx - px) * (ry - qy)
            if val == 0:
                return 0  # Colinear
            elif val > 0:
                return 1  # Horário
            else:
                return 2  # Antihorário

        # Função para  se um ponto está no segmento de reta
        def on_segment(px, py, qx, qy, rx, ry):
            return min(px, qx) <= rx <= max(px, qx) and min(py, qy) <= ry <= max(py, qy)

        # Calcula as orientações dos quatro pares de pontos
        o1 = orientation(*positions[edge1[0]], *positions[edge1[1]], *positions[edge2[0]])
        o2 = orientation(*positions[edge1[0]], *positions[edge1[1]], *positions[edge2[1]])
        o3 = orientation(*positions[edge2[0]], *positions[edge2[1]], *positions[edge1[0]])
        o4 = orientation(*positions[edge2[0]], *positions[edge2[1]], *positions[edge1[1]])

        # Se as arestas se intersectam
        if o1 != o2 and o3 != o4:
            return True

        # Casos especiais (colineares)
        if o1 == 0 and on_segment(*positions[edge1[0]], *positions[edge1[1]], *positions[edge2[0]]):
            return True
        if o2 == 0 and on_segment(*positions[edge1[0]], *positions[edge1[1]], *positions[edge2[1]]):
            return True
        if o3 == 0 and on_segment(*positions[edge2[0]], *positions[edge2[1]], *positions[edge1[0]]):
            return True
        if o4 == 0 and on_segment(*positions[edge2[0]], *positions[edge2[1]], *positions[edge1[1]]):
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
                    # Se houver sobreposição, adiciona o par de arestas
                    #ignorar se o cruzamento ocorre apenas no vertice
                    if edge1[0] != edge2[0] and edge1[0] != edge2[1] and edge1[1] != edge2[0] and edge1[1] != edge2[1]:
                        overlapping_edges.append((edge1, edge2))
                    else:
                        pass
        return overlapping_edges
