import json
import os
from queue import Queue

import networkx as nx
import matplotlib.pyplot as plt

from Nodo import Node

class Graph:

    def __init__(self, directed=False):
        self.m_nodes = []
        self.m_directed = directed
        self.m_graph = {}
        self.m_h = {}  


    def load_json(self, filename):
        map_path = os.path.join('data', filename)

        with open(map_path, 'r') as file:
            loaded_data = json.load(file)

        for edge in loaded_data["edges"]:
            source = edge["source"]
            target = edge["target"]
            weight = edge["weight"]
            self.add_edge(source, target, weight)

        for node, heuristic_value in loaded_data["bestpath"].items():
            self.add_heuristica(node, heuristic_value, "bestpath")

        for node, heuristic_value in loaded_data["transit"].items():
            self.add_heuristica(node, heuristic_value, "transit")

        for node, heuristic_value in loaded_data["roadquality"].items():
            self.add_heuristica(node, heuristic_value, "roadquality")

    def locationExists(self, name):
        for node in self.m_nodes:
            if node.getName() == name:
                return True
        return False
    
    def getNeighbours(self, node):
        if node in self.m_graph:
            return self.m_graph[node]
        else:
            return []
        
    def getH(self, node, heuristic):
        return self.m_h.get(heuristic, {}).get(node, 0)

    def __str__(self):
        out = ""
        for key in self.m_graph.keys():
            out = out + "node" + str(key) + ": " + str(self.m_graph[key]) + "\n"
        return out

    def get_node_by_name(self, name):
        search_node = Node(name)
        for node in self.m_nodes:
            if node == search_node:
                return node
        return None

    def imprime_aresta(self):
        listaA = ""
        lista = self.m_graph.keys()
        for nodo in lista:
            for (nodo2, custo) in self.m_graph[nodo]:
                listaA = listaA + nodo + " ->" + nodo2 + " custo:" + str(custo) + "\n"
        return listaA

    def add_edge(self, node1, node2, weight):
        n1 = Node(node1)
        n2 = Node(node2)
        if (n1 not in self.m_nodes):
            n1_id = len(self.m_nodes) 
            n1.setId(n1_id)
            self.m_nodes.append(n1)
            self.m_graph[node1] = []

        if (n2 not in self.m_nodes):
            n2_id = len(self.m_nodes) 
            n2.setId(n2_id)
            self.m_nodes.append(n2)
            self.m_graph[node2] = []

        self.m_graph[node1].append((node2, weight))  

        if not self.m_directed:
              self.m_graph[node2].append((node1, weight))

    def getNodes(self):
        return self.m_nodes

    def get_arc_cost(self, node1, node2):
        custoT = None
        a = self.m_graph[node1]
        for (nodo, custo) in a:
            if nodo == node2:
                custoT = custo

        return custoT

    def calcula_custo(self, caminho):
        teste = caminho
        custo = 0
        i = 0
        while i + 1 < len(teste):
            custo = custo + self.get_arc_cost(teste[i], teste[i + 1])
            i = i + 1
        return custo

    def procura_DFS(self, start, end, path=None, visited=None):
        if path is None:
            path = []
        if visited is None:
            visited = set()

        path.append(start)
        visited.add(start)

        if start == end:
            custoT = self.calcula_custo(path)
            return (path, custoT)

        for (adjacente, peso) in self.m_graph[start]:
            if adjacente not in visited:
                resultado = self.procura_DFS(adjacente, end, path, visited.copy())
                if resultado is not None:
                    return resultado

        path.pop()
        return None

    def procura_BFS(self, start, end):
        visited = set()
        fila = Queue()
        custo = 0

        fila.put(start)
        visited.add(start)

        parent = dict()
        parent[start] = None

        path_found = False
        while not fila.empty() and path_found == False:
            nodo_atual = fila.get()

            neighbors = sorted(self.m_graph[nodo_atual], key=lambda x: x[0])

            for (adjacente, peso) in neighbors:
                if adjacente not in visited:
                    fila.put(adjacente)
                    parent[adjacente] = nodo_atual
                    visited.add(adjacente)

                    if adjacente == end:
                        path_found = True
                        break 

        path = []
        if path_found:
            path.append(end)
            while parent[end] is not None:
                path.append(parent[end])
                end = parent[end]
            path.reverse()
            custo = self.calcula_custo(path)

        return (path, custo)

    def desenha(self):
        lista_v = self.m_nodes
        lista_a = []
        g = nx.Graph()
        for nodo in lista_v:
            n = nodo.getName()
            g.add_node(n)
            for (adjacente, peso) in self.m_graph[n]:
                lista = (n, adjacente)
                g.add_edge(n, adjacente, weight=peso)

        pos = nx.spring_layout(g)
        nx.draw_networkx(g, pos, with_labels=True, font_weight='bold')
        labels = nx.get_edge_attributes(g, 'weight')
        nx.draw_networkx_edge_labels(g, pos, edge_labels=labels)

        plt.draw()
        plt.show()

    def add_heuristica(self, n, estima, heuristic):
        n1 = Node(n)
        if heuristic not in self.m_h:
            self.m_h[heuristic] = {}

        if n1 in self.m_nodes:
            self.m_h[heuristic][n] = estima


    def procura_aStar(self, start, end, h):
        open_list = {start}
        closed_list = set([])

        g = {}

        g[start] = 0

        parents = {}
        parents[start] = start
        while len(open_list) > 0:
            n = None

            for v in open_list:
                if n == None or g[v] + self.getH(v, h) < g[n] + self.getH(n, h):  
                    n = v
            if n == None:
                print('Path does not exist!')
                return None

            if n == end:
                reconst_path = []

                while parents[n] != n:
                    reconst_path.append(n)
                    n = parents[n]

                reconst_path.append(start)

                reconst_path.reverse()

                return (reconst_path, self.calcula_custo(reconst_path))

            for (m, weight) in self.getNeighbours(n): 
                if m not in open_list and m not in closed_list:
                    open_list.add(m)
                    parents[m] = n
                    g[m] = g[n] + weight
                else:
                    if g[m] > g[n] + weight:
                        g[m] = g[n] + weight
                        parents[m] = n

                        if m in closed_list:
                            closed_list.remove(m)
                            open_list.add(m)

            open_list.remove(n)
            closed_list.add(n)

        print('Path does not exist!')
        return None

    def greedy(self, start, end, h):
        open_list = set([start])
        closed_list = set([])

        parents = {}
        parents[start] = start

        while len(open_list) > 0:
            n = None

            for v in open_list:
                if n == None or self.getH(v, h) < self.getH(n, h):
                    n = v

            if n == None:
                print('Path does not exist!')
                return None

            if n == end:
                reconst_path = []

                while parents[n] != n:
                    reconst_path.append(n)
                    n = parents[n]

                reconst_path.append(start)

                reconst_path.reverse()

                return (reconst_path, self.calcula_custo(reconst_path))

            for (m, weight) in self.getNeighbours(n):
                if m not in open_list and m not in closed_list:
                    open_list.add(m)
                    parents[m] = n

            open_list.remove(n)
            closed_list.add(n)

        print('Path does not exist!')
        return None
