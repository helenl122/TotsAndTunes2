# Code takes direct classification data from Zooniverse and flattens them into answer vectors per task
### Import libraries
import pandas as pd
import numpy as np
import os, json
from tqdm import tqdm # progress bar

'''
LEGEND:
T0 = What do you hear in this clip?
T2 = What type of speech do you hear?
T3 = What type of music do you hear?
T6 = Is the speech directed to a baby?
T7 = [Speech] What type of speech do you hear? (if T0: both speech & music)
T8 = [Music] What type of music do you hear? (if T0: both speech & music)
T9 = Is it directed to a baby (if T0: only speech OR only music)
T10 = Is the music directed to a baby?

sbj = subject
clf = classification
flt = flat
wkf = workflow
'''

### Initialize environment variables
# download subject set & workflow classification csv straight from Zooniverse
cur_dir = "." # CHANGE THIS DEPENDING ON LOCATION
sbj_file = "tots-and-tunes-subjects.csv"
clf_file = "tots-tunes-2-0-workflow-classifications.csv"
# set desired subject set/workflow ids & output filename
set_id = 120935
wkf_ver = 96.113
flt_file = "results/flattened_classifications.csv"
# set vectors according to answer response options
# np.eye(n, m, index) = one hot n x m array e.g. (1,4,0) = [1,0,0,0]
vectors = {
    "Speech produced by someone older than 2": np.eye(1,4,k=0),
    "Music or singing": np.eye(1,4,k=1),
    "Speech produced by someone older than 2 AND music/singing": np.eye(1,4,k=2),
    "None of the above": np.eye(1,4,k=3),
    "In-person speech": np.eye(1,3,k=0),
    "Speech through an electronic device": np.eye(1,3,k=1),
    "Both of these": np.eye(1,3,k=2),
    "In-person music or singing": np.eye(1,3,k=0),
    "Music through an electronic device": np.eye(1,3,k=1),
    "Yes, based on the words": np.eye(1,4,k=0),
    "Yes, based on how it sounds": np.eye(1,4,k=1),
    "Yes, based on both the words & how it sounds": np.eye(1,4,k=2),
    "No": np.eye(1,4,k=3)
}

### Read in subject set & classification files
os.chdir(cur_dir)
sbj_data = pd.read_csv(sbj_file)
sbj_data = sbj_data[sbj_data["subject_set_id"] == set_id]
clf_data = pd.read_csv(clf_file)
clf_data = clf_data[clf_data["workflow_version"] == wkf_ver]

### For each classification row: flatten JSON
# convert JSON string to JSON object dictionary
# normalize JSON object to row w/ tasks as column headings
# drop question, only keep answer & merge T7>T2, T8>T3, T9+speech>T6, T9+music>T10
# add in classification id for easy merging later
rows = []
for i, json_str in enumerate(tqdm(clf_data['annotations'])):
    json_obj = json.loads(json_str)
    row = pd.json_normalize(json_obj).set_index('task').T
    row.drop('task_label', inplace=True)
    if 'T7' in row.columns: row.rename(columns={'T7': 'T2'}, inplace=True)
    if 'T8' in row.columns: row.rename(columns={'T8': 'T3'}, inplace=True)
    if 'T9' in row.columns:
        value = row['T0']['value']
        if value == "Music or singing": row.rename(columns={'T9': 'T10'}, inplace=True)
        else: row.rename(columns={'T9': 'T6'}, inplace=True)
    row.rename(index={"value": clf_data['classification_id'].iloc[i]}, inplace=True)
    row.index.names=['classification_id']
    rows.append(row)


### Convert rows to dataframe & export
# replace text answers w/vector if non-null; else replace w/0
rows_data = pd.concat(rows)
rows_data = rows_data.map(lambda v: vectors.get(v).tolist() if v in vectors else v)
rows_data.fillna(0, inplace=True)

flt_data = pd.merge(clf_data, rows_data, on="classification_id")
flt_data.to_csv(flt_file, index=False)