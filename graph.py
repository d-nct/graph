#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov 23 13:36:04 2020

@author: danieln
"""

version = 1.0


# Sessão de Importações
# ---------------------
import collections

# Definição da Classe
# -------------------
class Graph(object):
    """A (multi)graph implementation in python. Probably not the most optimized.
    """

    def __init__(self, arestas):
        """Base structures.
        """
        self.adj = collections.defaultdict(set)

    def get_vertices(self):
        """Returns the list of graph vertices.
        """
        return list(self.adj.keys())


    def get_edges(self):
        """Returns the list of graph edges.
        """
        return [(k, v) for k in self.adj.keys() for v in self.adj[k]]

    def get_adjacents(self, v) -> list:
        """Returns a list with the vertices adjacent to v
        """
        ans = list(self.adj[v])
        if ans == []:
            raise KeyError(f'404. {v} not found in graph.')
        return ans

    def add_edges(self, arestas):
        """Add edges to the graph. 
        
        Parameters
        ----------
        arestas: list
            Iterable-like with 2-uples of vertices.
        
        Returns
        -------
        None
        
        Exemple
        -------
        >>> G = Grafo( [(1,2),(1,3),(1,4)] )
        >>> new_edges = [(2,3),(3,4)]
        >>> G.adiciona_arestas(new_edges)
        """
        for u, v in arestas:
            self.adiciona_aresta(u, v)

    def add_edge(self, u, v):
        """Adds an incident edge to the 'u' and 'v' vertices.
        """
        self.adj[u].add(v)
        self.adj[v].add(u)

    def connected(self):
        """Return the boolean if the graph is connected.
        """
        raise NotImplementedError

    def exists_edge(self, u, v):
        """Return the boolean if exists at least one edge connecting  u  and  v.
        """
        return u in self.adj and v in self.adj[u]

    def eulerian(self):
        """Return the boolean if the graph is eulerian.
        """
        V = self.get_vertices()
        for v in V:
            if len(self.get_vizinhos(v)) % 2 != 0:
                return False
        return True

    def traceable(self):
        """Verify if the graph is traceable. In other words, if thr graph contains a open eulerian track that contains all the vertices in the graph.
        
        Returns
        -------
        bool
            If the graph is traceable.
        list
            List with  v  vertices such that  g(v)  is odd.
        
        Observação
        ----------
        Se existe um  k  natural tal que há  2k  vértices de grau ímpar, então o grafo contém  k  trilhas eulerianas abertas disjuntas em arestas, que, juntas, contém todos os vértices do grafo.
        """
        impares = []
        V = self.get_vertices()
        for v in V:
            if len(self.get_vizinhos(v)) % 2 != 0: # Se g(v) não é par
                impares.append(v)

        if len(impares) == 2: 
            return True, impares
        else:
            return False, impares