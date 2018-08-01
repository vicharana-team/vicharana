import sys
import os
import codecs
import json
import pandas as pd

def nested_data(attributes: list, dict_line: dict) -> str:
	"""
	It trace out the nested structure values of elements of the json format.

	Args:
		attributes (list)     : list of elements of json in order to reach at particular attribute.
		dict_line (dictionary): It is json.loads(line) object

	Returns:
		value :	value of particular nested element in json.
	"""

	for att in attributes:
		temp = dict_line[att]
		dict_line = temp
	return dict_line


def json_to_dataframe(filepath: str, attributes: list, given_columns: list, datatype: dict):
	"""
	This function convert json files to dataframe accroding to given_columns and datatype by type casting.

	Args:
		filepath (string)    : Relative/Absolute path of json dataset file.
		attributes (list)    : All the available attributes in json files.
		given_columns (list) : Required column in dataframe. 
							   None: It will returns dataframe of attributes.
		datatype (dictionary): Datatype of column that is going to be type cast.

	Returns:
		Dataframe (Pandas dataframe object): It is dataframe of pandas.		
	"""

	types = {'int': int, 'str': str, 'float': float, 'boolean': str_to_bool}
	final_data = []
	reading_file_pointer = codecs.open(filepath, 'r', 'utf-8')
	if given_columns == None:
		if datatype == None:
			for line in reading_file_pointer:
				dict_line = json.loads(line)
				temp = []
				for att in attributes:
					if isinstance(att, list):
						temp.append(nested_data(att, dict_line))
					else:
						temp.append(dict_line[att])
				final_data.append(temp)
		else:
			given_datatype = parse_dict_line(datatype)
			for line in reading_file_pointer:
				dict_line = json.loads(line)
				temp = []
				for att in attributes:
					if isinstance(att, list):
						if att in given_datatype:
							temp.append(types[nested_data(att, datatype)](nested_data(att, dict_line)))
						else:
							temp.append(nested_data(att, dict_line))
					else:
						if att in given_datatype:
							temp.append(types[datatype[att]](dict_line[att]))
						else:
							temp.append(dict_line[att])
				final_data.append(temp)
		
		column_names = []
		for att in attributes:
			if isinstance(att, list):
				column_names.append(att[-1])
			else:
				column_names.append(att)

		dataframe = pd.DataFrame(final_data,columns=column_names)
	else:
		if datatype == None:
			for line in reading_file_pointer:
				dict_line = json.loads(line)
				temp = []
				for att in given_columns:
					if isinstance(att, list):
						temp.append(nested_data(att, dict_line))
					else:
						temp.append(dict_line[att])
				final_data.append(temp)
		else:
			given_datatype = parse_dict_line(datatype)
			for line in reading_file_pointer:
				dict_line = json.loads(line)
				temp = []
				for att in given_columns:
					if isinstance(att, list):
						if att in given_datatype:
							temp.append(types[nested_data(att, datatype)](nested_data(att, dict_line)))
						else:
							temp.append(nested_data(att, dict_line))
					else:
						if att in given_datatype:
							temp.append(types[datatype[att]](dict_line[att]))
						else:
							temp.append(dict_line[att])
				final_data.append(temp)
		
		column_names = []
		for att in given_columns:
			if isinstance(att, list):
				column_names.append(att[-1])
			else:
				column_names.append(att)

		dataframe = pd.DataFrame(final_data,columns=column_names)
	
	reading_file_pointer.close()
	return dataframe

def parse_dict_line(dict_line: dict) -> list:
	"""
	It is recursive function to list out all the attributes.

	Args:
		dict_line (dictionary): It is json.loads(line) object 
	
	Returns:
		attributes (list of string/ nested list): list of attributes from json format of file. 
	"""
	keys = dict_line.keys()
	attributes = []
	for k in keys:
		if isinstance(dict_line[k], dict):
			att = parse_dict_line(dict_line[k])
			for i in att:
				temp = []
				temp.extend(k)
				temp.extend(i)
				attributes.append(temp)
		else:
			attributes.append(k)
	return attributes

def get_json_attributes(filepath: str):
	"""
	Returns the attributes/elements of json format of dataset from the file.

	Args:
		filepath (string)    : Relative/Absolute path of json dataset file.

	Returns:
		attributes (list of string/ nested list): list of attributes from json format of file.
		It looks like in the following format.
		Refers the get_dataframe functions details.
		columns = ['ID', 'Name', ['Marks', 'Maths'], ['Marks', 'language', 'English'], ['Marks', 'language', 'Hindi'], 'Pass']
	"""
	attributes = []
	reading_file_pointer = codecs.open(filepath, 'r', 'utf-8')
	line = reading_file_pointer.readline()
	attributes = parse_dict_line(json.loads(line))
	reading_file_pointer.close()
	return attributes

