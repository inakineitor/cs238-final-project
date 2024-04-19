from pathlib import Path
from gerrychain import Graph
import numpy as np
from typing import Optional

from map_analyzer.maps.load_maps import MapType, StateCode, load_all_maps
from map_analyzer.models.graph_generating_model import GraphGeneratingModel


class RealLifeMaps(GraphGeneratingModel):
    all_maps: dict[MapType, dict[StateCode, Graph]]

    def __init__(self, cache_dir: Path, map_types: Optional[list[MapType]] = None):
        # Only load the and randomly select maps from the specified map levels/types
        self.all_maps = load_all_maps(cache_dir, map_types)

    def generate_graph(self, seed=None, param_dict=None) -> Graph:
        rng = np.random.default_rng(seed)
        selected_map_type = rng.choice(list(self.all_maps.keys()))
        selected_state_code = rng.choice(list(self.all_maps[selected_map_type].keys()))
        selected_map = self.all_maps[selected_map_type][selected_state_code]
        return selected_map
