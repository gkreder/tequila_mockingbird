import pickle
import numpy as np

# index_list = ['ATCAGT','GCTCAT','AGGAAT','CTTTTG','TAGTTG','CCGGTG','ATTCCG','AGCTAG','GTATAG']

# index_dict = {'ATCAGT': 't0_r1',
# 			  'GCTCAT': 't1_r1',
# 			  'AGGAAT': 't2_r1',
# 			  'CTTTTG':	't0_r2',
# 			  'TAGTTG': 't1_r2',
# 			  'CCGGTG':	't2_r2',
# 			  'ATTCCG': 't0_control',
# 			  'AGCTAG': 't1_control',
# 			  'GTATAG': 't2_control'}

generation_dict_perturb_r1 = {'t0_r1' : 0.0, 't1_r1' : 1.91, 't2_r1': 3.328354364}
generation_dict_perturb_r2 ={ 't0_r2' : 0.0, 't1_r2' : 1.35, 't2_r2' : 2.96}

generation_dict_control = {'t0_control' : 0.0, 't1_control' : 2.0, 't2_control': 4.0}

filename_list = ['t0_r1_allele_count.pkl',
				 't1_r1_allele_count.pkl',
 				 't2_r1_allele_count.pkl',
				 't0_r2_allele_count.pkl',
				 't1_r2_allele_count.pkl',
				 't2_r2_allele_count.pkl',
				 't0_control_allele_count.pkl',
				 't1_control_allele_count.pkl',
				 't2_control_allele_count.pkl']

data_dict = {}
for f in filename_list:
	time_point = f.replace('_allele_count.pkl', '')
	current_dict = pickle.load(open(f, 'rb'))

	# print current_dict
	time_point_sum = sum(current_dict.values())
	for tup in current_dict:
		if tup not in data_dict:
			data_dict[tup] = {}
		data_dict[tup][time_point] = np.log(5000.0 * (current_dict[tup] / float(time_point_sum)))
		

slope_dict_codon = {}
for index_tup in data_dict:
	perturb_tups_r1 = []
	perturb_tups_r2 = []
	control_tups = []	

	# x_vals_perturb = []
	# x_vals_control = []
	# y_vals_perturb = []
	# y_vals_control = []

	for time_point in data_dict[index_tup]:
		if time_point in generation_dict_perturb_r1:
			# x_vals_perturb.append(generation_dict_perturb[time_point])
			# y_vals_perturb.append(data_dict[tup][time_point])
			perturb_tups_r1.append((generation_dict_perturb_r1[time_point], data_dict[index_tup][time_point]))
		elif time_point in generation_dict_perturb_r2:
			# x_vals_perturb.append(generation_dict_perturb[time_point])
			# y_vals_perturb.append(data_dict[tup][time_point])
			perturb_tups_r2.append((generation_dict_perturb_r2[time_point], data_dict[index_tup][time_point]))
		elif time_point in generation_dict_control:
			# x_vals_control.append(generation_dict_control[time_point])
			# y_vals_control.append(data_dict[tup][time_point])
			control_tups.append((generation_dict_control[time_point], data_dict[index_tup][time_point]))

	
	perturb_tups_sorted_r1 = sorted(perturb_tups_r1, key = lambda tup: tup[0])
	perturb_tups_sorted_r2 = sorted(perturb_tups_r2, key = lambda tup: tup[0])
	control_tups_sorted = sorted(control_tups, key = lambda tup: tup[0])

	min_len = np.amin([len(perturb_tups_r1), len(perturb_tups_r2), len(control_tups_sorted)])
	if min_len == 3:
		
		# print perturb_tups_sorted_r1
		# print control_tups_sorted
		# print '------------------------'
		temp_x_control = [tup[0] for tup in control_tups_sorted]
		temp_y_control = [tup[1] for tup in control_tups_sorted]
		temp_x_r1 = [tup[0] for tup in perturb_tups_sorted_r1]
		temp_y_r1 = [tup[1] for tup in perturb_tups_sorted_r1]
		temp_x_r2 = [tup[0] for tup in perturb_tups_sorted_r2]
		temp_y_r2 = [tup[1] for tup in perturb_tups_sorted_r2]
		slope_r1 = np.polyfit(temp_x_r1, temp_y_r1, 1)[0]
		slope_r2 = np.polyfit(temp_x_r2, temp_y_r2, 1)[0]
		slope_control = np.polyfit(temp_x_control, temp_y_control, 1)[0]

		slope_dict_codon[index_tup] = (slope_control, slope_r1, slope_r2)
		# r1_fitness = 
		# slope_dict_codon[index_tup] = (float(slope_r1) / float(slope_control), float(slope_r2) / float(slope_control))	




print slope_dict_codon


