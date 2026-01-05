# For each counts file, pivot, i.e. collapse rows per subj
# then, sample n times, & take mean (m times) to form distribution
import pandas as pd
from statistics import mean
from tqdm import tqdm # progress bar

## Set up Environment
# input data folders
data_folder = "../Aggregation/results/"
tt1_type_path = data_folder + "TT1/tt1_type_counts.csv"
tt1_target_path = data_folder + "TT1/tt1_target_counts.csv"
tt1_source_path = data_folder + "TT1/tt1_source_counts.csv"
tt2_type_path = data_folder + "type_counts.csv"
tt2_target_path = data_folder + "target_counts.csv"
tt2_source_path = data_folder + "source_counts.csv"
# output data folders
pivot_folder = "pivot_counts/"
sample_folder = "comparison_analysis/sample_means/"

'''
Collapse rows
type_counts -> (subject_name | age | speech | music)
source_counts -> (subject_name | age | music_device | music_person | speech_device | speech_person)
source_counts -> (subject_name | age | music_baby | music_other | speech_baby | speech_other)
'''
def pivotCounts(count_df, type_cols, single=False):
    count_df = count_df.pivot_table(index=["subject_name", "age"], columns=type_cols, values="count").reset_index()
    if single: count_df.columns = [col.lower() for col in count_df.columns] # pivot based only on 1 var
    else: count_df.columns = ['_'.join(col).lower() if isinstance(col, tuple) and col[1] != "" else col[0] for col in count_df.columns]
    return count_df
# Read in data, drop "age_days", pivot, & add name
def setupData(path, cols, name, single=False):
    df = pivotCounts(pd.read_csv(path), cols, single=single)
    df.name = name
    df.to_csv(pivot_folder+name+"_pivot.csv", index=False) # save pivoted data to csv
    return df

# Set up data
pivot_cols = ["input_type", "input_source", "input_recipient"]
tt1_type = setupData(tt1_type_path, pivot_cols[0], "TT1 Type", single=True)
tt1_target = setupData(tt1_target_path, [pivot_cols[0],pivot_cols[2]], "TT1 Target")
tt1_source = setupData(tt1_source_path, pivot_cols[:2], "TT1 Source")
tt2_type = setupData(tt2_type_path, pivot_cols[0], "TT2 Type", single=True)
tt2_target = setupData(tt2_target_path, [pivot_cols[0],pivot_cols[2]], "TT2 Target")
tt2_source = setupData(tt2_source_path, pivot_cols[:2], "TT2 Source")

## Treat each sample as independent or w/n subject sample; m = times to sample n
def sample(df, within=False, n=24, m=1000):
    # create dictionary of col variables: [counts] that are number type var & not age
    cols = {c: [] for c in df.columns if pd.api.types.is_numeric_dtype(df[c]) and c != "age"}
    for _ in tqdm(range(m)):
        if within:
            output = []
            for s in df["subject_name"].unique(): # unique subjects
                options = df[df["subject_name"] == s]
                output.append(options.sample(1))
            sample = pd.concat(output).reset_index(drop=True)
        else: sample = df.sample(n=n, replace=True) # sample w/ replacement
        for c in cols: cols[c].append(mean(sample[c].values)) # add n samples to total
    # save sample means to csv
    pd.DataFrame.from_dict(cols).to_csv(sample_folder + df.name + "_sample.csv", index=False)

## Take samples for different variable counts
sample(tt1_type, within=True)
sample(tt1_target, within=True)
sample(tt1_source, within=True)
sample(tt2_type)
sample(tt2_target)
sample(tt2_source)