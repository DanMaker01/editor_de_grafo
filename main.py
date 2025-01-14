import pygame
import networkx as nx
import random
from config import *
from grafointerativo import InteractiveGraph

# ----------------------------------------------------------------------
# TO-DO
# ----------------------------------------------------------------------
# - Adicionar o botão de criar nó aonde clicar
# - Adicionar o botão de remover nó aonde clicar
# - Melhorar a função de espalhamento
# - Modularizar mais
#
#
#
# ----------------------------------------------------------------------

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

def main():
    interactive_graph = InteractiveGraph()

    # Adiciona nós e arestas iniciais
    interactive_graph.add_node(0, (100, 100))
    interactive_graph.add_node(1, (300, 200))
    interactive_graph.add_node(2, (500, 400))
    interactive_graph.add_node(3, (700, 500))
    interactive_graph.add_node(4, (900, 600)) 
    interactive_graph.add_node(5, (200, 600)) 
    for i in range(10):
        interactive_graph.add_node(i, (random.randint(0, 1000), random.randint(0, 1000)))


    interactive_graph.add_edge(0, 1)
    interactive_graph.add_edge(0, 2)
    interactive_graph.add_edge(2, 3)
    interactive_graph.add_edge(3, 4)
    interactive_graph.add_edge(3, 5)

    for i in range(10):
        interactive_graph.add_edge(random.randint(0, 9), random.randint(0, 9))


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
                            while len(interactive_graph.get_overlapping_edges()) > 1:
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
                    elif event.button == 3: # Clique com o botão direito
                        print("clicou com")
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
