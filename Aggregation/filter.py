# Code goes through retired aggregated answer vectors per classification to "choose" final answer option per task
### Import Libraries
import pandas as pd
import numpy as np
from tqdm import tqdm # progress bar
'''
LEGEND:
T0 = What do you hear in this clip?
[0,0,0,0]
 0,1,2,3
0 = speech -> T2
1 = music -> T3
2 = both -> T2,T3
3 = None
-1 = unresolved

T2(/7) = What type of *speech* do you hear? -> T6
T3(/8) = What type of *music* do you hear? -> T10
[0,0,0]
 0,1,2
0 = person
1 = electronic
2 = both
-1 = unresolved

T6(/9+speech) = Is the *speech* directed to a baby?
T10(/9+music) = Is the *music* directed to a baby?
[0,0,0,0]
 0,1,2,3
0 = yes based on words > Y
1 = yes based on how it sounds > Y
2 = yes based on both > Y
3 = no > N
**NOTATION DIFFERENCE**
Use 0 = NO
Use 1 = YES
-1 = unresolved

sbj = subject
agg = aggregation
ftr = filter
col = columns
ret = retired
'''

### Initialize environment variables
sbj_file = "tots-and-tunes-subjects.csv"
agg_file = "results/aggregated_classifications.csv"
ftr_file = "results/filtered_classifications.csv" # output file
set_id = 120935
max_retire_count = 7
majority = max_retire_count // 2
both_idx = 3 # index of "both" option in audio type question

# read in subject set dataframe
sbj_data = pd.read_csv(sbj_file)
sbj_data = sbj_data[sbj_data["subject_set_id"] == set_id]

# read in aggregated counts csv file
agg_data = pd.read_csv(agg_file)

# filter only the retired snippets & combine w/ aggregated counts
ret_data = sbj_data[(sbj_data["retirement_reason"] == "other") | (sbj_data["retirement_reason"] == "classification_count")]
ret_data = pd.merge(agg_data, ret_data, on='subject_id')

'''
### FILTERING
className: task/col name
silenceOption: value to assign if audio type is "None"
filtered: list to append filtered rows to
binary: boolean; whether this task answers are Y/N only
1st pass: get max (NO TIES ALLOWED) & check if >50%
-- if Y/N option, compare total "yes" to "no" count
2nd pass: choose max vote option (but not tied)
3rd pass: if no max: add "both" count to speech & music individually, get max
4th pass: assign unresolved value (-1)
'''
def filter(className, silenceOption, filtered, binary):
    for sbj in ret_data["subject_id"]:
        row = [sbj]
        reason = ret_data.loc[ret_data['subject_id'] == sbj, 'retirement_reason'].iloc[0] 
        # T0 early retirement (="other"); set as index number "None" represents
        if reason == "other": row.append(silenceOption)
        else:
            response_str = ret_data.loc[ret_data['subject_id'] == sbj, className[:-6]].iloc[0]
            response_vector = np.fromstring(response_str[1:-1], dtype=int, sep=". ")
            # 1st pass on non-binary tasks
            if not binary:
                maxIndex = response_vector.argmax()
                maxValue = response_vector[maxIndex]
                if maxValue > majority: row.append(maxIndex)
                else:
                    duplicates = np.count_nonzero(response_vector == maxValue)
                    if duplicates < 2: row.append(maxIndex) # 2nd pass
                    else: # 3rd pass
                        response_vector[0] += response_vector[2]
                        response_vector[1] += response_vector[2]
                        maxIndex = response_vector.argmax()
                        maxValue = response_vector[maxIndex]
                        duplicate = np.count_nonzero(response_vector == maxValue)
                        if duplicate < 2: row.append(maxIndex)
                        else: row.append(-1) # Unresolved
            else: # binary tasks
                yes = sum(response_vector[:-1])
                no = response_vector[-1]
                if yes > no: row.append(1)
                elif no > yes: row.append(0)
                else: row.append(-1) # Unresolved
        filtered.append(row)
    
    ftr_data = pd.DataFrame(filtered, columns=['subject_id', className])
    merged_data =  pd.merge(agg_data, ftr_data, on='subject_id')
    return merged_data

### RUN FILTERING ON DATA
new_cols = ["T0_class", "T2_class", "T3_class"]
binary_cols = ["T6_class", "T10_class"]
new_data = []
for col in tqdm(new_cols):
    filtered = []
    if col == "T0_class": new_data.append(filter(col, both_idx, filtered, False))
    else: new_data.append(filter(col, None, filtered, False))
for col in tqdm(binary_cols):
    filtered = []
    new_data.append(filter(col, None, filtered, True))
ftr_data = pd.concat(new_data, axis=1)


### Clean up data & save export to csv file
# Remove duplicate columns due to appending & clear classifications for sbj not early retired but still "None"
# Don't include music task answers for speech & vice versa
ftr_data = ftr_data.loc[:,~ftr_data.columns.duplicated()].copy()
ftr_data.loc[ftr_data['T0_class'] == 3, ['T2_class', 'T3_class', 'T6_class', 'T10_class']] = [None]*4
ftr_data.loc[ftr_data['T0_class'] == 0, ['T3_class', 'T10_class']] = [None]*2
ftr_data.loc[ftr_data['T0_class'] == 1, ['T2_class', 'T6_class']] = [None]*2
ftr_data.to_csv(ftr_file, index=False)