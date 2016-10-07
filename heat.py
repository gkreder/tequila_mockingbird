# ------------------------------------------------------------------------
import cPickle as pic
import numpy
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import operator
# ------------------------------------------------------------------------

# COUNT_DICT = {} 

# ------------------------------------------------------------------------

allele_data = pic.load(open('allele_dic.pkl', 'rb'))
aminotonumber_data = pic.load(open('aminotonumber.pkl', 'rb'))
translate_data = pic.load(open('translate.pkl', 'rb'))

data = numpy.zeros((21,77))

# print data
# print aminotonumber_data

# print allele_data

for barcode in allele_data:
	temp_list = allele_data[barcode][0].split('_')
	pos = temp_list[0]
	codon = temp_list[1]
	mrna_codon = codon.replace('T', 'U')
	AA = translate_data[mrna_codon]
	row_number = aminotonumber_data[AA]
	col_number = int(pos) - 1
	# if col_number > 75:
		# print col_number
	# print row_number

	data[row_number, col_number] += 1


# sns.heatmap(data)
# plt.show()

# print aminotonumber_data
# print aminotonumber_data.keys()
y_labels = []
sorted_aa_dict = sorted(aminotonumber_data.items(), key=operator.itemgetter(1))
for cod, index in sorted_aa_dict:
	y_labels.append(cod)

print y_labels
# print sorted_aa_dict


