from pathlib import Path
from gerrychain import Graph
import numpy as np
from typing import Optional

from map_analyzer.maps.load_maps import MapType, StateCode, load_all_maps
from map_analyzer.models.graph_generating_model import GraphGeneratingModel


class RealLifeMaps(GraphGeneratingModel):
    all_maps: dict[MapType, dict[StateCode, Graph]]

    def __init__(self, cache_dir: Path, map_types: Optional[list[MapType]] = None):
        self.all_maps = load_all_maps(cache_dir, map_types)

    def generate_graph(self, seed=None, param_dict=None) -> Graph:
        # WARN: This picks any category at random.
        # TODO: Depending on the implementation of our experiments, we should probably restrict to a single category or merge map types
        rng = np.random.default_rng(seed)
        selected_map_type = rng.choice(list(self.all_maps.keys()))
        selected_state_code = rng.choice(list(self.all_maps[selected_map_type].keys()))
        selected_map = self.all_maps[selected_map_type][selected_state_code]
        return selected_map
