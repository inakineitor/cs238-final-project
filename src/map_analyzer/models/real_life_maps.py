from dataclasses import dataclass
from pathlib import Path
from gerrychain import Graph
import numpy as np
from typing import Optional
import warnings

from map_analyzer.benchmark_framework.model_constraint_generator import ModelConstraints
from map_analyzer.maps.load_maps import MapType, StateCode, load_all_maps
from map_analyzer.models.graph_generating_model import (
    GraphGeneratingModel,
    GraphGeneration,
)


@dataclass
class RealLifeMapMetadata:
    state_code: StateCode
    map_type: MapType


class RealLifeMaps(GraphGeneratingModel[RealLifeMapMetadata]):
    all_maps: dict[MapType, dict[StateCode, Graph]]

    def __init__(self, cache_dir: Path, map_types: Optional[list[MapType]] = None):
        # Only load the and randomly select maps from the specified map levels/types
        self.all_maps = load_all_maps(cache_dir, map_types)

    # TODO: Respect constraints in the future
    def generate_graph(
        self, constraints, seed=None
    ) -> GraphGeneration[RealLifeMapMetadata]:
        rng = np.random.default_rng(seed)
        selected_map_type = rng.choice(list(self.all_maps.keys()))
        selected_state_code = rng.choice(list(self.all_maps[selected_map_type].keys()))
        selected_map = self.all_maps[selected_map_type][selected_state_code]
        return GraphGeneration(
            graph=selected_map,
            metadata=RealLifeMapMetadata(
                state_code=selected_state_code, map_type=selected_map_type
            ),
        )

    # TODO: Make a different function to do this and just sample with replacement for this one following constraints
    def generate_graphs(
        self, num_graphs, constraints, seed=None
    ) -> list[GraphGeneration[RealLifeMapMetadata]]:
        warnings.warn(
            "`num_graphs` parameter is ignored by RealLifeMaps model (all loaded maps will be returned)."
        )

        if seed is not None:
            raise ValueError("Seed is not supported by RealLifeMaps model.")

        return [
            GraphGeneration(
                graph=self.all_maps[map_type][state_code],
                metadata=RealLifeMapMetadata(state_code=state_code, map_type=map_type),
            )
            for map_type in self.all_maps.keys()
            for state_code in self.all_maps[map_type].keys()
        ]

    def get_all_graphs(self) -> list[GraphGeneration[RealLifeMapMetadata]]:
        return self.generate_graphs(
            num_graphs=0,
            constraints=ModelConstraints(
                num_nodes=0,
                max_edge_length=0,
            ),
        )
