# Compare the reasoning for coders for choosing YES (infant-directed) based on words, sound, or both
# should analyze whether this is related to type (speech, music)

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from tqdm import tqdm # progress bar

ftr_data = pd.read_csv("../Aggregation/results/filtered_classifications.csv")

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
'''

# for each T6 yes IDS (1 in T6_class: speech) and T10 yes IDM (1 in T10_class: music)
# look at PERCENTAGE distribution of reasons
def examine_yes(colName, fileName):
    output = []
    yes_data = ftr_data[ftr_data[colName]==1]
    for options in tqdm(yes_data[colName[:-6]]):
        # convert string array to array of ints
        options = options.replace(" ", "")[1:-1].split(".")
        options = [int(i) for i in options[:3]] # ["word", "sound", "both"] (0,1,2)
        # Add "both" option to individual option
        options[0] += options[2]
        options[1] += options[2]
        # compare which option majority decided
        if options[0] > options[1]: options[0], options[1] = 1,0 # more chose word
        elif options[0] < options[1]: options[0], options[1] = 0,1 # more chose wound
        else: options[0], options[1] = -1, -1 # tie b/n word & sound
        # add to row to output
        output.append(options[:2])
    res = pd.DataFrame(output, columns=["word", "sound"])
    res.to_csv("results/" + fileName + ".csv", index=False)

examine_yes("T6_class", "speech_yes_reasons")
examine_yes("T10_class", "music_yes_reasons")
