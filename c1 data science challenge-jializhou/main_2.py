import os
import pandas as pd

def read_txt(path):
	frames = pd.DataFrame()
	for file in os.listdir(path):
	    if file.endswith(".TXT"):	    	
	    	file = os.path.join(path,file)
	        frames = frames.append(pd.read_csv(file, sep = ',', header=None))
	frames.columns=['State', 'Gender', 'Year', 'Name', 'Count']
	return frames

# 2.  What is the most popular name of all time? (Of either gender.)
def most_popular_name(data,gender):
	names = data[data['Gender'] == gender]
	names['Sum'] = names.groupby('Name')['Count'].transform(sum)
	names.drop_duplicates(subset = ['Name'], inplace = True)
	return names.loc[names['Sum'].idxmax(),:]

#3.  the most gender ambiguous name in 2013? 1945?
def ambiguous_name(year, data):    
	#get the data of 2013 / 1945
    names = data[data['Year'] == year]
    #sum by gender
    names['Sum_gender'] = names.groupby(['Name','Gender'])['Count'].transform(sum)
    #overall sum (both genders)
    names['Sum'] = names.groupby('Name')['Count'].transform(sum)
    #percent = |count(Female or Male)/count(Female and Male) - 0.5|
    names["Percent"] = abs((0.0 + names["Sum_gender"]) / names["Sum"] -0.5)
    names = names.reset_index(drop = True)
    names = names.sort('Percent', ascending = True)
    header = names.head(1)
    return header

#4.  Of the names represented in the data, find the name that has had the largest 
#    percentage increase in popularity since 1980. Largest decrease?


def find_largest_increase_or_decrease(data, year1, year2):
	names = data[data["Year"] >= year1]
	names['Count_by_year'] = names.groupby(['Name','Year'])['Count'].transform(sum)
	names.drop_duplicates(subset = ['Name', 'Year'], inplace = True)
	
	helper = names.groupby(['Name']).apply(pd.DataFrame.sort, 'Year')['Count_by_year']
	helper = helper.reset_index()
	t = helper.groupby('Name').first()
	t['Year2'] = helper.groupby('Name').last()['Count_by_year']
	t['Change'] = t['Year2'] - t['Count_by_year']
	t = t.sort('Change', ascending = True)
	header = t.head(1)
	tailer = t.tail(1)
	return header, tailer

def prob_largest_increase_or_decrease(data, year1, year2):
	names = data[data["Year"] >= year1]
	names['Count_by_year'] = names.groupby(['Name','Year'])['Count'].transform(sum)
	names.drop_duplicates(subset = ['Name', 'Year'], inplace = True)
	
	helper = names.groupby(['Name']).apply(pd.DataFrame.sort, 'Year')['Count_by_year']
	helper = helper.reset_index()
	t = helper.groupby('Name').nth(-2)
	t['Year2'] = helper.groupby('Name').last()['Count_by_year']
	t['Change'] = t['Year2'] - t['Count_by_year']
	t = t.sort('Change', ascending = True)
	header = t.head(1)
	tailer = t.tail(1)
	return header, tailer

def main():
	path = "namesbystate"
	data_all = read_txt(path)
	print most_popular_name(data_all, 'F')
	# from results we can find that the most popular name of all times of Female is Mary
	print most_popular_name(data_all, 'M')
	# from results we can find that the most popular name of all times of Male is James.

	result = ambiguous_name(2013, data_all)
	print result
	#from result, we can find that the most ambiguous name in 2013 is Nikita, Cree and Sonam

	result = ambiguous_name(1945, data_all)
	print result
	#from result, we can find that the most ambiguous name in 1945 is Maxie.

	result = find_largest_increase_or_decrease(data_all, 1980, 2014)
	print result
	#from result, we can find that the name that has had the largest 
	#    percentage increase in popularity is Emma
	#    and the largest percentage decrease in popularity is Jennifer.

	result = prob_largest_increase_or_decrease(data_all, 1980, 2014)
	print result
	# print result
	#from result, we can find that the name that will probably have the largest 
	#    percentage increase in popularity is Oliver
	#    and will probably have the largest percentage decrease in popularity is Sophia.

if __name__ == "__main__":
    main()






