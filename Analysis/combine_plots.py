## Combine plot graphs for vertical diff & density graphs
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

## Read in count data
data_folder = "./pivot_counts/TT2 "
target_counts = pd.read_csv(data_folder + "Target_pivot.csv")
means_file =  "./results/comparison/distribution_means.csv"
# set colors for PNW speech main/sub, music main/sub
PNW_m1, PNW_m2, PNW_s1, PNW_s2 = "#010B96", "#8D96F8", "#2FA7C0", "#A9D4DE"
LAT_m1, LAT_m2, LAT_s1, LAT_s2 = "#960106", "#F88D90", "#FF9E07","#FFE2B5"
music_colors = [PNW_m1, LAT_m1, PNW_m2, LAT_m2] # music palette

data_folder = "comparison_analysis/sample_means/" # input
tt1_target = pd.read_csv(data_folder + "TT1 Target_sample.csv")
tt2_target = pd.read_csv(data_folder + "TT2 Target_sample.csv")
means = {}
replace = {"baby": "ID", "other": "Non-ID"}

# Plot density distribution comparing Latinx & Non-Latinx
def plot_dist(ax, df1, df2):
        vars = list(df1.columns)
        vars = vars[:len(vars)//2]
        curr_color = 0
        for var in vars:
            # name in legend shorten (speech/music/device/person/baby/other), xlab either speech/music
            (xlab, v_name) = var.split("_") if var not in ["speech", "music"] else("", var)
            v_name = replace[v_name] # e.g. change baby -> ID
            sns.kdeplot(df1[var], label="Non-Latinx "+v_name, fill=True, alpha=0.5, color=music_colors[curr_color])
            sns.kdeplot(df2[var], label="Latinx "+v_name, fill=True, alpha=0.5, color=music_colors[curr_color+1])
            curr_color += 2
            means["TT1 " + var] = df1[var].mean()
            means["TT2 " + var] = df2[var].mean()
        ax.legend()
        plt.xlabel(xlab + " counts")
    
# Plot scatter plots & vertical line of difference
def plot_diffs(ax, age, v1, v2, c, label1, label2):
    ax.scatter(age, v1, color=c[0], label=label1)
    sns.regplot(x=age, y=v1, color=c[0], ax=ax)
    ax.scatter(age, v2, color=c[1], label=label2)
    sns.regplot(x=age, y=v2, color=c[1], ax=ax)
    ax.vlines(x=age, ymin=v1, ymax=v2, color="gray", linestyle='dotted')
    ax.set_xlabel("Age (Days)")
    ax.set_ylabel("Count")
    ax.legend(loc="best", bbox_to_anchor=(1, 0.2))

## Create plot to show vertical difference b/n variants of speech and music
def plot_diffs_dist(df, vars, title1, title2=None):
    fig, (ax1, ax2) = plt.subplots(2, figsize=(12, 10))
    colors = ["#960106", "#FF9E07", "#FF0108", "#FFE2B5"] # color palette
    ages = [a for a in df["age"]]
    v1 = [v for v in df[vars[0]]]
    v2 = [v for v in df[vars[1]]]
    # shorten labels e.g. speech_device -> device
    label1 = "ID"
    label2 = "Non-ID"
    # only speech vs music in 1 graph: (red vs orange) else (red vs pink)
    plot1_colors = [colors[0], colors[2]]
    plot_diffs(ax1, ages, v1, v2, plot1_colors, label1, label2)
    ax1.set_title(title1)
    plot_dist(ax2, tt1_target, tt2_target)
    ax2.set_title(title2)
    plt.tight_layout(rect=[0, 0, 0.9, 1])
    plt.savefig("./results/combined.svg", bbox_inches='tight')


## Plot Differences for type, source, and target counts
plot_diffs_dist(target_counts, ["music_baby", "music_other"], 
            "Latinx: ID vs Non-ID Music", "Latinx vs Non-Latinx Music")
