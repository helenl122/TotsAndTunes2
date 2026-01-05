# Plot distribution from sampled means, comparing variables
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

## Set up Environment
data_folder = "comparison_analysis/sample_means/" # input
output_folder = "./results/comparison/" # output
means_file = output_folder + "distribution_means.csv"
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
means = {}

'''
Functions for plotting comparison distributions of individual vars & across speech/music
'''
## Create subplots comparing each individual variable in 2 given dataframes
def plot_per_var(df1, df2, title):
    vars = list(df1.columns)
    n_cols = 2
    n_rows = len(vars) // n_cols
    plt.figure(figsize=(6*n_cols, 4*n_rows))
    for i, var in enumerate(vars):
        plt.subplot(n_rows, n_cols, i + 1)
        sns.kdeplot(df1[var], label="PNW", fill=True, alpha=0.5)
        sns.kdeplot(df2[var], label="LAT/HSP", fill=True, alpha=0.5)
        plt.title(f'Density of {var.replace("_", " and ")} counts')
    # Collect unique legend handles and labels
    handles, labels = plt.gca().get_legend_handles_labels()
    by_label = dict(zip(labels, handles))  # removes duplicates
    # Set the figure legend with unique entries
    plt.figlegend(by_label.values(), by_label.keys(), loc='outside right upper')
    plt.tight_layout(rect=[0, 0, 0.9, 1]) # leave space for legend
    plt.savefig(output_folder + title + ".svg")
    plt.close()

# Helper function for plot_distribution (create individual subplot of multiple vars)
def plot_sub(vars, df1, df2):
        for var in vars:
            # name in legend shorten (speech/music/device/person/baby/other), xlab either speech/music
            (xlab, v_name) = var.split("_") if var not in ["speech", "music"] else("", var)
            sns.kdeplot(df1[var], label="PNW "+v_name, fill=True, alpha=0.5)
            sns.kdeplot(df2[var], label="LAT/HSP "+v_name, fill=True, alpha=0.5)
            plt.legend()
            means["TT1 " + var] = df1[var].mean()
            means["TT2 " + var] = df2[var].mean()
        plt.xlabel(xlab + " counts")
# Plot comparison distribution of variables across speech/music or combine speech & music
def plot_distribution(df1, df2, title):
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
    plt.suptitle(f"Density of {title} counts")
    plt.tight_layout(rect=[0, 0, 0.9, 1]) # leave space for legend
    plt.savefig(output_folder + title + ".svg")
    plt.close()

'''
Call Functions & create plots
'''
plot_distribution(tt1_source, tt2_source, "source")
plot_distribution(tt1_target, tt2_target, "target")
plot_distribution(tt1_type, tt2_type, "type")

# save distribution means to csv file
pd.DataFrame(list(means.items()), columns=['Vars', 'Mean']).to_csv(means_file, index=False)
# pd.DataFrame.from_dict(means).to_csv(means_file, index=False)

# plotting out distributions per variable (into 4 plots)
# plot_per_var(tt1_type, tt2_type, "type_per_var")
# plot_per_var(tt1_source, tt2_source, "source_per_var")
# plot_per_var(tt1_target, tt2_target, "target_per_var")