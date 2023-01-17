#! python

import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

import sys
import argparse
import shutil
import csv
import os
import configparser
from gophish import Gophish
from gophish.models import *

parser = argparse.ArgumentParser('Export GoPhish Users to CSV.')

parser.add_argument('-c', '--csv', help="CSV file to export users.")

args = parser.parse_args()

if args.csv is None:
	sys.exit("Please provide a CSV file to export Users.")

if not os.path.isfile('config.config'):
	sys.exit("Configuration file is missing.")
	
config = configparser.ConfigParser()
config.read('config.config')

api = Gophish(config['DEFAULT']['API_KEY'], host=config['DEFAULT']['GOPHISH_URL'], verify=False)

with open(args.csv, 'w') as f:

	f.write('First Name,Last Name,Email,Position\n')

	groups = api.groups.get()
	groups.sort(key=lambda x: x.name)

	for group in groups:
		for user in group.targets:
			f.write("{},{},{},{}\n".format(user.first_name,user.last_name,user.email,user.position))

#end