from abc import ABC, abstractmethod
from dataclasses import dataclass
from rich.table import Table

import numpy as np
from gerrychain import Graph

from map_analyzer.models import (
    real_life_maps,
    triangle_edge_deletion,
    flood_fill,
    waxman,
)
