#!/usr/bin/env python

from setuptools import setup, find_packages
import os
import subprocess
#adding path to bash profile
installation_path=os.__file__[:-5]+'site-packages/cable/cd '
home_path= subprocess.Popen("echo $HOME", shell=True, stdout=subprocess.PIPE).stdout.read().strip().decode('utf-8')

with open(home_path+"/.bash_profile",'a') as f:
	f.write("added by cable installer\n")
	f.write('export PATH=$PATH":'+installation_path+"\n")

with open(home_path+"/.bashrc",'a') as f:
	f.write("added by cable installer\n")
	f.write('export PATH=$PATH":'+installation_path+"\n")

setup(name='cable',
      version='0.0.3',
      description='This package has components  for preprocessing',
      author='Avhirup',
      author_email='avhirupchakraborty@gmail.com',
      packages=find_packages(exclude=["*.tests", "*.tests.*", "tests.*", "tests"])
    )
