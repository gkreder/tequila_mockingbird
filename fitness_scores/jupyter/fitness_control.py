import fitness_lib
import pickle
import sys
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib as mpl
from operator import itemgetter

AMINOTONUMBER_DATA = pickle.load(open('./input_output_files/input/aminotonumber.pkl', 'rb'))
scriptname, replicate = sys.argv
file_name_perturb = './input_output_files/output/' + 'r1' + '_full_data.pkl'
file_name_control = './input_output_files/output/' + 'control' + '_full_data.pkl'
# ub_seq = 'MQIFVKTLTGKTITLEVESSDTIDNVKSKIQDKEGIPPDQQRLIFAGKQLEDGRTLSDYNIQKESTLHLVLRLRGG'
ub_seq = 'QIFVKTLTGKTITLEVESSDTIDNVKSKIQDKEGIPPDQQRLIFAGKQLEDGRTLSDYNIQKESTLHLVLRLRGG'
print len(ub_seq)


def plot_hmap(data, row_labels, column_labels):
    # sns.set(font_scale=0.7)
    sns.set(font_scale=1.0)

    grid_kws = {"height_ratios": (.9, .05), "hspace": .3}
    f, (ax, cbar_ax) = plt.subplots(2, gridspec_kw=grid_kws)
    ax = sns.heatmap(data, ax=ax,
                     cbar_ax=cbar_ax,
                     cbar_kws={"orientation": "horizontal"},
                     xticklabels=row_labels,
                     yticklabels=column_labels,
                     linewidths = 0.5)
    
    # mpl.rcParams.update({'font.size': 22})
    plt.sca(ax)
    plt.yticks(rotation=0)
    plt.xticks(rotation=90)
    # plt.title(replicate + ' Fitness Scores')
    plt.title('r1 - control Fitness Scores')
    plt.show()

def plot_scores_diff(AA_scores_perturb, AA_scores_control):
    locs = []
    # AAs_keys = AMINOTONUMBER_DATA.keys().
    AA_labels = [tup[0] for tup in sorted(AMINOTONUMBER_DATA.items(), key=itemgetter(1))]
    scores_perturb = []
    scores_control = []

    # numpy.zeros((21,77))
    scores = np.empty((21,75))
    scores[:] = np.NAN
    
    for (loc, AA) in AA_scores_perturb:
        print loc, AA
        if AA != 'WT' and loc > 1 and loc < 77:
            if (loc, AA) in AA_scores_perturb:
                perturb_score = AA_scores_perturb[(loc, AA)]['score']
            else:
                perturb_score = float('nan')

            if (loc, AA) in AA_scores_control:
                control_score = AA_scores_control[(loc, AA)]['score']
            else:
                control_score = float('nan')

            scores[int(AMINOTONUMBER_DATA[AA]), int(loc - 2)] = perturb_score - control_score
            locs.append(loc)

    # loc_labels = sorted(set(locs))
    ub_seq_list = list(ub_seq)
    for index, c in enumerate(ub_seq_list):
        ub_seq_list[index] = str(index + 2) + ' (' + c + ')'
    loc_labels = ub_seq_list
    plot_hmap(scores, loc_labels, AA_labels)





(AA_scores_perturb, total_reads_perturb, thrown_out_N_reads_perturb, thrown_out_dictionary_reads_perturb) = pickle.load(open(file_name_perturb, 'rb'))
(AA_scores_control, total_reads_control, thrown_out_N_reads_control, thrown_out_dictionary_reads_control) = pickle.load(open(file_name_control, 'rb'))
plot_scores_diff(AA_scores_perturb, AA_scores_control)









