
import networkx as nx
from geopy.distance import geodesic, distance

from database.DAO import DAO


class Model:
    def __init__(self):
        self._grafo = nx.Graph()
        self._nodes= []
        self._edges = []
        self.solBest = 0
        self.path = []
        self.path_edge = []


    def getPath(self):
        #self.solBest = 0
        self.path = []
        self.path_edge = []

        for n in self._nodes:
            parziale = []
            parziale.append(n)
            self.ricorsione(parziale, [])

    def ricorsione(self, parziale, parziale_edge):
        n_last = parziale[-1]

        vicini = self.getViciniAmmissibili(n_last, parziale_edge)

        if len(vicini) == 0:
            peso_percorso = self.getPesoPercorso(parziale_edge)
            print(peso_percorso)
            if peso_percorso > self.solBest:
                self.solBest = peso_percorso + 0.0
                self.path = parziale[:]
                self.path_edge = parziale_edge[:]
            return

    def getViciniAmmissibili(self, n_last, parziale_edge):
        all_neigh = self._grafo.edges(n_last, data=True)
        result = []
        for e in all_neigh:
            if len(parziale_edge) != 0:
                if e[2]["weight"] > parziale_edge[-1][2]:
                    result.append(e[1])
            else:
                result.append(e[1])
        return result

    def getPesoPercorso(self, mylist):
        weight = 0
        for e in mylist:
            #weight += geodesic((e[0].lat, e[0].lng), (e[1].lat, e[1].lng)).km
            weight += distance.geodesic((e[0].lat, e[0].lng), (e[1].lat, e[1].lng)).km
        print(weight)
        return weight


    def getAnni(self):
        return DAO.getAnni()

    def getForme(self, anno):
        return DAO.getForme(anno)

    def buildGraph(self, anno, forma):
        self._grafo.clear()

        self._nodes = DAO.getStati()
        self._grafo.add_nodes_from(self._nodes)
        self._idMap = {}
        for n in self._nodes:
            self._idMap[n.id] = n

        archi = DAO.getAvvistamenti(forma, anno)
        for a in archi:
            self._edges.append((self._idMap[a[0]], self._idMap[a[1]], a[2]))
        self._grafo.add_weighted_edges_from(self._edges)



    def getPesiAdiacenti(self):
        tupla = []
        for n in self._nodes:
            peso = 0
            vicini = list(nx.neighbors(self._grafo, n))
            for v in vicini:
                peso += self._grafo[n][v]["weight"]
            tupla.append((n, peso))
        return tupla


    def getNumNodes(self):
        return len(self._grafo.nodes)

    def getNumEdges(self):
        return len(self._grafo.edges)

