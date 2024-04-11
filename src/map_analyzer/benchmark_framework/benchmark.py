from typing import Callable
from gerrychain import Graph


class Benchmark:
    name: str
    num_scores: int
    score_calculator: Callable[[Graph], list[float]]

    def __init__(
        self,
        name: str,
        num_scores: int,
        score_calculator: Callable[[Graph], list[float]],
    ):
        self.name = name
        self.num_scores = num_scores
        self.score_calculator = score_calculator

    def score_graph(self, graph: Graph) -> list[float]:
        scores = self.score_calculator(graph)
        if len(scores) != self.num_scores:
            raise Exception(
                f"While computing benchmark {self.name} the scoring function returned {len(scores)} but was supposed to return {self.num_scores}"
            )
        return scores
