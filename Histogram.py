import Dataframe
import collections
import matplotlib.pyplot as plt

def get_histogram(df, columns = None):
	
	"""
	shape = df.shape
	columns = df.columns
	dtypes = df.dtypes
	print(shape, columns, dtypes)
	"""

	all_column_names = df.columns
	allow_columns = {}
	index = 0
	for col in all_column_names:
		col_type = type(df.values[0, index])
		if col_type == int or col_type == float:
			allow_columns[col] = index
		index += 1

	no_allow_columns = len(allow_columns)

	if columns == None:
		assert no_allow_columns > 0, 'No such columns have INTEGER or FLOAT values to plot the histogram'
		figure = []
		for col, index in allow_columns.items():
			figure.append(plt.figure())
			plt.hist(df.values[:, index].tolist())
			plt.title('Histogram of ' + str(col))
		plt.show()
	else:
		for col in columns:
			assert col in all_column_names, str(col) + ' is not present in dataframe. Check name of column.'
			assert col in allow_columns, str(col) + ' has invalid datatype for histogram. Only INT & FLOAT datatype is allowed.'

		figure = []
		for col in columns:
			figure.append(plt.figure())
			plt.hist(df.values[:, allow_columns[col]].tolist())
			plt.title('Histogram of ' + str(col))
		plt.show()




def test():
	"""
	filepath = './remain.json'
	columns = ['tweet_text']
	datatype = {'tweet_text' : 'str'}
	"""

	filepath = './test.csv'
	columns = ['ID', 'date_time', 'hum']
	datatype = {'ID' : 'int', 'date_time' : 'str', 'hum': 'int'}
	df = Dataframe.get_dataframe(filepath, columns, datatype, filetype='csv')
	columns = ['ID', 'hum']
	get_histogram(df, columns=columns)

if __name__ == "__main__":
	test()
	