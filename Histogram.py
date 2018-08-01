import Dataframe
import collections
import matplotlib.pyplot as plt

def arg_helper(columns, plot, bins, range, histtype, align, orientation, rwidth, log, color):
	"""
	Convert all arguments in dictionary form for each column name, even if it is not given by user and also want to provide same
	values to all columns.

	Args:
		1). columns: All feasible histogram column name.
		
		2). plot [dict/bool]: Columnwide plot flag values/Same plot-flag_value for all columns.
		
		3). bins [dict/int/list]: Columnwide bins values/Same bins_value for all columns by 'int' or 'list'. 
		
		4). range [dict/tuple]: Columnwide range values/Same range_value for all columns.
		
		5). histtype [dict/str]: Columnwide histtype values/Same histtype_value for all columns.
		
		6). align [dict/str]: Columnwide align values/Same align_value for all columns.
		
		7). orientation [dict/str]: Columnwide orientation values/Same orientation_value for all columns.
		
		8). rwidth [dict/float]: Columnwide rwidth values/Same rwidth_value for all columns.
		
		9). log [dict/bool]: Columnwide log values/Same log_value for all columns.
		
		10). color [dict/str]: Columnwide color values/Same color_value for all columns.

	Returns:	
		1). plot [dict]: Each columnwide plot flag values

		2). bins [dict]: Each columnwide bins values 
		
		3). range [dict]: Each columnwide range values
		
		4). histtype [dict]: Each columnwide histtype values
		
		5). align [dict]: Each columnwide align values
		
		6). orientation [dict]: Each columnwide orientation values
		
		7). rwidth [dict]: Each columnwide rwidth values
		
		8). log [dict]: Each columnwide log values
		
		9). color [dict]: Each columnwide color values

	"""
	no_columns = len(columns)

	if type(plot) == bool:
		temp_plot = {}
		for col in columns:
			temp_plot[col] = plot
	else:
		temp_plot = {}
		for col in columns:
			temp_plot[col] = plot.get(col, True)
	
	if bins == None:
		temp_bins = {}
		for col in columns:
			temp_bins[col] = None
	else:
		temp_bins = {}
		if type(bins) == dict:
			for col in columns:
				temp_bins[col] = bins.get(col, None)
		else:
			for col in columns:
				temp_bins[col] = bins

	if range == None:
		temp_range = {}
		for col in columns:
			temp_range[col] = None
	else:
		temp_range = {}
		if type(range) == dict:
			for col in columns:
				temp_range[col] = range.get(col, None)
		else:
			for col in columns:
				temp_range[col] = range	

	if type(histtype) == str:
		temp_histtype = {}
		for col in columns:
			temp_histtype[col] = histtype
	else:
		temp_histtype = {}
		for col in columns:
			temp_histtype[col] = histtype.get(col, 'bar')
		
	if type(align) == str:
		temp_align = {}
		for col in columns:
			temp_align[col] = align
	else:
		temp_align = {}
		for col in columns:
			temp_align[col] = align.get(col, 'mid')

	if type(orientation) == str:
		temp_orientation = {}
		for col in columns:
			temp_orientation[col] = orientation
	else:
		temp_orientation = {}
		for col in columns:
			temp_orientation[col] = orientation.get(col, 'vertical')
		
	if rwidth == None:
		temp_rwidth = {}
		for col in columns:
			temp_rwidth[col] = None
	else:
		temp_rwidth = {}
		if type(rwidth) == dict:
			for col in columns:
				temp_rwidth[col] = rwidth.get(col, None)
		else:
			for col in columns:
				temp_rwidth[col] = rwidth

	if type(log) == bool:
		temp_log = {}
		for col in columns:
			temp_log[col] = log
	else:
		temp_log = {}
		for col in columns:
			temp_log[col] = log.get(col, False)
		
	if color == None:
		temp_color = {}
		for col in columns:
			temp_color[col] = None
	else:
		temp_color = {}
		if type(color) == dict:
			for col in columns:
				temp_color[col] = color.get(col, None)
		else:
			for col in columns:
				temp_color[col] = color

	return (temp_plot, temp_bins, temp_range, temp_histtype, temp_align, temp_orientation, temp_rwidth, temp_log, temp_color)

