from warnings import warn
from gerrychain import Graph
import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
from random import choice

from .graph_generating_model import GraphGeneratingModel, GraphGeneration

DISPLAY_PLOTS = False
DISPLAY_PLOT_OPTIONS = {"node_size": 500}


class FloodFillModel(GraphGeneratingModel):
    def __init__(self):
        """
        Constructor for the FloodFillModel.
        """

    def generate_graph(self, constraints, seed=None) -> GraphGeneration[None]:
        num_points = constraints.num_nodes
        graph_width = num_points
        graph_height = num_points

        rng = np.random.default_rng(seed)

        num_walkers = num_points  # number of walkers

        # grid = nx.grid_graph([self.graph_width, self.graph_height]) # TODO: Update this with message passing
        grid = nx.grid_graph([graph_width, graph_height])

        unassigned = list(grid.nodes())

        walkers = []

        cdict = {x: 0 for x in grid.nodes()}

        for i in range(num_walkers):
            walker_starting_position = tuple(rng.choice(unassigned))
            walkers.append(walker_starting_position)
            unassigned.remove(walker_starting_position)
            cdict[walker_starting_position] = i + 1

        if DISPLAY_PLOTS:
            print(grid)
            plt.figure()
            nx.draw(
                grid,
                pos={x: x for x in grid.nodes()},
                node_color=[cdict[x] for x in grid.nodes()],
                node_size=DISPLAY_PLOT_OPTIONS["node_size"],
                cmap="tab20",
                node_shape="s",
            )
            plt.title("Initial Walkers")
            plt.show()

        while unassigned:
            order = list(range(num_walkers))
            rng.shuffle(order)

            for i in order:
                potential_moves = list(grid.neighbors(walkers[i]))
                if not potential_moves or all(
                    [move not in unassigned for move in potential_moves]
                ):
                    walkers.pop(i)
                    continue

                old = walkers[i]
                walkers[i] = tuple(rng.choice(potential_moves))
                if walkers[i] in unassigned:
                    unassigned.remove(walkers[i])
                    cdict[walkers[i]] = i + 1
                    grid = nx.contracted_nodes(grid, walkers[i], old, self_loops=False)
                else:
                    walkers[i] = old

        dual_graph = grid

        if DISPLAY_PLOTS:
            print(dual_graph)
            plt.figure()
            nx.draw(
                dual_graph,
                pos={x: x for x in grid.nodes()},
                node_color=["k" for _ in grid.nodes()],
                node_shape="s",
                node_size=25,
            )
            plt.title("Dual Graph")
            plt.show()

        if DISPLAY_PLOTS:
            grid2 = nx.grid_graph([graph_width, graph_height])
            print(grid2)
            plt.figure()
            nx.draw(
                grid2,
                pos={x: x for x in grid2.nodes()},
                node_color=[cdict[x] for x in grid2.nodes()],
                node_size=DISPLAY_PLOT_OPTIONS["node_size"],
                cmap="tab20",
                node_shape="s",
            )
            plt.title("Full Partition")
            plt.show()

        return GraphGeneration(graph=dual_graph, metadata=None)
