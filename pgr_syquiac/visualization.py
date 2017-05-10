'''
Pauline Ramirez & Carlos Syquia

'''
import matplotlib.pyplot as plt
import numpy as np

# Average distance to hospital and the correlation coefficient of distance & rate of checkup

distance = np.arange(0.25, 5.25, 0.25)

corrs1 = [-0.0205161663643, 0.227578094728, 0.265153530461, 0.213774834125, 0.251720389634, \
		0.216096387764, 0.174904892898, 0.0461452124291, -0.0638549317789, -0.134122159266, \
		-0.134122159266, -0.134122159266, -0.134122159266, -0.126742665016, -0.143234368051, \
		-0.143234368051, -0.139380162789, -0.139380162789, -0.139380162789, -0.139380162789]

bar_width = 0.25
plt.figure(figsize=(10,6))
plt.bar(distance, corrs1, bar_width, edgecolor='black', align='center', color='blue')


plt.ylabel('Correlation Coefficient')
plt.xlabel('Distance in Miles')

plt.show()


# corrs2 = [-0.37044742301, -0.370335432693, -0.258417057261, -0.195759861625, -0.136465899632, \
# 		-0.119460338958, -0.111505946893, -0.127920694846, -0.121753023948, -0.137551289412, \
# 		-0.149172834419, ]