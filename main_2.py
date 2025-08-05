import pygame
import random
import math
import networkx as nx
from grapheditor import GraphEditor
from botao import Botao
from random_walker import RandomWalker, draw_graph, layout_positions
from interface import Interface

def build_graph_from_matrix(matrix):
    G = nx.DiGraph()
    for i, row in enumerate(matrix):
        for j, prob in enumerate(row):
            if prob > 0:
                G.add_edge(i, j, weight=prob)
    return G

def main():
    pygame.init()
    screen = pygame.display.set_mode((1000, 600))
    pygame.display.set_caption("Passeio Aleatório com Matriz Estocástica")

    transition_matrix = [
        [0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
        [0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
        [0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
        [1/4, 1/4, 1/4, 0.0, 1/4, 0.0, 0.0, 0.0, 0.0, 0.0],
        [0.0, 0.0, 0.0, 0.5, 0.0, 0.5, 0.0, 0.0, 0.0, 0.0],
        [0.0, 0.0, 0.0, 0.0, 1/5, 0.0, 1/5, 1/5, 1/5, 1/5],
        [0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0],
        [0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0],
        [0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0],
        [0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0],
    ]

    G = build_graph_from_matrix(transition_matrix)
    pos = layout_positions(len(transition_matrix))
    interface = Interface(screen, G, pos)  # Ordem correta: screen primeiro

    clock = pygame.time.Clock()
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            interface.handle_event(event)

        interface.update()
        screen.fill((120,120,120))
        draw_graph(screen, G, pos)
        interface.desenhar_interface()  # Método renomeado
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()