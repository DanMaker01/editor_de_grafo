import pygame
from botao import Botao
from grapheditor import GraphEditor
from random_walker import RandomWalker
import networkx as nx

class Interface:
    def __init__(self, screen, G, pos):
        self.screen = screen
        self.graph = G
        self.pos = pos
        self.editor = GraphEditor(G, pos)
        self.walker = RandomWalker(G, screen, pos)
        self.largura_barra = 180
        self._criar_botoes()

    def _criar_botoes(self):
        """Cria e posiciona todos os botões da interface"""
        self.botoes = [
            Botao("Iniciar passeio", (10, 20), (160, 40), lambda: self.walker.reset()),
            Botao("Sortear próximo", (10, 70), (160, 40), lambda: self.walker.avancar()),
            Botao("Resetar Grafo", (10, 120), (160, 40), lambda: self.editor.reset_positions()),
            Botao("Adicionar Filho", (10, 170), (160, 40), self._adicionar_filho),
            Botao("Normalizar Pesos", (10, 220), (160, 40), self._normalizar_pesos),
        ]

    def _adicionar_filho(self):
        """Adiciona um nó filho ao nó selecionado com conexão bidirecional"""
        if self.editor.selected_node is not None:
            novo_no = self.editor.add_child_node(self.editor.selected_node)
            if novo_no is not None:
                print(f"Adicionado nó {novo_no} conectado ao nó {self.editor.selected_node}")
        else:
            print("Nenhum nó selecionado! Selecione um nó primeiro.")

    def _normalizar_pesos(self):
        """Normaliza os pesos das arestas do nó selecionado para soma 1"""
        if self.editor.selected_node is not None:
            if self.editor.normalizar_pesos(self.editor.selected_node):
                print(f"Pesos normalizados para o nó {self.editor.selected_node}")
            else:
                print(f"Nó {self.editor.selected_node} não tem arestas de saída")
        else:
            print("Nenhum nó selecionado!")

    def desenhar_interface(self):
        """Desenha todos os elementos da interface na tela"""
        # Fundo preto
        self.screen.fill((0, 0, 0))
        
        # Desenha o grafo
        self.editor.draw(self.screen)
        
        # Barra lateral
        pygame.draw.rect(self.screen, (240, 240, 240), 
                        (0, 0, self.largura_barra, self.screen.get_height()))
        
        # Botões
        for botao in self.botoes:
            botao.desenhar(self.screen)
        
        # Walker (caminhante aleatório)
        self.walker.draw()

    def handle_event(self, event):
        """Processa eventos da interface"""
        # Eventos dos botões
        for botao in self.botoes:
            botao.handle_event(event)
        
        # Eventos do editor (seleção, arraste, edição)
        self.editor.handle_event(event)
        
        # Atalho: botão direito para adicionar filho
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
            self._adicionar_filho()

    def update(self):
        """Atualiza a lógica da interface"""
        self.walker.update()