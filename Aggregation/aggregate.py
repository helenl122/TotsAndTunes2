# Code takes flattened classification data and aggregates answer vectors per subject (snippet recording)
### Import libraries
import pandas as pd
import numpy as np
from tqdm import tqdm # progress bar

''''
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
agg = aggregation
ret = retirement
wkf = workflow
col = columns
'''

### Initialize environment variables
sbj_file = "tots-and-tunes-subjects.csv"
flt_file = "results/flattened_classifications.csv"
set_id = 120935
ret_count = 3
agg_file = "results/aggregated_classifications.csv" # output file

### Read in subject set & flattened classification files
sbj_data = pd.read_csv(sbj_file)
sbj_data = sbj_data[sbj_data["subject_set_id"] == set_id]
flt_data = pd.read_csv(flt_file)

### Aggregate counts by subject, matching using subject id
col_list = ['T0', 'T2', 'T3', 'T6', 'T10']
agg_rows = []
for subject in tqdm(sbj_data["subject_id"]):
    row = [subject]
    # check if there are any classifications for it
    sbj_clf = flt_data[flt_data["subject_ids"] == subject]
    if sbj_clf.empty: continue
    for task in col_list:
        total = 0
        for v in sbj_clf[task]:
            # create count vector according to task's answer options (4 vs 3)
            # adds arrays together, created from string."[0,1,0,0]"->[0,1,0,0]; [0,1,0,0]+[1,0,0,0]=>[1,1,0,0]
            if task in ['T0', 'T6', 'T10']:
                total += np.fromstring(v[2:-2], sep=",") if v!='0' else np.zeros(4)
            else:
                total += np.fromstring(v[2:-2], sep=",") if v!='0' else np.zeros(3)
        row.append(total)
    agg_rows.append(row)

### Export aggregated data to file
agg_data = pd.DataFrame(agg_rows, columns=['subject_id'] + col_list)
agg_data.to_csv(agg_file, index=False)