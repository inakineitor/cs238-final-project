from abc import ABC, abstractmethod
from dataclasses import dataclass
import numpy as np
from typing import Generic, Optional, Union, Any, TypeVar
from rich.progress import track

from gerrychain import Graph
from numpy.random import Generator

from map_analyzer.benchmark_framework.model_constraint_generator import ModelConstraints

MetadataType = TypeVar("MetadataType")


@dataclass
class GraphGeneration(Generic[MetadataType]):
    graph: Graph
    metadata: MetadataType


class GraphGeneratingModel(ABC, Generic[MetadataType]):
    @abstractmethod
    def generate_graph(
        self,
        constraints: ModelConstraints,
        seed: Optional[Union[int, Generator]] = None,
    ) -> GraphGeneration[MetadataType]:
        pass

    def generate_graphs(
        self,
        num_graphs: int,
        constraints: ModelConstraints,
        seed: Optional[int] = None,
    ) -> list[GraphGeneration[MetadataType]]:
        rng = np.random.default_rng(seed)

        return [
            self.generate_graph(constraints=constraints, seed=rng)
            for _ in track(
                range(num_graphs),
                description=f"Generating {self.__class__.__name__} graphs...",
            )
        ]
