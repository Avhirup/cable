import pandas as pd 
import numpy as np 
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
import category_encoders as ce

class Fisher(BaseEstimator, TransformerMixin):
    def __init__(self,percentile=0.95):
            self.percentile = percentile
    def fit(self, X, y):
            from numpy import shape, argsort, ceil
            X_pos, X_neg = X[y==1], X[y==0]
            X_mean = X.mean(axis=0)
            X_pos_mean, X_neg_mean = X_pos.mean(axis=0), X_neg.mean(axis=0)
            deno = (1.0/(shape(X_pos)[0]-1))*X_pos.var(axis=0) + (1.0/(shape(X_neg)[0]-1))*X_neg.var(axis=0)
            num = (X_pos_mean - X_mean)**2 + (X_neg_mean - X_mean)**2
            F = num/deno
            sort_F = argsort(F)[::-1]
            n_feature = (float(self.percentile)/100)*shape(X)[1]
            self.ind_feature = sort_F[:ceil(n_feature)]
            return self
    def transform(self, x):
            return x[self.ind_feature,:]

class DateTimeEngineer(BaseEstimator,TransformerMixin):
	"""Helper to Add Date/Time features to data"""
	def __init__(self,columns,options=["dayofweek","dayofyear"]):
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
		self.each_column_transform[column]=temp

	def fit(self,X,y=None):
		self.__check_columns(X)
		for column in self.columns_to_transform :
			self.__transform_column(X,column)
		return self

	def transform(self,x):
		all_concat=pd.concat(list(self.each_column_transform.values()),axis=1)
		return pd.concat([x,all_concat],axis=1)




class CategoryEngineer(object):
	"""docstring for CategoryEngineer"""
	def __init__(self,columns, encoding_method=["OneHotEncoder"]):
		super(CategoryEngineer, self).__init__()
		self.options_supported= ["BackwardDifferenceEncoder","BinaryEncoder","HashingEncoder","HelmertEncoder","OneHotEncoder","OrdinalEncoder","SumEncoder","PolynomialEncoder","BaseNEncoder","TargetEncoder","LeaveOneOutEncoder"]
		self.columns=columns
		self.encoding_method=encoding_method[0]

	def __check_options(self,options):
		for opt in options: 
			if opt not in self.options_supported:
				raise NotImplementedError

	def fit(self,X,y=None):
		self.encoder=getattr(ce,self.encoding_method)(cols=self.columns,use_cat_names=True)
		self.encoder.fit(X,y)
		return self

	def transform(self,x):
		return self.encoder.transform(x)


class NumericalEngineer(object):
	"""docstring for NumericalEngineer"""
	def __init__(self, arg):
		super(NumericalEngineer, self).__init__()
		self.arg = arg
		raise NotImplementedError
		



class CastingEngineer(object):
	"""docstring for NumericalEngineer"""
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
			X=X.drop(self.key_columns, axis=1)
		X[self.date_columns]=X[self.date_columns].apply(pd.to_datetime)
		X[self.numerical_columns]=X[self.numerical_columns].apply(pd.to_numeric)
		X[self.category_columns]=X[self.category_columns].fillna(-1)
		# X[self.category_columns]=X[self.category_columns].astype("category")
		return X





		

