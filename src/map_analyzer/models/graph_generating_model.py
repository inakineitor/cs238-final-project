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

        if opt_params: # indicates a null model
            returnres = []
            if opt_params['model'] == 'tri': # triangle deletion model
                for i in range(num_graphs):
                    params = {}
                    params['p_delete'] = opt_params['p_delete']
                    params['n'] = opt_params['num_vertices'][i]
                    returnres.append(self.generate_graph(seed=rng, param_dict=params))
                return returnres
        else: # real life graphs
            return [self.generate_graph(seed=rng, param_dict=opt_params) for _ in range(num_graphs)]
