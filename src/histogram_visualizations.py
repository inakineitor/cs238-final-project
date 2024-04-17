import json

import matplotlib.pyplot as plt

def main():
    for map_type in  ["BLOCK", "BG", "TRACT", "COUSUB", "COUNTY"]:
        # Read the JSON file
        with open(f"do_not_commit/{map_type}_main_stats.json") as f:
            data = json.load(f)

        # key = benchmark name, value = list of values from all states, one value per state
        for benchmark_name, all_values in data.items():
            if benchmark_name in ["RadiusBenchmark", "DiameterBenchmark"]:
                values = [x for x in all_values if x != -1] # -1 encodes disconnected graph
                num_invalid = len(all_values) - len(values) # e.g. for radius and diameter, some maps are disconnected
                plt.hist(values)
                if num_invalid > 0:
                    plt.text(0.5, -0.1, f"Proportion of disconnected graphs: {num_invalid}/{len(all_values)}", transform=plt.gca().transAxes, ha='center')
            else:
                plt.hist(all_values)
            plt.title(benchmark_name)
            plt.savefig(f"../data/histograms/{benchmark_name}_{map_type}_realmaps.png")
            plt.close()

if __name__ == "__main__":
    main()