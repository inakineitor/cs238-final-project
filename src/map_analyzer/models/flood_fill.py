from warnings import warn
from gerrychain import Graph
import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
from random import choice
import random
import string
from map_analyzer.models.graph_generating_model import GraphGeneratingModel, GraphGeneration
import math
# from graph_generating_model import GraphGeneratingModel, GraphGeneration

DISPLAY_PLOTS = True
DISPLAY_PLOT_OPTIONS = {"node_size": 500}

# For titles, because we don't pass in the state info yet
def generate_random_string(length):
    # Choose from letters and digits
    characters = string.ascii_letters + string.digits
    # Generate a random string of specified length
    random_string = ''.join(random.choice(characters) for _ in range(length))
    return random_string

## random.choice() doesn't support sets, but we can still get the fast ops we want
## https://stackoverflow.com/questions/15993447/python-data-structure-for-efficient-add-remove-and-random-choice

class ListDict(object):
    def __init__(self):
        self.item_to_position = {}
        self.items = []

    def add_item(self, item):
        if item in self.item_to_position:
            return
        self.items.append(item)
        self.item_to_position[item] = len(self.items)-1

    def remove_item(self, item):
        position = self.item_to_position.pop(item)
        last_item = self.items.pop()
        if position != len(self.items):
            self.items[position] = last_item
            self.item_to_position[last_item] = position

    def choose_random_item(self):
        return random.choice(self.items)

    def __contains__(self, item):
        return item in self.item_to_position

    def __iter__(self):
        return iter(self.items)

    def __len__(self):
        return len(self.items)

class FloodFillModel(GraphGeneratingModel):
    def __init__(self):
        """
        Constructor for the FloodFillModel.
        """

    def generate_graph(self, constraints, seed=None) -> GraphGeneration[None]:
        num_points = constraints.num_nodes
        randstring = generate_random_string(5) # id for this run

        # I want there to be approximately 5 tiles per walker by the end, so the way I will do this is say
        # (n/k)^2 = 5n => k^2 = n/5
        graph_width = round(num_points / int(math.sqrt(num_points/4)))
        graph_height = round(num_points / int(math.sqrt(num_points/4)))

        rng = np.random.default_rng(seed)
        num_walkers = num_points  # number of walkers

        # TODO: Update this with message passing
        grid = nx.grid_graph([graph_width, graph_height])

        # Move into ListDict
        unassigned = list(grid.nodes())
        object = ListDict()
        for i in unassigned:
            object.add_item(i)
        
        # Init 
        walkers = []
        cdict = {x: 0 for x in grid.nodes()}
        print(f"Num Walkers: {num_walkers}")
        for i in range(num_walkers):
            print(i)
            walker_starting_position = object.choose_random_item()
            walkers.append(walker_starting_position)
            object.remove_item(walker_starting_position)
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
            plt.title(f"Initial Walkers (n={num_walkers})")
            plt.savefig(f"Initial_Walkers_{randstring}.png")
            #plt.show()

        while len(object) > 0:
            order = list(range(len(walkers)))
            rng.shuffle(order)

            for i in order:
                try:
                    potential_moves = list(grid.neighbors(walkers[i]))
                except:
                    print(len(walkers))
                if not potential_moves or all(
                    [move not in object for move in potential_moves]
                ):
                    walkers.pop(i)
                    print(f"Walkers: {len(walkers)}")
                    break
                    
                old = walkers[i]
                walkers[i] = tuple(rng.choice(potential_moves))
                if walkers[i] in object:
                    object.remove_item(walkers[i])
                    print(f"Removal: {len(object)}")
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
            plt.title(f"Dual Graph (n={num_walkers})")
            plt.savefig(f"Dual_Graph_{randstring}.png")
            #plt.show()

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
            plt.title(f"Full Partition (n={num_walkers})")
            plt.savefig(f"Full_Partition_{randstring}.png")
            #plt.show()

        return GraphGeneration(graph=dual_graph, metadata=None)
