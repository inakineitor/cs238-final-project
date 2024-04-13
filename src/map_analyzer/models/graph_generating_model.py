from abc import ABC, abstractmethod
import numpy as np
from typing import Optional, Union, Any

from gerrychain import Graph
from numpy.random import Generator


class GraphGeneratingModel(ABC):
    @abstractmethod
    def generate_graph(self, seed: Optional[Union[int, Generator]] = None) -> Graph:
        pass

    def generate_graphs(
        self, num_graphs: int, seed: Optional[int] = None, opt_params: Optional[dict[str, Any]] = None
    ) -> list[Graph]:
        rng = np.random.default_rng(seed)
        return [self.generate_graph(seed=rng) for _ in range(num_graphs)]
