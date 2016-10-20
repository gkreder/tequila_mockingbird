import pickle
import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt
import sys

# arg,arg1 = sys.argv
# FILE = arg1
FILE = 'fitness_scores.pkl'
fitness_scores = pickle.load(open(FILE, 'r'))

# test_data = [{'A' : (0.1 , 0.1, 0.2, 0.15), 'V' : (0.4, 0.4, 0.5, 0.45)}, {'A' : (0.4, 0.2, 0.3, 0.25), 'V' : (0.4, 0.5, 0.6, 0.55)}]

averagefitnessdata_list = []

for position in fitness_scores:
	averageposition_dict = {}
	for aa in position.keys():
		# value = position[aa]
		(fitness_control, fitness_r1, fitness_r2, fitness_average, std_err_avg) = position[aa]
		# averageposition_dict[aa] = value[3] - value[0]
		averageposition_dict[aa] = fitness_control
	averagefitnessdata_list.append(averageposition_dict)
plt.figure(figsize=[20,8])



df = pd.DataFrame(averagefitnessdata_list).T
pmask = df.isnull()
sns.set_style('dark')
sns.heatmap(df, cmap = plt.cm.seismic, mask = pmask)
plt.show()