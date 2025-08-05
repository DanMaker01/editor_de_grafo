import pygame
import random
import numpy as np
from typing import Dict, List, Tuple, Optional


class Grafo:
    def __init__(self, direcionado: bool = True):
        """
        Classe que representa a estrutura do grafo
        
        Args:
            direcionado: Bool indicando se o grafo é direcionado (padrão: True)
        """
        self.direcionado = direcionado
        self.vertices = {}  # {nome: (x, y)}
        self.arestas = {}  # {(origem, destino): peso}
        
    def adicionar_vertice(self, nome: str, posicao: Tuple[int, int]) -> None:
        """Adiciona um vértice ao grafo com posição (x, y)"""
        self.vertices[nome] = posicao
        
    def adicionar_aresta(self, origem: str, destino: str, peso: float = 1.0) -> None:
        """Adiciona uma aresta entre dois vértices"""
        if origem not in self.vertices or destino not in self.vertices:
            raise ValueError("Vértices não existem no grafo")
            
        self.arestas[(origem, destino)] = peso
        if not self.direcionado:
            self.arestas[(destino, origem)] = peso
            
    def gerar_matriz_estocastica(self) -> Dict[str, Dict[str, float]]:
        """Gera uma matriz estocástica a partir das arestas"""
        matriz = {}
        
        for origem in self.vertices:
            matriz[origem] = {}
            arestas_saida = [(dest, peso) for (orig, dest), peso in self.arestas.items() if orig == origem]
            
            if not arestas_saida:
                # Se não há arestas de saída, fica no mesmo estado
                matriz[origem][origem] = 1.0
            else:
                total_pesos = sum(peso for _, peso in arestas_saida)
                for dest, peso in arestas_saida:
                    matriz[origem][dest] = peso / total_pesos
                    
        return matriz
