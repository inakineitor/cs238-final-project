from dataclasses import dataclass
from gerrychain import Graph


@dataclass
class ModelConstraints:
    num_nodes: int
    max_edge_length: float


def generate_constraints_from_graph(graph: Graph) -> ModelConstraints:
    # Generate constraints from graph
    num_nodes = graph.number_of_nodes()
    max_edge_length = 1  # TODO: Figure out how to calculate this. It appears that NetoworkX does not inherrently have a position for nodes unless a specific layout is specified.

    return ModelConstraints(num_nodes=num_nodes, max_edge_length=max_edge_length)
