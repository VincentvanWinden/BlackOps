# import relevant packages
# Numpy (maths and arrays)
# Csv (reading and writing csv files)
# to use them I call csv.[function] or np.[function]

import csv as csv
import numpy as np

# open the csv file with training records in a Python object
csv_file_object = csv.reader(open('../data/train.csv','rb'))


# next command to skip the header of the file
header = csv_file_object.next()
 
# data variable which is a list
data=[]	

# add each row of the file to the data list variable
for row in csv_file_object:
	data.append(row) 

# convert each item in the data list variable into an array
data = np.array(data)

# the size counts the elements in an array
# the sum sums up the elements in an array
number_passengers = np.size(data[0::,0].astype(np.float))
number_survived = np.sum(data[0::,0].astype(np.float))
proportion_survivors = number_survived / number_passengers

# built a survival reference table in which we can look up passenger survival attributes

# cut off the highest fares and maken them 39
fare_ceiling = 40
data[data[0::,8].astype(np.float) >= fare_ceiling, 8] = fare_ceiling-1.0
fare_bracket_size = 10
number_of_price_brackets = fare_ceiling / fare_bracket_size
number_of_classes = 3 # this is a given there were 1st, 2nd and 3rd classes

# define the survival table based on gender * classes * price_brackets
survival_table = np.zeros((2, number_of_classes, number_of_price_brackets))


for i in xrange(number_of_classes):
	for j in xrange(number_of_price_brackets):
		women_only_stats = 	data[	\
						(data[0::, 3] == "female") \
						&(data[0::,1].astype(np.float) == i+1) \
						&(data[0:,8].astype(np.float) >= j*fare_bracket_size) \
						&(data[0:,8].astype(np.float) < (j+1)*fare_bracket_size) \
					,0]
		men_only_stats = 	data[	\
						(data[0::, 3] != "female") \
						&(data[0::,1].astype(np.float) == i+1) \
						&(data[0:,8].astype(np.float) >= j*fare_bracket_size) \
						&(data[0:,8].astype(np.float) < (j+1)*fare_bracket_size) \
					,0]
		survival_table[0,i,j] = np.mean(women_only_stats.astype(np.float)) # women survival percentage
		survival_table[1,i,j] = np.mean(men_only_stats.astype(np.float)) # men survival percentage
		survival_table[ survival_table != survival_table ] = 0.
	

# survival in percentages
for i in xrange(number_of_classes):
	for j in xrange(number_of_price_brackets):
		jbottom = j * fare_bracket_size
		jtop = (j+1) * fare_bracket_size
		jstring = repr(jbottom) +  ' - ' + repr(jtop)
		print 'Class: ' + repr(i+1) + '\tPrice bracket: ' + jstring + '\tFemale Survivals:\t' + repr(survival_table[0,i,j])
		print 'Class: ' + repr(i+1) + '\tPrice bracket: ' + jstring + '\tMale Survivals:\t\t' + repr(survival_table[1,i,j])

print '\n\n'

survival_table[ survival_table < 0.5] = 0
survival_table[ survival_table >= 0.5] = 1

# survival in yes / no survival
for i in xrange(number_of_classes):
	for j in xrange(number_of_price_brackets):
		jbottom = j * fare_bracket_size
		jtop = (j+1) * fare_bracket_size
		jstring = repr(jbottom) +  ' - ' + repr(jtop)
		print 'Class: ' + repr(i+1) + '\tPrice bracket: ' + jstring + '\tFemale Survivals:\t' + repr(survival_table[0,i,j])
		print 'Class: ' + repr(i+1) + '\tPrice bracket: ' + jstring + '\tMale Survivals:\t\t' + repr(survival_table[1,i,j])

test_file_obect = csv.reader(open('../data/test.csv','rb'))
fname = '../data/output_gender_class_price_model_python.csv'
open_file_object = csv.writer(open(fname,'wb'))
header = test_file_obect.next()

for row in test_file_obect:
	for j in xrange(number_of_price_brackets):
		try:
			row[7] = float(row[7])
		except: # if we cannot bin the fare-price we bin according to class which is row[0]
			bin_fare = 3-float(row[0])
			break
		if row[7] > fare_ceiling:
			bin_fare = number_of_price_brackets-1
			break
		if row[7] >= j*fare_bracket_size and row[7] < (j+1)*fare_bracket_size:
			bin_fare = j
			break
	if row[2] == 'female':
		row.insert(0,int(survival_table[0, float(row[0])-1, bin_fare])) # doe lookup in survival table op [sex, class en fare)
	else:
		row.insert(0,int(survival_table[1, float(row[0])-1, bin_fare])) # doe lookup in survival table op [sex, class en fare)
	open_file_object.writerow(row)
	

