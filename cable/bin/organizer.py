#!/usr/bin/env python3
import os
import sys
import argparse

class Organizer(object):
	"""Class to organize a data science project"""
	folders=['analysis','data','logs','logs/train_logs','logs/tensorboard_logs','model','model_weights','config','pipeline','pipeline/cleaning','pipeline/encoding']

	def __init__(self, project_name,path):
		super(Organizer, self).__init__()
		self.path = path
		self.project_name=project_name


	def make_folders(self):
		"""
		Makes folders for experimentation
		"""
		for name in self.folders:
			os.makedirs(self.path+"/"+name,exist_ok=True)

