# -*- coding at utf-8 -*-

# TODO: Se geramos um grafo contendo duas arestas exatamente iguais, só uma é computada. Preciso mudar a implementação base do armazenamento das arestas de `defaultdict(set)` para algum outro tipo hasheável que permita vértices iguais. Talvez `defaultdict(list)`?

from collections import defaultdict
import os
import csv
from random import choice


class Grafo(object):
    """A (multi)graph implementation in python. Probably not the most optimized.
    """

    def __init__(self, arestas, direcionado=False):
        """Base structures.
        """
        self._adj = defaultdict(set)
        self.direcionado = direcionado
        self.adiciona_arestas(arestas)


    def get_vertices(self):
        """Returns the list of graph vertices.
        """
        return list(self._adj.keys())


    def get_arestas(self):
        """Returns the list of graph edges.
        """
        return [(k, v) for k in self._adj.keys() for v in self._adj[k]]

    def get_vizinhos(self, v) -> list:
        """Returns a list with the vertices adjacent to v
        """
        ans = list(self._adj[v])
        if ans == []:
            raise KeyError(f'404. {v} not found in graph.')
        return ans

    def adiciona_arestas(self, arestas):
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

    def adiciona_aresta(self, u, v):
        """Adds an incident edge to the 'u' and 'v' vertices.
        """
        self._adj[u].add(v)
        if not self.direcionado:
            self._adj[v].add(u)

    def conexo(self):
        """Return the boolean if the graph is connected and the connected components
        
        Parameters
        ----------
        
        Returns
        -------
        bool
            If the graph is connected
        list of sets
            Connected components of the graph
        
        Notes
        -----
        https://pt.wikipedia.org/wiki/Busca_em_largura
        """
        comp_conex = []
        desconhecidos = set(self._adj)

        while not len(desconhecidos) == 0:
            v = choice(list(desconhecidos))
            fila = list(self._adj[v]) # vértices a serem buscados
            mapeados = {v}.union(self._adj[v]) # vértices já encontrados
            while fila != []:
                v = fila[0]
                del(fila[0])
                adjacentes = list(self._adj[v])
                for v in adjacentes:
                    if not v in mapeados:
                        fila.append(v)
                    mapeados.add(v)

            comp_conex.append(mapeados)
            desconhecidos.difference_update(mapeados)

        if len(comp_conex) == 1: # A partir do vértice inicial, se a busca encontrou todos os vértices do grafo, então ele é conexo.
            return True, comp_conex

        else:
            return False, comp_conex

    def existe_aresta(self, u, v):
        """Return the boolean if exists at least one edge connecting  u  and  v.
        """
        return u in self._adj and v in self._adj[u]
    
    def g(self, v) -> int:
        """Return o grau de  v.
        """
        if not v in self._adj:
            raise KeyError(f'404. {v} not found in graph.')
        return len(self.get_vizinhos(v))

    def euleriano(self):
        """Return the boolean if the graph is eulerian.
        """
        V = self.get_vertices()
        for v in V:
            if len(self.get_vizinhos(v)) % 2 != 0:
                return False
        return True
        
    def bipartido(self):
        """Retorna o booleano se o grafo é bipartido.
        
        Notes
        -----
        Ele é bipartido se, e somente se, não admite um ciclo ímpar.
        """
        raise NotImplementedError
    
    def dist(self, u, v):
        """Retorna a distância entre os vértices  u  e  v.
        
        Notes
        -----
        Definimos a distância como o número de arestas no menor u-v caminho.
        """
        if not (u in self._adj and v in self._adj): raise KeyError(r'404. u ou v \notin{E(G)}')
        if u == v: return 0
        encontrados = {u: 0} # vertice : dist(u)
        fila = list(self._adj[u])
        
        while True:
            adjacentes = list(self._adj[u]) # vértices a serem buscados
            for w in adjacentes:
                if w == v:
                    return encontrados[u] +1
                elif not encontrados.get(w): # Se  w  não está em encontrados
                    encontrados[w] = encontrados.get(u) +1
                    fila.append(w)
            if fila == []:
                return float('inf')
            u = fila[0]
            del(fila[0])

    def tracavel(self):
        """Verify if the graph is traceable. In other words, verify if the graph contains an open eulerian track that contains all the vertices in the graph.
        
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

    def __len__(self):
        return len(self._adj)


    def __str__(self):
        return f'{self.__class__.__name__}({dict(self._adj)})'


    def __getitem__(self, v):
        return self._adj[v]





def gera_codigo_graphviz(arestas, visual=False) -> str:
    """Imprime o código fonte para vizualizar o grafo não direcionado com tais arestas.

    Para vizualizar, rode:
    dot -Tpng -O path.dot
    """
    txt = '''graph grafo {
  node [shape=box];'''

    for A,B in arestas:
        tmp = f'  {A} -- {B};\n'
        txt += tmp

    txt += '}'

    if visual: print(txt)
    return txt

def plot(G, output='output.png'):
    """Utilizamos a dot language para criar uma imagem de um grafo.

    Parameters
    ----------
    G : Grafo
        Grafo a ser plotado.
    output : str
        Nome do arquivo da imagem do grafo.
        
    Output
    ------
    grafo.png
        Grafo.
    """
    edges = G.get_arestas()
    code = gera_codigo_graphviz(edges)
    with open('tmp.gv', mode='w') as f:
        f.write(code)
    os.system(f'dot -Tpng tmp.gv -o {output}')
    os.remove('tmp.gv')

def csv2grafo(path, direcionado=False) -> Grafo:
    """Transforma um arquivo csv em um grafo utilizável.

    Parâmetros
    ----------
    path : str
        Caminho do arquivo csv.
    direcionavel : bool, opcional
        Se o grafo é direcionado. O padrão é False.

    Returns
    -------
    Grafo.
        Retorna o grafo contido no csv.
    """
    with open(path, newline='') as csvfile:
        tudo = csv.reader(csvfile, delimiter=',', quotechar='|')
        data = [tuple(x) for x in tudo if len(x) != 1]
    
    return Grafo(data, direcionado)
