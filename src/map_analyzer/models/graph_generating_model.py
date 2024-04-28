from abc import ABC, abstractmethod
from dataclasses import dataclass
import numpy as np
from typing import Generic, Optional, Union, Any, TypeVar
from rich.progress import track
import pickle
from gerrychain import Graph
from numpy.random import Generator

#from map_analyzer.benchmark_framework.model_constraint_generator import ModelConstraints
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
        # save_dir: Optional[Path] = None,
        # save_format: str = "npy",
    ) -> list[GraphGeneration[MetadataType]]:
        rng = np.random.default_rng(seed)
        graphs = []

        #if save_dir is not None:
           # save_dir.mkdir(parents=True, exist_ok=True)
    
        #for _ in track(
           # range(num_graphs),
            #description=f"Generating {self.__class__.__name__} graphs...",
            #):
            #graph_generation = self.generate_graph(constraints=constraints, seed=rng)
            #graphs.append(graph_generation)

        #if save_dir is not None:
           # if save_format == "npy":
                #graph_array = np.array([g.graph for g in graphs], dtype=object)
                #metadata_array = np.array([g.metadata for g in graphs], dtype=object)
                #np.save(save_dir / "graphs.npy", graph_array)
                #np.save(save_dir / "metadata.npy", metadata_array)
            #elif save_format == "pkl":
                #with open(save_dir / "graphs.pkl", "wb") as f:
                    #pickle.dump([g.graph for g in graphs], f)
                #with open(save_dir / "metadata.pkl", "wb") as f:
                    #pickle.dump([g.metadata for g in graphs], f)

        return [
            self.generate_graph(constraints=constraints, seed=rng)
            for _ in track(
                range(num_graphs),
                description=f"Generating {self.__class__.__name__} graphs...",
            )
        ]
