import json
import matplotlib.pyplot as plt

def plot_and_save_and_show(title, file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)

    # Prepare figure for plotting histograms with standard scale
    fig_standard, axs_standard = plt.subplots((len(data) + 4) // 5, 5, figsize=(9, 2.2 * ((len(data) + 4) // 5)))
    axs_standard = axs_standard.flatten()

    # Prepare figure for plotting histograms with log scale
    fig_log, axs_log = plt.subplots((len(data) + 4) // 5, 5, figsize=(9, 2.2 * ((len(data) + 4) // 5)))
    axs_log = axs_log.flatten()

    # Process each state's data
    for index, (state, (length, array_A)) in enumerate(data.items()):
        first_15_elements = array_A[:15]
        
        # Plot with standard scale
        axs_standard[index].hist(range(15), weights=first_15_elements, bins=15, alpha=0.75)
        axs_standard[index].set_title(state)
        axs_standard[index].set_xlim([0, 14])
        axs_standard[index].set_xlabel('Index')
        axs_standard[index].set_ylabel('Counts')
        
        # Plot with log scale
        axs_log[index].hist(range(15), weights=first_15_elements, bins=15, alpha=0.75, log=True)
        axs_log[index].set_title(state)
        axs_log[index].set_xlim([0, 14])
        axs_log[index].set_xlabel('Index')
        axs_log[index].set_ylabel('Counts (log scale)')
        
        # Check for non-zero values beyond the first 15 elements
        non_zero_beyond_15 = [(i, val) for i, val in enumerate(array_A[15:], start=15) if val != 0]
        if non_zero_beyond_15:
            print(f"State {state} has non-zero values beyond index 15: {non_zero_beyond_15}")

    # Presentation Details 
    fig_standard.tight_layout()
    fig_log.tight_layout()
    fig_standard.subplots_adjust(top=0.9)  # Adjust the top to allow for suptitle
    fig_log.subplots_adjust(top=0.9)
    fig_standard.suptitle('Histograms with Standard Scale', va='bottom')
    fig_log.suptitle('Histograms with Log Scale', va='bottom')

    # Save Figure
    fig_standard.savefig(f"{title}_Face_Histogram_Stats.png")
    fig_log.savefig(f"{title}_LOG_Face_Histogram_Stats.png")

    # Show
    # fig_standard.show()
    # fig_log.show()
    # plt.show()

# Types
types = ["BG", "TRACT", "COUSUB", "COUNTY"]

# Load the JSON data from the file
for t in types:
    file_path = f"../../data/faces/{t}_face_stats.json"
    plot_and_save_and_show(t, file_path)