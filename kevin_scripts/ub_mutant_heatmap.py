import pickle
import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt

fitness_scores = pickle.load(open('fitness_scores.pkl', 'r'))

# test_data = [{'A' : (0.1 , 0.1, 0.2, 0.15), 'V' : (0.4, 0.4, 0.5, 0.45)}, {'A' : (0.4, 0.2, 0.3, 0.25), 'V' : (0.4, 0.5, 0.6, 0.55)}]

averagefitnessdata_list = []

for position in fitness_scores:
	averageposition_dict = {}
	for aa in position.keys():
		value = position[aa]
		averageposition_dict[aa] = value[3] - value[0]
	averagefitnessdata_list.append(averageposition_dict)

sns.heatmap(pd.DataFrame(averagefitnessdata_list).T)
plt.show()