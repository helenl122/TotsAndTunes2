# Plot distribution from sampled means, comparing variables
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

## Set up Environment
data_folder = "comparison_analysis/sample_means/" # input
output_folder = "./results/comparison/" # output

# set colors for PNW speech main/sub, music main/sub
PNW_m1, PNW_m2, PNW_s1, PNW_s2 = "#010B96", "#8D96F8", "#2FA7C0", "#A9D4DE"
LAT_m1, LAT_m2, LAT_s1, LAT_s2 = "#960106", "#F88D90", "#FF9E07","#FFE2B5"

# Set up data
tt1_source = pd.read_csv(data_folder + "TT1 Source_sample.csv")
tt1_target = pd.read_csv(data_folder + "TT1 Target_sample.csv")
tt1_type = pd.read_csv(data_folder + "TT1 Type_sample.csv")
tt2_source = pd.read_csv(data_folder + "TT2 Source_sample.csv")
tt2_target = pd.read_csv(data_folder + "TT2 Target_sample.csv")
tt2_type = pd.read_csv(data_folder + "TT2 Type_sample.csv")

'''
Functions for plotting comparison histogram data of individual vars & across speech/music
'''
# Helper function for plot_distribution (create individual subplot of multiple vars)
def plot_sub(vars, df1, df2):
        for var in vars:
            # name in legend shorten (speech/music/device/person/baby/other), xlab either speech/music
            (xlab, v_name) = var.split("_") if var not in ["speech", "music"] else("", var)
            sns.histplot(df1[var], label="PNW "+v_name, alpha=0.5, element="step", kde=True)
            sns.histplot(df2[var], label="LAT/HSP "+v_name, alpha=0.5, element="step", kde=True)
            plt.legend()
        plt.xlabel(xlab + " counts")
        plt.ylabel("Number of counts")
# Plot comparison distribution of variables across speech/music or combine speech & music
def plot_hist(df1, df2, title):
    vars = list(df1.columns)
    n_cols, n_rows = len(vars)//2, 1
    plt.figure(figsize=(6*n_cols, 4*n_rows))    
    # for source & target: make 2 subplots
    if len(vars) > 2:
        sns.set_palette([PNW_m1, LAT_m1, PNW_m2, LAT_m2]) # music palette
        plt.subplot(n_rows, n_cols, 1)
        plot_sub(vars[:len(vars)//2], df1, df2)

        sns.set_palette([PNW_s1, LAT_s1, PNW_s2, LAT_s2]) # speech palette
        plt.subplot(n_rows, n_cols, 2)
        plot_sub(vars[len(vars)//2:], df1, df2)
    # for type: 1 plot
    else:
        sns.set_palette([PNW_m1, LAT_m1, PNW_s1, LAT_s1]) # speech vs music palette
        plt.subplot(n_rows, n_cols, 1)
        plot_sub(vars, df1, df2)
    
    # Set the figure legend with unique entries
    plt.suptitle(f"Histogram of {title} counts")
    plt.tight_layout(rect=[0, 0, 0.9, 1]) # leave space for legend
    plt.savefig(output_folder + title + "_hist.svg")
    plt.close()

'''
Call Functions & create plots
'''
plot_hist(tt1_source, tt2_source, "source")
plot_hist(tt1_target, tt2_target, "target")
plot_hist(tt1_type, tt2_type, "type")