def get_columns(filepath: str) -> list:
	"""
	Returns column names list from csv/txt file.

	Args:
		filepath (string)    : Relative/Absolute path of csv/txt dataset file.

	Returns:
		attributes (list): list of column names in string.
	"""
	columns = []
	str_columns = []
	reading_file_pointer = codecs.open(filepath, 'r', 'utf-8')
	line = reading_file_pointer.readline()
	columns = line.split(',')
	for col in columns:
		str_columns.append(str(col))
	reading_file_pointer.close()
	return str_columns

def str_to_bool(string: str) -> bool:
	"""
	It convert string true/false to boolean datatype.

	Args:
		string (string): "true"/"false"
	
	Returns:
		Boolean values: True/False
	"""
	string = string.lower()

	if string == 'true':
		 return True
	elif string == 'false':
		 return False
	else:
		 sys.exit(str(string) + ' can\'t be converted to boolean')

def csv_to_dataframe(filepath: str, all_columns: list, given_columns: list, datatype: dict):
	"""
	This function convert csv and txt files to dataframe accroding to given_columns and datatype by type casting.

	Args:
		filepath (string)    : Relative/Absolute path of csv/txt dataset file.
		all_columns (list)   : All the available columns in csv/txt files.
		given_columns (list) : Required column in dataframe. 
							   None: It will returns dataframe of all_columns.
		datatype (dictionary): Datatype of column that is going to be type cast.

	Returns:
		Dataframe (Pandas dataframe object): It is dataframe of pandas.

	"""
	types = {'int': int, 'str': str, 'float': float, 'boolean': str_to_bool}
	final_data = []
	all_columns_index = {}
	index = 0
	for col in all_columns:
		all_columns_index[col] = index
		index += 1

	reading_file_pointer = codecs.open(filepath, 'r', 'utf-8')
	if given_columns == None:
		if datatype == None:
			line_no = 1
			for line in reading_file_pointer:
				if line_no == 1:
					line_no = 0
					continue

				data_row = line.split(',')	
				new_data_row = []
				for col in all_columns:
					try:
						new_data_row.append(data_row[all_columns_index[col]].strip())
					except:
						print(data_row[all_columns_index[col]])
						continue
				final_data.append(new_data_row)
		else:
			given_datatype = datatype.keys()
			line_no = 1
			for line in reading_file_pointer:
				if line_no == 1:
					line_no = 0
					continue

				data_row = line.split(',')
				new_data_row = []
				for col in all_columns:
					try:
						if col in given_datatype:
							new_data_row.append(types[datatype[col]](data_row[all_columns_index[col]].strip()))
						else:
							new_data_row.append(data_row[all_columns_index[col]].strip())
					except:
						print(data_row[all_columns_index[col]])
						continue
				final_data.append(new_data_row)
		dataframe = pd.DataFrame(final_data,columns=all_columns)
	else:
		if datatype == None:
			line_no = 1
			for line in reading_file_pointer:
				if line_no == 1:
					line_no = 0
					continue

				data_row = line.split(',')	
				new_data_row = []
				for col in given_columns:
					try:
						new_data_row.append(data_row[all_columns_index[col]].strip())
					except:
						print(data_row[all_columns_index[col]])
						continue
				final_data.append(new_data_row)
		else:
			given_datatype = datatype.keys()
			line_no = 1
			for line in reading_file_pointer:
				if line_no == 1:
					line_no = 0
					continue

				data_row = line.split(',')
				new_data_row = []
				for col in given_columns:
					try:
						if col in given_datatype:
							new_data_row.append(types[datatype[col]](data_row[all_columns_index[col]].strip()))
						else:
							new_data_row.append(data_row[all_columns_index[col]].strip())
					except:
						print(data_row[all_columns_index[col]])
						continue
				final_data.append(new_data_row)
		dataframe = pd.DataFrame(final_data,columns=given_columns)
	reading_file_pointer.close()
	return dataframe

def read_file(filepath: str, filetype: str, given_columns: list, datatype: dict):
	"""
	This function returns the dataframe(pandas) of given_columns based on .csv, .txt, .json files of datasets by typecasting datatype.

	Args:
		filepath (string)	  : Dataset file's relative/absolute path. It must be CSV, TEXT, JSON file.
		filetype (string)     : Possible values -----> 'txt', 'csv', 'json'
		given_columns (list)  : Required columns/attributes in dataframe.
		datatype (dictionary) : Datatype for type casting.

	Returns:
		Dataframe (Pandas dataframe object): It is dataframe of pandas.
	"""
	if filetype == 'txt' or filetype == 'csv':
		all_columns = get_columns(filepath)
		dataframe = csv_to_dataframe(filepath, all_columns, given_columns, datatype)
	else:
		attributes = get_json_attributes(filepath)
		dataframe = json_to_dataframe(filepath, attributes, given_columns, datatype)
	return dataframe

