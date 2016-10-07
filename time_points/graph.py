import pandas as pd
import numpy
import matplotlib.pyplot as plt
import seaborn


file_name = 'time_points.csv'
df = pd.read_csv(file_name, delimiter = '\t')
# print df['Time']



clock_times = df['Clock'].values
hour_times = []
for index, time in enumerate(clock_times):
	if 'pm' in time.lower():
		newtime = time.replace('pm', '')
		newtime = newtime.replace('PM', '')
		newtime = newtime.replace(':', '.')
		t = float(newtime)
		if index == 0:
			t_0 = t
		
		hour_times.append((t - t_0) / 60.0)

# print hour_times
df['Hours'] = hour_times

fig, ax = plt.subplots()
ax.scatter(df['Hours'], numpy.log2(df['Control']), c = 'b')
best_fit_control = numpy.polyfit(df['Hours'], df['Control'], 1)
control_slope = best_fit_control[1]
control_intercept = best_fit_control[0]
control_line = control_slope * df['Hours']  + control_intercept
ax.plot(df['Hours'], control_line, c = 'b')

ax.scatter(df['Hours'], numpy.log2(df['50nm']), c = 'r')
ax.scatter(df['Hours'], numpy.log(df['100nm']), c = 'y')
ax.scatter(df['Hours'], numpy.log(df['200nm']), c = 'g')
ax.scatter(df['Hours'], numpy.log(df['400nm']), c = 'c')

plt.legend(loc = 2)
plt.xlabel('Hours')
plt.ylabel('ln(OD)')



# 1 / tau * ln(2)


plt.show()

# print clock_times




# df

# df = pd.read_csv(Location, names=['','Births'])
