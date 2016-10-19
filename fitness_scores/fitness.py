import pickle
import numpy as np
import scipy.stats

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

codon_AA_dict = pickle.load(open('translate.pkl', 'rb'))
pos_AAwt_dict = {}
for i in range(76):
	pos_AAwt_dict[i] = 'A'

# AAwt_pos_dict = pickle.load(open('aminotonumber.pkl', 'rb'))
# pos_AAwt_dict = dict((v,k) for k,v in AAwt_pos_dict.iteritems())
# print pos_AAwt_dict

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
data_dict_wildtype = {}
for f in filename_list:
	time_point = f.replace('_allele_count.pkl', '')
	current_dict = pickle.load(open(f, 'rb'))

	# print current_dict
	time_point_sum = sum(current_dict.values())
	for tup in current_dict:
		loc = tup[0]
		codon = tup[1]
		# print codon.replace('T','U')
		# print codon == 'WT'

		if codon != 'WT':
			RNA_codon = codon.replace('T','U')
			AA = codon_AA_dict[RNA_codon]
			is_WT = False
		else:
			AA = pos_AAwt_dict[loc]
			is_WT = True

		tup_AA = (loc, AA, is_WT)
		if tup_AA not in data_dict:
			data_dict[tup_AA] = {}
		data_dict[tup_AA][time_point] = np.log(5000.0 * (current_dict[tup] / float(time_point_sum)))
		
# print data_dict
for (loc, AA, is_WT) in data_dict:
	if is_WT:
		perturb_tups_r1 = []
		perturb_tups_r2 = []
		control_tups = []
		for time_point in data_dict[(loc, AA, is_WT)]:
			if time_point in generation_dict_perturb_r1:
				perturb_tups_r1.append((generation_dict_perturb_r1[time_point], data_dict[(loc, AA, is_WT)][time_point]))
			elif time_point in generation_dict_perturb_r2:
				perturb_tups_r2.append((generation_dict_perturb_r2[time_point], data_dict[(loc, AA, is_WT)][time_point]))
			elif time_point in generation_dict_control:
				control_tups.append((generation_dict_control[time_point], data_dict[(loc, AA, is_WT)][time_point]))

		perturb_tups_sorted_r1 = sorted(perturb_tups_r1, key = lambda tup: tup[0])
		perturb_tups_sorted_r2 = sorted(perturb_tups_r2, key = lambda tup: tup[0])
		control_tups_sorted = sorted(control_tups, key = lambda tup: tup[0])

		WT_x_control = [tup[0] for tup in control_tups_sorted]
		WT_y_control = [tup[1] for tup in control_tups_sorted]
		WT_x_r1 = [tup[0] for tup in perturb_tups_sorted_r1]
		WT_y_r1 = [tup[1] for tup in perturb_tups_sorted_r1]
		WT_x_r2 = [tup[0] for tup in perturb_tups_sorted_r2]
		WT_y_r2 = [tup[1] for tup in perturb_tups_sorted_r2]

		slope_r1_WT = np.polyfit(WT_x_r1, WT_y_r1, 1)[0]
		slope_r2_WT = np.polyfit(WT_x_r2, WT_y_r2, 1)[0]
		slope_control_WT = np.polyfit(WT_x_control, WT_y_control, 1)[0]


fitness_scores = []
for i in range(77):
	fitness_scores.append({})

for (loc, AA, is_WT) in data_dict:
	perturb_tups_r1 = []
	perturb_tups_r2 = []
	control_tups = []	
	for time_point in data_dict[(loc, AA, is_WT)]:
		if time_point in generation_dict_perturb_r1:
			perturb_tups_r1.append((generation_dict_perturb_r1[time_point], data_dict[(loc, AA, is_WT)][time_point]))
		elif time_point in generation_dict_perturb_r2:
			perturb_tups_r2.append((generation_dict_perturb_r2[time_point], data_dict[(loc, AA, is_WT)][time_point]))
		elif time_point in generation_dict_control:
			control_tups.append((generation_dict_control[time_point], data_dict[(loc, AA, is_WT)][time_point]))

	perturb_tups_sorted_r1 = sorted(perturb_tups_r1, key = lambda tup: tup[0])
	perturb_tups_sorted_r2 = sorted(perturb_tups_r2, key = lambda tup: tup[0])
	control_tups_sorted = sorted(control_tups, key = lambda tup: tup[0])
	min_len = np.amin([len(perturb_tups_r1), len(perturb_tups_r2), len(control_tups_sorted)])
	if min_len == 3:
		temp_x_control = [tup[0] for tup in control_tups_sorted]
		temp_y_control = [tup[1] for tup in control_tups_sorted]
		temp_x_r1 = [tup[0] for tup in perturb_tups_sorted_r1]
		temp_y_r1 = [tup[1] for tup in perturb_tups_sorted_r1]
		temp_x_r2 = [tup[0] for tup in perturb_tups_sorted_r2]
		temp_y_r2 = [tup[1] for tup in perturb_tups_sorted_r2]

		# temp_y_control = temp_y_control / WT_y_control
		# temp_y_r1 = temp_y_r1 / WT_y_r1
		# temp_y_r2 = temp_y_r2 / WT_y_r2



		# slope_r1 = np.polyfit(temp_x_r1, temp_y_r1, 1)[0]
		# slope_r2 = np.polyfit(temp_x_r2, temp_y_r2, 1)[0]
		# slope_control = np.polyfit(temp_x_control, temp_y_control, 1)[0]

		slope_r1, intercept_r1, r_value_r1, p_value_r1, std_err_r1 = scipy.stats.linregress(temp_x_r1, temp_y_r1)
		slope_r2, intercept_r2, r_value_r2, p_value_r2, std_err_r2  = scipy.stats.linregress(temp_x_r2, temp_y_r2)
		slope_control, intercept_control, r_value_control, p_value_control, std_err_control  = scipy.stats.linregress(temp_x_control, temp_y_control)

		std_err_avg = (std_err_r1 + std_err_r2) / 2.0

		fitness_r1 = slope_r1 - slope_r1_WT
		fitness_r2 = slope_r2 - slope_r2_WT
		fitness_control = slope_control - slope_control_WT
		fitness_average = (fitness_r1 + fitness_r2) / 2.0

		# print loc
		fitness_scores[loc - 1][AA] = (fitness_control, fitness_r1, fitness_r2, fitness_average, std_err_avg)

		# slope_dict[(loc, AA, is_WT)] = (slope_control, slope_r1, slope_r2)
		# r1_fitness = 
		# slope_dict[(loc, AA, is_WT)] = (float(slope_r1) / float(slope_control), float(slope_r2) / float(slope_control))


pickle.dump(fitness_scores, open( "fitness_scores.pkl", "wb"))

