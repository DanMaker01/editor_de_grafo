import pygame
import math
from collections import defaultdict

class GraphEditor:
    def __init__(self, graph, pos):
        self.graph = graph
        self.pos = pos
        self.selected_node = None
        self.selected_edge = None
        self.dragging = False
        self.editing_weight = False
        self.current_weight_text = ""
        self.offset = (0, 0)
        self.next_node_id = max(graph.nodes(), default=-1) + 1
        self.font = pygame.font.SysFont('Arial', 16)  # Cache da fonte
        self.node_radius = 20
        self.weight_radius = 10

    def normalizar_pesos(self, node):
        """Versão otimizada da normalização de pesos"""
        if node not in self.graph.nodes:
            return False

        successors = list(self.graph.successors(node))
        if not successors:
            return False

        weight = 1.0 / len(successors)
        for neighbor in successors:
            self.graph[node][neighbor]['weight'] = weight
        
        return True

    def add_child_node(self, parent_node):
        """Versão otimizada de adição de nó filho"""
        if parent_node not in self.graph.nodes:
            return None

        child_id = self.next_node_id
        self.next_node_id += 1

        self.graph.add_node(child_id)
        self.graph.add_edge(parent_node, child_id, weight=1.0)
        self.graph.add_edge(child_id, parent_node, weight=1.0)

        # Posição relativa com verificação de colisão
        base_x, base_y = self.pos[parent_node]
        offset = 50
        colisions = 1
        
        while any(math.hypot(base_x + offset - x, base_y + offset - y) < 2*self.node_radius 
                for x, y in self.pos.values()):
            offset += 20 * colisions
            colisions += 1

        self.pos[child_id] = (base_x + offset, base_y + offset)
        return child_id

    def handle_event(self, event):
        """Manipulador de eventos otimizado"""
        if event.type == pygame.MOUSEBUTTONDOWN:
            self._handle_mouse_down(event)
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            self.dragging = False
        elif event.type == pygame.MOUSEMOTION and self.dragging:
            self._handle_drag(event)
        elif event.type == pygame.KEYDOWN and self.editing_weight:
            self._handle_key_press(event)

    def _handle_mouse_down(self, event):
        mx, my = event.pos
        if event.button == 1:
            self._handle_left_click(mx, my)
        elif event.button == 3 and self.selected_node is not None:
            self.add_child_node(self.selected_node)

    def _handle_left_click(self, mx, my):
        self.editing_weight = False
        
        # Verifica clique em peso primeiro (área menor)
        for u, v, data in self.graph.edges(data=True):
            wx, wy = self._calculate_midpoint(u, v, offset=20)
            if (mx-wx)**2 + (my-wy)**2 <= self.weight_radius**2:
                self.selected_edge = (u, v)
                self.editing_weight = True
                self.current_weight_text = f"{data['weight']:.2f}"
                return

        # Verifica clique em nós
        for node, (x, y) in self.pos.items():
            if (mx-x)**2 + (my-y)**2 <= self.node_radius**2:
                self.selected_node = node
                self.dragging = True
                self.offset = (x - mx, y - my)
                return

        self.selected_node = None

    def _handle_drag(self, event):
        mx, my = event.pos
        self.pos[self.selected_node] = (mx + self.offset[0], my + self.offset[1])

    def _handle_key_press(self, event):
        if event.key == pygame.K_RETURN:
            try:
                new_weight = float(self.current_weight_text)
                if new_weight > 0:
                    u, v = self.selected_edge
                    self.graph[u][v]['weight'] = new_weight
            except ValueError:
                pass
            self.editing_weight = False
        elif event.key == pygame.K_BACKSPACE:
            self.current_weight_text = self.current_weight_text[:-1]
        elif event.unicode.replace('.', '', 1).isdigit():
            self.current_weight_text += event.unicode

    def _calculate_midpoint(self, u, v, offset=0):
        """Calcula ponto médio com offset perpendicular otimizado"""
        x1, y1 = self.pos[u]
        x2, y2 = self.pos[v]
        mx, my = (x1+x2)/2, (y1+y2)/2
        
        if offset:
            dx, dy = x2-x1, y2-y1
            length = max(1, math.hypot(dx, dy))
            nx, ny = -dy/length, dx/length
            return (mx + nx*offset, my + ny*offset)
        return (mx, my)

    def draw(self, screen):
        """Renderização otimizada"""
        # Desenho de arestas
        edge_color = (100, 100, 255)
        for u, v, data in self.graph.edges(data=True):
            pygame.draw.line(screen, edge_color, self.pos[u], self.pos[v], 2)
            
            wx, wy = self._calculate_midpoint(u, v, 20)
            weight_text = self.current_weight_text if (self.editing_weight and self.selected_edge == (u, v)) else f"{data['weight']:.2f}"
            
            if self.editing_weight and self.selected_edge == (u, v):
                pygame.draw.circle(screen, (255, 255, 0), (int(wx), int(wy)), 12)
            
            self._draw_text(screen, weight_text, (wx, wy))

        # Desenho de nós
        for node, (x, y) in self.pos.items():
            color = (255, 0, 0) if node == self.selected_node else (200, 200, 200)
            pygame.draw.circle(screen, color, (int(x), int(y)), self.node_radius)
            self._draw_text(screen, str(node), (x, y), bg_alpha=128)

    def _draw_text(self, screen, text, pos, text_color=(255,255,255), bg_color=(0,0,0), bg_alpha=128):
        """Método otimizado para desenho de texto com fundo"""
        text_surf = self.font.render(text, True, text_color)
        text_rect = text_surf.get_rect(center=pos)
        
        if bg_alpha > 0:
            bg = pygame.Surface((text_rect.width+4, text_rect.height+4), pygame.SRCALPHA)
            bg.fill((*bg_color, bg_alpha))
            screen.blit(bg, (text_rect.x-2, text_rect.y-2))
        
        screen.blit(text_surf, text_rect)