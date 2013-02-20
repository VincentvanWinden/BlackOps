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
# the sum sums ip the elements in an array
number_passengers = np.size(data[0::,0].astype(np.float))
number_survived = np.sum(data[0::,0].astype(np.float))
proportion_survivors = number_survived / number_passengers

women_only_stats = data[0::, 3] == "female"
men_only_stats = data[0::, 3] != "female"

women_onboard = data[women_only_stats, 0].astype(np.float)
men_onboard = data[men_only_stats, 0].astype(np.float) 

proportion_women_survived = np.sum(women_onboard) / np.size(women_onboard)
proportion_men_survived = np.sum(men_onboard) / np.size(men_onboard)

print 'Proportion of women who survived the Titanic disaster is %s' % proportion_women_survived
print 'Proportion of men who survived the Titanic disaster is %s' % proportion_men_survived

# open the testfile so we can start with our predictions
test_file_object = csv.reader(open('../data/test.csv','rb'))
header = test_file_object.next()

# open a output file for writing our predictions
open_file_object = csv.writer(open('../data/output_genderbasedmodel.csv','wb'))

for row in test_file_object:
	if row[2] == 'female':
		row.insert(0,'1')
	else:
		row.insert(0,'0')
	open_file_object.writerow(row)
		

