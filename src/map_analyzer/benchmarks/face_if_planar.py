import networkx as nx

from ..benchmark_framework.benchmark import Benchmark
from sage.graphs.graph_input import from_networkx_graph
from sage.graphs.planarity import is_planar
from sage.all import Graph

class FaceIfPlanarBenchmark(Benchmark):
    def score_graph(self, graph) -> float:
        if nx.check_planarity(graph):
            G = Graph()
            from_networkx_graph(G, graph)
            faces = G.faces()
            face_stats = [0 for i in range(500)]
            for i in range(len(faces)):
                face_stats[len(faces[i])-1] += 1

            return face_stats[2] / sum(face_stats)
        else:
            return -1