def get_histogram(df, columns = None, plot=True, bins=None, range=None, histtype='bar', align='mid', orientation='vertical', rwidth=None, log=False, color=None):
	"""
	For given dataframe, it finds INT & FLOAT columns to plot histogram.

	Args:
		1). df [pandas DataFrame]: pandas DataFrame

		2). columns [list]: list of column name going to have histogram (In string type & same name as in dataframe/dataset).
							Only INT & FLOAT type column is allowed.
							Default: None [All INT & FLOAT columns histogram will be computed]
		
		3). plot [dict/bool]: Plot_histogram flag 
							  Default: True [All INT & FLOAT columns histogram will be drawed]
							  Columnwide different value can also be assigned for different columns through dictionary.
							  ex: plot={'Maths': True, 'Total': False}
							  Same value for all columns can also be assigned just by passing value instead using dictionary.
							  ex: plot=False
		
		4). bins [dict/int/list]: Equal or unequal bin size/boundaries
								  Default: None [Number of bin will be 10 within column range]
								  INT value means number of bins within range.
								  LIST value means bins partion's boundaries (bins + 1) 
								  Columnwide different value can also be assigned for different columns through dictionary.
								  ex: bins={'Maths': 10, 'Total': [0,1,1.5,3,4]}
								  Same value for all columns can also be assigned just by passing value instead using dictionary.
								  ex: bins=20 or bins=[10,20,30]						  
		
		5). range [dict/tuple]: Range of value in INT & FLOAT columns
								Default: None [(min(x), max(x)) will be your range]
								Columnwide different value can also be assigned for different columns through dictionary.
							  	ex: range={'Maths': (10,50), 'Total': (0,500)}
								Same value for all columns can also be assigned just by passing value instead using dictionary.
							  	ex: range=(20,50)						
		
		6). histtype [dict/str]: Type of Histogram to draw. ['bar', 'barstacked', 'step', 'stepfilled']
								 Default: 'bar'
								 Columnwide different value can also be assigned for different columns through dictionary.
							  	 ex: histtype={'Maths': 'bar', 'Total': 'step'}
								 Same value for all columns can also be assigned just by passing value instead using dictionary.
							  	 ex: histtype='step'						 
		
		7). align [dict/str]: Controls how the histogram is plotted. [‘left’, ‘mid’, ‘right’]
							  Default: 'mid'
							  Columnwide different value can also be assigned for different columns through dictionary.
						  	  ex: align={'Maths': 'mid', 'Total': 'right'}
							  Same value for all columns can also be assigned just by passing value instead using dictionary.
						  	  ex: align='left'

		8). orientation [dict/str]: If ‘horizontal’, barh will be used for bar-type histograms. [‘horizontal’, ‘vertical’]
									Default: 'vertical'
								  	Columnwide different value can also be assigned for different columns through dictionary.
							  	  	ex: align={'Maths': 'vertical', 'Total': 'horizontal'}
								  	Same value for all columns can also be assigned just by passing value instead using dictionary.
							  	  	ex: align='vertical'

		9). rwidth [dict/float]: The relative width of the bars as a fraction of the bin width. 
								 Default: None
							  	 Columnwide different value can also be assigned for different columns through dictionary.
						  	  	 ex: align={'Maths': 2.5, 'Total': 5.2}
							  	 Same value for all columns can also be assigned just by passing value instead using dictionary.
						  	  	 ex: align=2.1
		
		10). log [dict/bool]: If True, the histogram axis will be set to a log scale.
							  Default: False
							  Columnwide different value can also be assigned for different columns through dictionary.
							  ex: align={'Maths': False, 'Total': True}
							  Same value for all columns can also be assigned just by passing value instead using dictionary.
							  ex: align=True


		11). color [dict/str]: Color specification. ['red', 'green', ...]
							   Default: None
							   Columnwide different value can also be assigned for different columns through dictionary.
						  	   ex: align={'Maths': 'red', 'Total': 'green'}
							   Same value for all columns can also be assigned just by passing value instead using dictionary.
						  	   ex: align='red'

	Returns:
		1). hist_return [dict]: Columnwide different value will be returned for different columns through dictionary.
								Each column contains following three:
									n ==> The values of the histogram bins.
									bins ==> The edges of the bins.
									patches ==> Silent list of individual patches used to create the histogram.

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
	hist_return = {}
	unplotted = {}

	if columns == None:
		assert no_allow_columns > 0, 'No such columns have INTEGER or FLOAT values to plot the histogram'
		(plot, bins, range, histtype, align, orientation, rwidth, log, color) = arg_helper(allow_columns.keys(), plot, bins, range, histtype, align, orientation, rwidth, log, color)
		for col, index in allow_columns.items():
			if plot[col] == True:
				plt.figure()
				hist_return[col] = plt.hist(df.values[:, index].tolist(), bins=bins[col], range=range[col], histtype=histtype[col], align=align[col], orientation=orientation[col], rwidth=rwidth[col], log=log[col], color=color[col])
				plt.title('Histogram of ' + str(col))
			else:
				unplotted[col] = index
		
		plt.show()
		for col, index in unplotted.items():
			hist_return[col] = plt.hist(df.values[:, index].tolist(), bins=bins[col], range=range[col], histtype=histtype[col], align=align[col], orientation=orientation[col], rwidth=rwidth[col], log=log[col], color=color[col])

	else:
		for col in columns:
			assert col in all_column_names, str(col) + ' is not present in dataframe. Check name of column.'
			assert col in allow_columns, str(col) + ' has invalid datatype for histogram. Only INT & FLOAT datatype is allowed.'

		figure = []
		(plot, bins, range, histtype, align, orientation, rwidth, log, color) = arg_helper(columns, plot, bins, range, histtype, align, orientation, rwidth, log, color)
		for col in columns:
			if plot[col] == True:
				plt.figure()
				hist_return[col] = plt.hist(df.values[:, allow_columns[col]].tolist(), bins=bins[col], range=range[col], histtype=histtype[col], align=align[col], orientation=orientation[col], rwidth=rwidth[col], log=log[col], color=color[col])
				plt.title('Histogram of ' + str(col))
			else:
				unplotted[col] = index

		plt.show()

		for col, index in unplotted.items():
			hist_return[col] = plt.hist(df.values[:, index].tolist(), bins=bins[col], range=range[col], histtype=histtype[col], align=align[col], orientation=orientation[col], rwidth=rwidth[col], log=log[col], color=color[col])


	return hist_return

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
	hist_return = get_histogram(df, plot={'ID':False, 'hum':True}, bins=5, range=(10,20), histtype='step')
	print(hist_return)

if __name__ == "__main__":
	test()
	