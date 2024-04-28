from abc import ABC, abstractmethod
from dataclasses import dataclass
from rich.table import Table
import pickle

import numpy as np
from gerrychain import Graph

@dataclass
class GraphData:
    def __init__(self, graph, metadata):
        self.graph = graph
        self.metadata = metadata


def find_table_column_id(table: Table, column_name: str) -> int:
    col_idx = -1
    for i in range(len(table.columns)):
        if table.columns[i].header == column_name:
            col_idx = i
            break
    return col_idx


def ensure_table_has_column(table: Table, column_name: str):
    col_idx = find_table_column_id(table, column_name)
    if col_idx == -1:
        table.add_column(column_name)
        col_idx = len(table.columns) - 1
    return col_idx


def add_values_to_table(table: Table, values: list[tuple[str, str]]):
    column_indexes = [
        ensure_table_has_column(table, col_name) for col_name, _ in values
    ]
    new_row = ["" for _ in range(len(table.columns))]
    for i in range(len(values)):
        _, val = values[i]
        col_idx = column_indexes[i]
        new_row[col_idx] = val
    table.add_row(*new_row)


@dataclass
class BenchmarkResults:
    minimum: float
    mean: float
    maximum: float
    all_vals: list[float]


class Benchmark(ABC):
    @abstractmethod
    def score_graph(self, graph: Graph) -> float:
        pass

    def score_graphs(self, graphs: list[Graph]) -> list[float]:
        return [self.score_graph(graph) for graph in graphs]

    def benchmark_graphs(self, graphs: list[Graph]) -> BenchmarkResults:
        scores = self.score_graphs(graphs)
        return BenchmarkResults(
            minimum=np.min(scores),
            mean=float(np.mean(scores)),
            maximum=np.max(scores),
            all_vals=scores,
        )

    @classmethod
    def print_benchmark_metrics(cls, benchmark_results: BenchmarkResults):
        for key in ["minimum", "mean", "maximum"]:
            print(f"{key}: {benchmark_results.__getattribute__(key)}")

    @classmethod
    def get_table_benchmark_metrics(cls, benchmark_results: BenchmarkResults) -> Table:
        table = Table()
        table.add_column("Minimum")
        table.add_column("Mean")
        table.add_column("Maximum")
        table.add_row(
            str(benchmark_results.minimum),
            str(benchmark_results.mean),
            str(benchmark_results.maximum),
        )
        return table

    @classmethod
    def add_benchmark_metrics_to_table(
        cls, table: Table, benchmark_name: str, benchmark_results: BenchmarkResults
    ):
        values = [
            (key, str(benchmark_results.__getattribute__(key)))
            for key in ["minimum", "mean", "maximum"]
        ]
        add_values_to_table(table, [("name", benchmark_name)] + values)

    
