import networkx as nx

from ..benchmark_framework.benchmark import Benchmark, BenchmarkResults
from sage.graphs.graph_input import from_networkx_graph
from sage.graphs.planarity import is_planar
from sage.all import Graph


class FaceIfPlanarBenchmark(Benchmark):
    def score_graph(self, graph) -> float:
        if nx.is_planar(graph):
            G = Graph()
            from_networkx_graph(G, graph)
            faces = G.faces()
            num_faces_with_3_sides = sum([1 for face in faces if len(face) == 3])
            total_num_faces = len(faces)
            return (
                num_faces_with_3_sides / total_num_faces if total_num_faces > 0 else 0
            )
            # face_stats = [0 for i in range(500)]
            # for i in range(len(faces)):
            #     face_stats[len(faces[i]) - 1] += 1
            #
            # return face_stats[2] / sum(face_stats)
        else:
            return -1

    @classmethod
    def print_benchmark_metrics(cls, benchmark_results: BenchmarkResults):
        values = [
            x for x in benchmark_results.all_vals if x != -1
        ]  # -1 encodes non-planar
        num_nonplanar = benchmark_results.all_vals.count(-1)
        print("minimum: ", min(values))
        print("mean: ", sum(values) / len(values))
        print("maximum: ", max(values))
        print(
            f"Proportion of non-planar graphs: {num_nonplanar}/{len(benchmark_results.all_vals)}"
        )
