import pickle
import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt
import sys

arg,arg1 = sys.argv
FILE = arg1
fitness_scores = pickle.load(open(FILE, 'r'))

# test_data = [{'A' : (0.1 , 0.1, 0.2, 0.15), 'V' : (0.4, 0.4, 0.5, 0.45)}, {'A' : (0.4, 0.2, 0.3, 0.25), 'V' : (0.4, 0.5, 0.6, 0.55)}]

averagefitnessdata_list = []

for position, aa_dict in enumerate(fitness_scores):
	
	averageposition_dict = {}
	print position
	print '----------------------------------------'
	for aa in aa_dict.keys():
		(fitness_control, fitness_r1, fitness_r2, fitness_average, std_err_avg) = aa_dict[aa]
		print aa, fitness_average
	print '----------------------------------------'
		
		
		# if position == 12 and aa == 'Y':
		# 	print fitness_average
		# 	print '----------------------------------------'


	# (fitness_control, fitness_r1, fitness_r2, fitness_average, std_err_avg) = fitness_scores[position][aa]
	# print fitness_average
	# averageposition_dict[aa] = value[3] - value[0]
	# averageposition_dict[aa] = value[3]


	# if position == 12 and aa == 'Y':
	# 	print '----------------------------------------'
	# 	print 'here'
	# 	# print value[3]
	# 	print '----------------------------------------'
	# averagefitnessdata_list.append(averageposition_dict)

	






# plt.figure(figsize=[20,8])
# sns.heatmap(pd.DataFrame(averagefitnessdata_list).T, cmap = plt.cm.seismic)
# plt.show()