# ------------------------------------------------------------------------
import cPickle as pic
import numpy
import seaborn as sns
import matplotlib.pyplot as plt
# ------------------------------------------------------------------------


# allele_data = pic.load(open('allele_dic_with_WT.pkl', 'rb'))
allele_data = pic.load(open('allele_dic.pkl', 'rb'))
aminotonumber_data = pic.load(open('aminotonumber.pkl', 'rb'))
translate_data = pic.load(open('translate.pkl', 'rb'))


# position_indices = numpy.linspace(0, 77, 78)
# barcode_counts = numpy.zeros(78)
# AA_counts = numpy.zeros(78)
positions = []

for barcode in allele_data:
	temp_list = allele_data[barcode][0].split('_')
	pos = temp_list[0]
	codon = temp_list[1]
	# # (pos, codon) = allele_data[barcode][0].split('_')
	positions.append(int(pos))
	# barcode_counts[pos] += 1

# print len(positions)
	
	# if pos == 76:
		# print pos

# min_positions = numpy.amin(positions)
# max_positions = numpy.amax(positions)
# print allele_data
# print(barcode_counts)
# print len(positions)
# print len(barcode_counts)
# print position_indices

# print set(translate_data.values())

# print positions
# ------------------------------------------------------------------------
# Plot # of barcodes mapped to each position
# ------------------------------------------------------------------------
f, ax = plt.subplots()
plt.hist(positions, bins = 76)
plt.xlabel('AA Position')
plt.ylabel('Barcode Counts')
xticks = numpy.linspace(1, 77, 77)
# print xticks
ax.set_xticks(xticks)
plt.show()
# ------------------------------------------------------------------------







# print allele_data
# print translate_data
# print aminotonumber_data