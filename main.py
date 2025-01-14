import pygame
import networkx as nx
import random
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

def draw_hud(graph, selected_nodes):
    """Desenha o HUD com informações sobre o grafo e os nós selecionados."""
    font = pygame.font.SysFont(None, 24)
    vertices_text = f"Vértices: {graph.number_of_nodes()}"
    edges_text = f"Arestas: {graph.number_of_edges()}"

    vertices_surface = font.render(vertices_text, True, BLACK)
    edges_surface = font.render(edges_text, True, BLACK)

    window.blit(vertices_surface, (10, 10))
    window.blit(edges_surface, (10, 40))

    # Exibe os nós selecionados no HUD
    if selected_nodes:
        selected_text = f"Selecionados: {', '.join(map(str, selected_nodes))}"
        selected_surface = font.render(selected_text, True, BLACK)
        window.blit(selected_surface, (10, 70))

    # Desenha os botões
    pygame.draw.rect(window, GRAY, (WIDTH - 110, HEIGHT - 170, 100, 40))  # Novo botão
    font = pygame.font.SysFont(None, 24)
    text = font.render("Criar aresta", True, BLACK)
    window.blit(text, (WIDTH - 150, HEIGHT - 170))

    
    pygame.draw.rect(window, GRAY, (WIDTH - 110, HEIGHT - 110, 100, 40))  # Novo botão
    font = pygame.font.SysFont(None, 24)
    text = font.render("Verificar", True, BLACK)
    window.blit(text, (WIDTH - 150, HEIGHT - 110))

    #botão organizar
    pygame.draw.rect(window, GRAY, (WIDTH - 110, HEIGHT - 60, 100, 40))  # Botão existente
    text = font.render("Reorganizar", True, BLACK)
    window.blit(text, (WIDTH - 150, HEIGHT - 60))

    pygame.display.flip()

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

def main():
    interactive_graph = InteractiveGraph()

    # Adiciona nós e arestas iniciais
    interactive_graph.add_node(0, (100, 100))
    interactive_graph.add_node(1, (300, 200))
    interactive_graph.add_node(2, (500, 400))
    interactive_graph.add_node(3, (700, 500))
    interactive_graph.add_node(4, (900, 600)) 
    interactive_graph.add_node(5, (200, 600)) 


    interactive_graph.add_edge(0, 1)
    interactive_graph.add_edge(0, 2)
    interactive_graph.add_edge(2, 3)
    interactive_graph.add_edge(3, 4)
    interactive_graph.add_edge(3, 5)


    running = True
    interactive_graph.set_all_inside_window()
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.MOUSEBUTTONDOWN:
                # Verifica se um nó foi clicado
                node = interactive_graph.get_node_at_position(pygame.mouse.get_pos())
                if node is not None:
                    # Alterna a seleção do nó
                    if node in interactive_graph.selected_nodes:
                        interactive_graph.selected_nodes.remove(node)
                    else:
                        interactive_graph.selected_nodes.append(node)

                    # Inicia o arraste do nó
                    interactive_graph.dragging_node = node

                # Verifica se clicou em um botão (como no seu código original)
                else:
                    if event.button == 1:
                        print("Clicou no botão esquerdo")
                        button3_rect = pygame.Rect(WIDTH - 110, HEIGHT - 170, 100, 40)
                        button1_rect = pygame.Rect(WIDTH - 110, HEIGHT - 110, 100, 40)
                        button2_rect = pygame.Rect(WIDTH - 110, HEIGHT - 60, 100, 40)

                        if button1_rect.collidepoint(pygame.mouse.get_pos()): #
                            print(pygame.mouse.get_pos(), "clicou no botao1")
                            print("Sobreposicoes nós:", interactive_graph.get_overlapping_nodes())
                            print("Sobreposicoes de arestas:", interactive_graph.get_overlapping_edges())
                        
                        if button2_rect.collidepoint(pygame.mouse.get_pos()): #reorganizar
                            print(pygame.mouse.get_pos(), "clicou no botao2")
                            
                            interactive_graph.reset_all_node_position()
                            ite = 0
                            while len(interactive_graph.get_overlapping_edges()) > 0:
                                interactive_graph.reset_all_node_position()
                                ite+=1
                                if ite > 1000:
                                    break
                            
                            #espalhar os nós que se sobrepõem
                            for i in range(10):
                                interactive_graph.reposition_nodes()
                            print("Nos reorganizados.")

                        if button3_rect.collidepoint(pygame.mouse.get_pos()):
                            print(pygame.mouse.get_pos(), "clicou no botao3")
                            if len(interactive_graph.selected_nodes) == 2:
                                interactive_graph.add_edge(interactive_graph.selected_nodes[0], interactive_graph.selected_nodes[1])
                            else:
                                print("Selecione dois nos para adicionar uma aresta.")
                    elif event.button == 3:
                        pass

            elif event.type == pygame.MOUSEBUTTONUP:
                # Finaliza o arraste
                interactive_graph.dragging_node = None

            elif event.type == pygame.MOUSEMOTION:
                # Se estiver arrastando um nó, atualiza a posição dele
                if interactive_graph.dragging_node is not None:
                    node_pos = pygame.mouse.get_pos()
                    interactive_graph.positions[interactive_graph.dragging_node] = node_pos

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:  # Para reorganizar os nós
                    interactive_graph.reposition_nodes()
                    print("Nos reorganizados.")

                if event.key == pygame.K_w:  # Para imprimir a árvore
                    interactive_graph.set_all_inside_window()

        # Desenha o grafo
        interactive_graph.draw()
        
        draw_hud(interactive_graph.graph, interactive_graph.selected_nodes)

        # # Exibe o HUD
        # draw_hud(interactive_graph.graph, interactive_graph.selected_nodes)

        # Atualiza a tela
        # pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()
