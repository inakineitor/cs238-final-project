import json

import matplotlib.pyplot as plt

def main():
    # ["BLOCK"]
    for map_type in ["BG", "TRACT", "COUSUB", "COUNTY"]:
        # Read the JSON file
        with open(f"do_not_commit/{map_type}_main_stats.json") as f:
            data = json.load(f)

        # key = benchmark name, value = list of values from all states, one value per state
        for key, value in data.items():
            # Create a histogram for each list value
            plt.hist(value)
            plt.title(key)
            plt.savefig(f"../data/histograms/{key}_{map_type}_realmaps.png")
            plt.close()

if __name__ == "__main__":
    main()