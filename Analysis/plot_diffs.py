## Plot graphs for vertical diff b/n counts of type, source, and target across age(days)
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from tqdm import tqdm # progress bar

## Read in count data
data_folder = "./pivot_counts/TT2 "
type_counts = pd.read_csv(data_folder + "Type_pivot.csv")
source_counts = pd.read_csv(data_folder + "Source_pivot.csv")
target_counts = pd.read_csv(data_folder + "Target_pivot.csv")

# Helper function to plot 1 subplot: scatter plots & vertical line of difference
def plot_subplots(ax, age, v1, v2, c, label1, label2):
    ax.scatter(age, v1, color=c[0], label=label1)
    sns.regplot(x=age, y=v1, color=c[0], ax=ax)
    ax.scatter(age, v2, color=c[1], label=label2)
    sns.regplot(x=age, y=v2, color=c[1], ax=ax)
    ax.vlines(x=age, ymin=v1, ymax=v2, color="gray", linestyle='dotted')
    ax.set_xlabel("Age (Days)")
    ax.set_ylabel("Count")
    ax.legend(loc="best", bbox_to_anchor=(1, 0.2))

## Create plot to show vertical difference b/n variants of speech and music
def plot_diffs(df, vars, title1, title2=None):
    fig, (ax1, ax2) = plt.subplots(2, figsize=(12, 10))
    colors = ["#960106", "#FF9E07", "#FF0108", "#FFE2B5"] # color palette
    ages = [a for a in df["age"]]
    v1 = [v for v in df[vars[0]]]
    v2 = [v for v in df[vars[1]]]
    # shorten labels e.g. speech_device -> device
    label1 = vars[0].split("_")[1] if len(vars) > 2 else vars[0]
    label2 = vars[1].split("_")[1] if len(vars) > 2 else vars[1]
    # only speech vs music in 1 graph: (red vs orange) else (red vs pink)
    plot1_colors = colors[:2] if len(vars) <= 2 else [colors[0], colors[2]]
    plot_subplots(ax1, ages, v1, v2, plot1_colors, label1, label2)
    ax1.set_title(title1)
    # 2 graphs: 1 for music (red vs pink), 1 for speech (orange vs light orange)
    if len(vars) > 2:
        v3 = [v for v in df[vars[2]]]
        v4 = [v for v in df[vars[3]]]
        # shorten labels e.g. speech_device -> device
        label3 = vars[2].split("_")[1]
        label4 = vars[3].split("_")[1]
        plot_subplots(ax2, ages, v3, v4, [colors[1], colors[3]], label3, label4)
        ax2.set_title(title2)
    else: fig.delaxes(ax2)
    plt.tight_layout(rect=[0, 0, 0.9, 1])
    plt.savefig("./results/"+vars[0]+".svg", bbox_inches='tight')

## Plot Differences for type, source, and target counts
plot_diffs(type_counts, ["music", "speech"], "Music vs Speech Input")

plot_diffs(source_counts, ["music_device", "music_person", "speech_device", "speech_person"], 
            "Music from Device vs Person", "Speech from Device vs Person")

plot_diffs(target_counts, ["music_baby", "music_other", "speech_baby", "speech_other"], 
            "Music for Baby vs Other", "Speech for Baby vs Other")
