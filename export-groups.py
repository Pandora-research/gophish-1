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

parser = argparse.ArgumentParser('Export GoPhish User Groups to CSV.')

parser.add_argument('-c', '--csv', help="CSV file to export user groups.")

args = parser.parse_args()

if args.csv is None:
	sys.exit("Please provide a CSV file to export User Groups.")

config = configparser.ConfigParser()
config.read('config.config')

api = Gophish(config['DEFAULT']['API_KEY'], host=config['DEFAULT']['GOPHISH_URL'], verify=False)

with open(args.csv, 'w') as f:

	f.write('User Group Name,Email Template Name')

	groups = api.groups.get()
	groups.sort(key=lambda x: x.name)

	for group in groups:
		f.write("{},\n".format(group.name))

#end