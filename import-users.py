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

parser = argparse.ArgumentParser('Import Users into GoPhish')
parser.add_argument('-c', '--csv', help="Targets CSV.")


args = parser.parse_args()

if args.csv is None:
	sys.exit("Please provide a CSV file containing the targets.")

if not os.path.isfile(args.csv):
	sys.exit("Please provide an existing CSV file.")

config = configparser.ConfigParser()
config.read('config.config')

api = Gophish(config['DEFAULT']['API_KEY'], host=config['DEFAULT']['GOPHISH_URL'], verify=False)


with open(args.csv, newline='') as csvfile:
	reader = csv.DictReader(csvfile)
	for row in reader:
		firstname = row['First Name'].strip()
		lastname = row['Last Name'].strip()
		email = row['Email'].strip()
		#position = row['Position'].strip()
		groupname = firstname+'_'+lastname
		groupname = groupname.upper()
		targets = [User(first_name=firstname, last_name=lastname, email=email)]#, position=position
		group = Group(name=groupname, targets=targets)
		group = api.groups.post(group)
		print('A new user group has been imported with id {0}.'.format(group.id))

#end