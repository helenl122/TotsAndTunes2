# Plot counts of type, source, and recipient
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Set up environment variabless
data_folder = "./pivot_counts/TT2 "
drop_cols = ["subject_name", "age"]
fig, axes = plt.subplots(1,3,sharey=True)

# helper function for subplots
def plot_counts(path, i, title):
    df = pd.read_csv(path)
    df.drop(drop_cols, axis=1, inplace=True)
    # sns.boxplot(data=[df[cols] for cols in list(df.columns)], ax=axes[i]).set(title=title)
    sns.violinplot(data=[df[cols] for cols in list(df.columns)], ax=axes[i]).set(title=title)
    axes[i].tick_params(axis='x', rotation=45)  # rotate x-axis labels
    
# plot type, source, & target counts; export
plot_counts(data_folder + "Type_pivot.csv", 0, "Type Counts")
plot_counts(data_folder + "Source_pivot.csv", 1, "Source Counts")
plot_counts(data_folder + "Target_pivot.csv", 2, "Target Counts")
plt.tight_layout()
plt.savefig("./results/counts.svg")