def get_filetype(filepath: str):
	"""
	It returns the filetype from the relative/absolute file address.

	Args:
		filepath (string): Dataset file's relative/absolute path
	
	Returns:
		extension: It returns following values.
				   'txt' for text file
				   'csv' for csv file
				   'json' for json file
				   None for if extension is not from the above list or not given in file's basename.
	"""
	file_basename = os.path.basename(filepath)
	split_names = file_basename.split('.')
	if len(split_names) == 1:
		return None
	else:
		return split_names[-1] 

def get_dataframe(filepath: str, columns = None, datatype = None, filetype = None):
	"""
	Main calling function of API 
	This function returns the dataframe(pandas) based on .csv, .txt, .json files of datasets.

	Args:
		filepath (string)      : Dataset file's relative/absolute path. It must be CSV, TEXT, JSON file, if extension(.csv, .txt, .json)
						         is not given in the file's basename(test ----> test.json), then filetype argument is required.
						         If extension and filetype argument is given then it should be match.
								 TEXT ----> Data is in comma separable format but saved as .txt.
								 CSV & TEXT file should have first column with column names in comma separable manner.

		columns (list)         : Provide only required columns dataframe.
								 This argumnet differs for the file types.

			.txt or .csv -----> list of column names in string 
			(By default: None)-----> That creates all the column names list.  
			columns = ['ID', 'Name', 'Date_Time']
			
			.json -----> list of attribute names in string and list(WHY LIST?).
			(By default: None)-----> That creates all the attributes list in following manner.
					WHY LIST?
					{
					'ID': 1,
					'Name': 'Ghanshyam',
					'Marks': {
							  'Maths' : 95,
							  'language': {
										  'English' : 80,
										  'Hindi': A+
										  }
							 }
					'Pass': True
					}
			columns = ['ID', 'Name', ['Marks', 'Maths'], ['Marks', 'language', 'English'], ['Marks', 'language', 'Hindi'], 'Pass']

		datatype (dictionary)  : datatypes for columns/attributes for those we want to apply strict type conversion.
								 (if possible else will generate error)
								 Supported datatype: str, int, boolean, float
								 This arguments differs for the file types.
			.txt or .csv ----->  datatype = {'column1': 'int', 'column2': 'str', 'column3': 'float', 'column4': 'boolean'}
			(By default: None)-----> That doesn't apply any type conversion.

			.json ----> (By default: None)-----> That doesn't apply any type conversion.
			{
			'ID': 'int',
			'Name': 'str',
			'Marks': {
					  'Maths' : 'int',
					  'language': {
								  'English' : 'int',
								  'Hindi': 'str'
								  }
					 }
			'Pass': 'boolean'
			}

		filetype (string)      : Available values -----> 'txt', 'csv', 'json'
		(By default: None)-----> If you have pass the filepath with one of the supported extensions, then filetype = None is works.
		If filepath is not having extension then filetype is mandatory.

	Returns:
			Dataframe (Pandas dataframe object): It is dataframe of pandas.
	"""
	assert os.path.exists(filepath), "Given filepath doesn't exist"

	supported_file_type = ['txt', 'json', 'csv']

	if filetype == None:
		filetype = get_filetype(filepath)
		if filetype in supported_file_type:
			dataframe = read_file(filepath, filetype, columns, datatype)
		else:
			sys.exit('Add file extension: json, txt, and csv format are allowed')
	else:
		filetype = filetype.lower()
		if filetype in supported_file_type:
			if get_filetype(filepath) != None:
				if get_filetype(filepath) == filetype:
					dataframe = read_file(filepath, filetype, columns, datatype)
				else:
					sys.exit('File extension doesn\'t match with filetype argument')
			else:
				dataframe = read_file(filepath, filetype, columns, datatype)
		else:
			if get_filetype(filepath) == None:
				sys.exit('Add file extension')
			else:
				if get_filetype(filepath) in supported_file_type:
					dataframe = read_file(filepath, filetype, columns, datatype)
				else:
					sys.exit('Filetype is not supported: json, txt, and csv format is allowed')
	return dataframe

def test():
	"""
	filepath = './test.csv'
	columns = ['ID', 'date_time', 'hum']
	datatype = {'ID' : 'int', 'date_time' : 'str'}
	dataframe = get_dataframe(filepath, columns, datatype, filetype='csv')
	"""
	
	
	filepath = './remain.json'
	columns = ['tweet_text']
	datatype = {'tweet_text' : 'str'}
	dataframe = get_dataframe(filepath, datatype = datatype)
	
	print(dataframe)

if __name__ == "__main__":
	test()