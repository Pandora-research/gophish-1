#! python

import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

import sys
import argparse
import shutil
import csv
import os
import configparser
import random
import string

from gophish import Gophish
from gophish.models import *


parser = argparse.ArgumentParser('Delete Users from GoPhish')

args = parser.parse_args()

if not os.path.isfile('config.config'):
	sys.exit("Configuration file is missing.")
	
config = configparser.ConfigParser()
config.read('config.config')

api = Gophish(config['DEFAULT']['API_KEY'], host=config['DEFAULT']['GOPHISH_URL'], verify=False)


groups = api.groups.get()
groups.sort(key=lambda x: x.name)

for group in groups:
	print("Deleting group ({}) with ID: {}\n".format(group.name, group.id))
	api.groups.delete(group.id)

#end