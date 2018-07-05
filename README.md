# vicharana
A python way for data analysis.

## Dataframe

Get pandas dataframe by passing .csv, .txt, & .json file. Even you can type cast data by providing the columns/attributes datatype in the following format.

```
#Common way: without typcasting
filepath = './test.csv'
dataframe = get_dataframe(filepath)
```

```
#With selective column only
columns = ['ID', 'name']
dataframe = get_dataframe(filepath, columns)
```

```
#With typecast
columns = ['ID', 'name', 'pass']
datatype = {'ID': 'int', 'name': 'str'}
dataframe = get_dataframe(filepath, columns= columns, datatype = datatype)
```

```
Main calling function of API 
This function returns the dataframe(pandas) based on .csv, .txt, .json files of datasets.

Args:
	filepath (string)      : Dataset file's relative/absolute path. It must be CSV, TEXT, JSON file, if extension(.csv, .txt, .json) is not given in the file's basename(test ----> test.json), then filetype argument is required. If extension and filetype argument is given then it should be match.
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
```
