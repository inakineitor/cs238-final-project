import json

import matplotlib.pyplot as plt
from matplotlib.ticker import PercentFormatter


def main():
    # Generate histograms for main stats
    # ["BLOCK", "BG", "TRACT", "COUSUB", "COUNTY"]
    for map_type in []:
        # Read the JSON file
        with open(f"do_not_commit/{map_type}_main_stats.json") as f:
            data = json.load(f)

        # key = benchmark name, value = list of values from all states, one value per state
        for benchmark_name, all_values in data.items():
            if benchmark_name in ["RadiusBenchmark", "DiameterBenchmark"]:
                values = [
                    x for x in all_values if x != -1
                ]  # -1 encodes disconnected graph
                num_invalid = len(all_values) - len(
                    values
                )  # e.g. for radius and diameter, some maps are disconnected
                plt.hist(values)
                if num_invalid > 0:
                    plt.text(
                        0.5,
                        -0.1,
                        f"Proportion of disconnected graphs: {num_invalid}/{len(all_values)}",
                        transform=plt.gca().transAxes,
                        ha="center",
                    )
            else:
                plt.hist(all_values)
            plt.title(benchmark_name)
            plt.savefig(f"../data/histograms/{map_type}_{benchmark_name}_realmaps.png")
            plt.close()

    # Generate histograms for face stats
    for map_type in ["BG", "TRACT", "COUSUB", "COUNTY"]:  # "BLOCK" also
        with open(f"do_not_commit/{map_type}_face_stats.json") as f:
            data = json.load(
                f
            )  # {state name: [number of total faces, [faces with 1 side, 2 sides, 3 sides, ...]]}

        face_stats = [0 for i in range(500)]
        for _, face_data in data.items():
            num_faces, face_sides = face_data[0], face_data[1]
            # remember: external face has largest total number of faces! remove it from each state
            for j in range(499, -1, -1):
                if face_sides[j] > 0:
                    face_sides[j] -= 1
                    break
            num_faces -= 1
            for j in range(500):
                face_stats[j] += face_sides[j]

        # face_stats has combined (for all states) data: [number of faces with 1 side, 2 sides, 3 sides, ...]
        max_display_face_size = 8
        plt.hist(
            range(1, max_display_face_size + 1),
            bins=max_display_face_size,
            weights=[
                face_stats[j] / sum(face_stats) for j in range(max_display_face_size)
            ],
        )
        plt.title("Face Sides")
        largest_face_size = max([j for j in range(500) if face_stats[j] > 0]) + 1
        plt.text(
            0.5,
            -0.1,
            f"Percentage of faces not depicted: {round(sum(face_stats[max_display_face_size:]) / sum(face_stats), 4) * 100}%; Largest face number of sides: {largest_face_size}",
            transform=plt.gca().transAxes,
            ha="center",
        )
        plt.gca().yaxis.set_major_formatter(PercentFormatter(1))
        plt.savefig(f"../data/histograms/{map_type}_faces_realmaps.png")
        plt.close()


if __name__ == "__main__":
    main()
