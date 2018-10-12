from prettytable import PrettyTable
import pandas as pd

def chunks(l, n):
	"""Yield successive n-sized chunks from l."""
	for i in range(0, len(l), n):
		yield l[i:i + n]


def print_list(l,is_nb=True,is_fp=False,num_of_items_in_a_row=2):
	t=PrettyTable()
	if is_fp:
		l=list(map(lambda x: x.split("/")[-1],l))
	for l_part in chunks(l,num_of_items_in_a_row):
		l_part.extend(["*"]*(num_of_items_in_a_row-len(l_part)))
		t.add_row(l_part)
	print(t)

def find_id_columns(columns,suffix="_ID"):
	return filter(lambda x:x[-len(suffix):]==suffix,columns)

def find_columns_empty(data):
	return filter(lambda x:data[x].isnull().any(),data.columns)

def find_type_and_length(data):
	column_type={}
	column_length={}
	for column in data.columns:
		k=data[column].value_counts().keys()
		column_type[column]=k.dtype
		column_length[column]=len(k)
	return column_type,column_length

def find_numerical_columns(column_type):
	return filter(lambda x:x[1]!='O',column_type.items())	

def find_categorical_columns(column_type):
	return filter(lambda x:x[1]=='O',column_type.items()) 


def dict_to_table(dictionary,columns=["Key","Vales"],header=True):
	t=PrettyTable(columns,header=header)
	for k,v in dictionary.items():
		t.add_row([k,v])
	return t

def list_to_table(l,column_name=None):
	if column_name:
		t=PrettyTable([column_name])
	else:
		t=PrettyTable(header=False)

	for c in l:
		t.add_row([c])
	return t

		
def describe_data(file_path,extension="xls",is_detailed=False):
	"""
	Makes reports to analyse and get overview of data quick
	Input:
	file_path: location of the file
	extension: file_extension of the file
	is_detailed: Describe detailed report which prints the name of the columns instead of the just numbers

	#TODO:
	* return t instead of printing
	* additioal analystics and statistics 
	"""
	try:
		if extension=="xls":
			data=pd.read_excel(file_path)
		elif extension=="csv":
			data=pd.read_csv(file_path)
		else:
			print("Not Supported file type")
			return 
	except Exception as e:
		print("Unable to Open file"+e.__traceback__)
		return
	#details 
	t=PrettyTable(['Description',"Information"])
	t.title=file_path.split('/')[-1]
	print("            "+t.title)
	t.add_row(['Row and Column',data.shape])
	if not is_detailed:
		t.add_row(['# of ID columns',len(list(find_id_columns(data.columns)))])
		t.add_row(['# of Columns with Empty Values',len(list(find_columns_empty(data)))])
		column_type,column_length=find_type_and_length(data)
		t.add_row(['# of Categorical Values',len(list(find_numerical_columns(column_type)))])
		t.add_row(['# of Numberical Values',len(list(find_categorical_columns(column_type)))])
		t.add_row(['Column length distribution',dict_to_table(column_length,['Column','Length'])])
	else:
		t.add_row(['Columns',list_to_table(list(data.columns))])
		t.add_row(['ID columns',list_to_table(list(find_id_columns(data.columns)))])
		t.add_row(['Columns with Empty Values',list_to_table(list(find_columns_empty(data)))])
		column_type,column_length=find_type_and_length(data)
		t.add_row(['Categorical Columns',list_to_table(list(map(lambda x:x[0],find_numerical_columns(column_type))))])
		t.add_row(['Numberical Columns',list_to_table(list(map(lambda x:x[0],find_categorical_columns(column_type))))])
		t.add_row(['Column length distribution',dict_to_table(column_length,['Column','Length'])])

	print(t)

def describe_series(series):
	"""
	Makes reports to analyse and get overview of data quick
	Input:
	series : pandas series for analysis
	#TODO:
	* return t instead of printing
	* additioal analystics and statistics 
	"""	
	t=PrettyTable(['Description','Information'])
	t.title=series.name
	is_category=series.value_counts().keys().dtype=='O'
	t.add_row(['Empty Rows',dict_to_table(dict(series.isnull().value_counts()),header=False)])
	if is_category:
		t.add_row(['Category and Count',dict_to_table(dict(series.value_counts()))])
	else:
		t.add_row(['Statistics',dict_to_table(dict(series.describe()))])
	#ToDo: Add statistical tests

	print(t)













	


