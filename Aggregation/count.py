# Counts filtered classification task answers for type, src, and infant directed per infant subject (excl. -1 unresolved)
### Import Libraries
import pandas as pd
import json
from tqdm import tqdm # progress bar

'''
T0_class (type)
0 = Speech
1 = Music
2 = Both
3 = None
-1 = unresolved

T2_class (speech src) / T3_class (music src)
0 = person
1 = electronic
2 = both
-1 = unresolved

T6_class (speech target) / T10_class (music target)
0 = no
1 = yes
-1 = unresolved
'''

### Initialize environment variables
set_id = 120935
inputTypes = ['Speech', 'Music']
inputSources = ['Person', 'Device']
inputTargets = ['Other', 'Baby']
# Filenames used
sbj_file = "tots-and-tunes-subjects.csv"
age_file = "subject-ages.csv"
ftr_file = "results/filtered_classifications.csv"
type_file = "results/type_counts.csv" # output file
src_file = "results/source_counts.csv" # output file
target_file = "results/target_counts.csv" # output file
snippet_file = "results/snippet_counts.csv" # output file
unres_file = "results/unresolved_counts.csv" # output file

### Set up necessary Data frames
# read in audio subject set & filtered dataframe (for subject name, i.e. EILD/WBH)
# combine classifications w/ subject set data
sbj_data = pd.read_csv(sbj_file)
sbj_data = sbj_data[sbj_data["subject_set_id"] == set_id]
ftr_data = pd.read_csv(ftr_file)
clf_data = pd.merge(sbj_data, ftr_data, on="subject_id")

# read in infant subject name & age data to dataframe
# 1) create type dataframe: ea. sbj has "speech" & "music" rows
type_data = pd.read_csv(age_file)
type_data['input_type'] = [inputTypes] * len(type_data)
type_data = type_data.explode('input_type', ignore_index=True)
type_data['count'] = 0

# 2) create source dataframe:
# ea. sbj has 1)"speech & person", 2)"speech & device", 3)"music & person", 4)"music & device" rows
src_data = type_data.copy()
src_data['input_source'] = [inputSources] * len(src_data)
src_data = src_data.explode('input_source', ignore_index=True)

# 3) create target recipient dataframe:
# ea. sbj has 1)"speech & not infant directed", 2)"speech & yes", 3)"music & no", 4)"music & yes" rows
target_data = type_data.copy()
target_data['input_recipient'] = [inputTargets] * len(target_data)
target_data = target_data.explode('input_recipient', ignore_index=True)

# counting how many snippets retired for each infant subject (complete=100)
snippet_data = pd.read_csv(age_file)
snippet_data['count'] = 0

### Increment Helper Functions
def increment_type(name, input_type):
    type_data.loc[(type_data['subject_name'] == name) & (type_data['input_type'] == input_type), ['count']] += 1

def increment_src(name, input_type, input_source):
    src_data.loc[(src_data['subject_name'] == name) & (src_data['input_type'] == input_type)
                  & (src_data['input_source'] == input_source), ['count']] += 1

def increment_target(name, input_type, input_recipient):
    target_data.loc[(target_data['subject_name'] == name) & (target_data['input_type'] == input_type)
                  & (target_data['input_recipient'] == input_recipient), ['count']] += 1

### Increment Function for counting up snippets
def increment(name, input_type, taskA_name, taskB_name):
    increment_type(name, input_type)
    taskA = clf_data.iloc[i][taskA_name] # t2 or t3
    if taskA in [0,2]: increment_src(name, input_type, inputSources[0])
    if taskA in [1,2]: increment_src(name, input_type, inputSources[1])
    taskB = clf_data.iloc[i][taskB_name] # t6 or t10
    if taskB == 0: increment_target(name, input_type, inputTargets[0])
    if taskB == 1: increment_target(name, input_type, inputTargets[1])

### For each classification row: add to type, src, and target dataframe counts
for i, json_str in enumerate(tqdm(clf_data['metadata'])):
    json_obj = json.loads(json_str)
    name = json_obj["#Audio Snippet"][:8].replace("_", "") # extract snippet's subject_name
    snippet_data.loc[(snippet_data['subject_name'] == name), ['count']] += 1
    t0 = clf_data.iloc[i]["T0_class"]
    if t0 in [0,2]: increment(name, inputTypes[0], "T2_class", "T6_class")
    if t0 in [1,2]: increment(name, inputTypes[1], "T3_class", "T10_class")

### Save count dataframes to csv files
type_data.to_csv(type_file, index=False)
src_data.to_csv(src_file, index=False)
target_data.to_csv(target_file, index=False)
snippet_data.to_csv(snippet_file, index=False) # file for num snippets counted per sbj    

### Count unresolved for T0 type, T2 speech src, T3 music src, T6 speech target, T10 music target
unresolved = {}
for t in ['T0_class', 'T2_class', 'T3_class', 'T6_class', 'T10_class']:
    col_name = t[:-5]+'count'
    count = (ftr_data[t] == -1).sum()
    total = ftr_data[t].count()
    unresolved[col_name] = [count, count/total]
unres_df = pd.DataFrame.from_dict(unresolved)
unres_df = pd.pivot_table(unres_df, columns=[0,1])
unres_df.rename(columns={0: 'Count', 1: 'Percentage'}, inplace=True)
# save to file
unres_df.to_csv(unres_file, index=True)
