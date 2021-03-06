import pandas as pd 
import numpy as np 
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import StandardScaler,Normalizer
from sklearn.pipeline import Pipeline
import category_encoders as ce
import pickle 

class DateTimeEngineer(BaseEstimator,TransformerMixin):
	"""Helper to Add Date/Time features to data"""
	def __init__(self,columns,options=["dayofweek","dayofyear"],is_train=None,enc_loc=None):
		self.options_supported=["dayofweek","dayofyear","dayofmonth","daysinmonth","hour","is_leap_year","is_month_end","is_month_start","is_quarter_end","is_year_start","is_year_end","minute","month","month_name","quarter","second","week","weekday","weekday_name","weekofyear"]
		self.__check_options(options)
		self.options=options
		self.columns_to_transform=columns
		self.each_column_transform={}

	def __check_options(self,options):
		for opt in options: 
			if opt not in self.options_supported:
				raise NotImplementedError(opt)

	def __check_columns(self,X):
		for i in self.columns_to_transform:
			try:
				X[i].dt
			except Exception as e:
				raise Exception(f"Column {i} not in correct format"+str(e))

	def __transform_column(self,data,column):
		temp=pd.DataFrame()
		x=data[column].dt
		if 'day_name' in self.options:
			temp[column+'_day_name']=x.day_name()
		# replace by getattr 
		for opt in self.options:
			temp[column+'_'+opt]=getattr(x,opt)
		self.each_column_transform[column]=temp.fillna(0)

	def fit(self,X,y=None):
		self.__check_columns(X)
		for column in self.columns_to_transform :
			self.__transform_column(X,column)
		return self

	def transform(self,x):
		all_concat=pd.concat(list(self.each_column_transform.values()),axis=1)
		return pd.concat([x,all_concat],axis=1)


class CategoryEngineer(BaseEstimator,TransformerMixin):
	"""Helper to encode Categorical Columns"""
	def __init__(self,columns, encoding_method=["OneHotEncoder"],is_train=True,enc_loc=None):
		super(CategoryEngineer, self).__init__()
		self.options_supported= ["BackwardDifferenceEncoder","BinaryEncoder","HashingEncoder","HelmertEncoder","OneHotEncoder","OrdinalEncoder","SumEncoder","PolynomialEncoder","BaseNEncoder","TargetEncoder","LeaveOneOutEncoder"]
		self.columns=columns
		self.encoding_method=encoding_method[0]
		self.is_train=is_train
		self.enc_loc=enc_loc
		self.__check_options(encoding_method)

	def __check_options(self,options):
		for opt in options: 
			if opt not in self.options_supported:
				raise NotImplementedError

	def fit(self,X,y=None):
		if self.is_train:
			self.encoder=getattr(ce,self.encoding_method)(cols=self.columns,use_cat_names=True)
			self.encoder.fit(X,y)
			with open(self.enc_loc,"wb") as f:
				pickle.dump(self.encoder,f)	
		else:
			self.encoder=pickle.load(open(self.enc_loc,"rb"))
		return self

	def transform(self,x):
		return self.encoder.transform(x)

class OutputEngineer(BaseEstimator,TransformerMixin):
	"""Encoder to encoder OutputClass"""
	def __init__(self, column,is_classification=True,is_train=True,enc_loc=None):
		super(OutputEngineer, self).__init__()
		self.column = column
		self.is_train=is_train
		self.enc_loc=enc_loc

	def fit(self,X,y=None):
		if self.is_train:
			self.encoder=LabelEncoder()
			self.encoder.fit(X[self.column].fillna("Null").tolist())
			with open(self.enc_loc,"wb") as f:
				pickle.dump(self.encoder,f)	
		else:
			self.encoder=pickle.load(open(self.enc_loc,"rb"))
		return self

	def transform(self,x):
		x[self.column+'_output']=self.encoder.transform(x[self.column].fillna("Null").tolist())
		return x



class NumericalEngineer(BaseEstimator,TransformerMixin):
	"""Helper to Normalize/Scale numerical columns"""
	def __init__(self, columns,encoding_method="StandardScaler",is_train=True,enc_loc=None):
		super(NumericalEngineer, self).__init__()
		self.columns = columns
		self.encoding_method=encoding_method
		self.__options_supported= ["MinMaxScaler","StandardScaler"]
		self.is_train=is_train
		self.enc_loc=enc_loc

	def __check_options(self,_options):
		for opt in options: 
			if opt not in self.options_supported:
				raise NotImplementedError		

	def fit(self,X,y=None):
		if self.is_train:
			self.scaler=globals()[self.encoding_method]()

			c=list(map(lambda x:x+f"_{self.encoding_method}",self.columns))
			self.scaler.fit(X[self.columns].fillna(0))
			with open(self.enc_loc,"wb") as f:
				pickle.dump(self.scaler,f)	
		else:
			self.scaler=pickle.load(open(self.enc_loc,"rb"))
		return self

	def transform(self,x):
		temp=pd.DataFrame()
		try:
			c=list(map(lambda x:x+f"_{self.encoding_method}",self.columns))
			scaled=pd.DataFrame(self.scaler.transform(x[self.columns].fillna(0)),columns=c)
			temp=pd.concat([temp,scaled],axis=1)
		except Exception as e:
			raise e
		
		return pd.concat([x,temp],axis=1)



class CastingEngineer(BaseEstimator,TransformerMixin):
	"""Helper to cast columns to proper type"""
	def __init__(self,casting_map,drop_key=False):
		super(CastingEngineer, self).__init__()
		self.casting_map=casting_map
		self.date_columns=self.casting_map["Date"]
		self.numerical_columns=self.casting_map["Numerical"]
		self.category_columns=self.casting_map["Category"]
		self.key_columns=self.casting_map["Key"]
		self.drop_key=drop_key

	def fit(self,X,y=None):
		return self
	def transform(self,X):
		if self.drop_key:
			X=X.drop(self.key_columns, axis=1,errors='ignore')
		X[self.date_columns]=X[self.date_columns].apply(pd.to_datetime)
		for n_col in self.numerical_columns:
			X[n_col]=X[n_col].fillna(0).astype(str).apply(lambda x:x.split('.')[0].replace(",","") if isinstance(x,str) else x).apply(pd.to_numeric)
		for c_col in self.category_columns:
			X[c_col]=X[c_col].fillna("Null").apply(lambda x:x.lower())
		return X





		

