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


parser = argparse.ArgumentParser('Import Users into GoPhish')

parser.add_argument('-c', '--csv', help="Targets CSV.")
parser.add_argument('-n', '--name', type=str, help="Users Group name.")
parser.add_argument('-t', '--tracking_codes', action='store_true', help="Generate Tracking codes, they will be stored in the position field.")
parser.add_argument('-l', '--tc_length', type=int, default=12, help="Tracking code length (default: 12).")
parser.add_argument('-g', '--group_per_user', action='store_true', help="Create a new group for each new user.")

args = parser.parse_args()

if args.csv is None:
	sys.exit("Please provide a CSV file containing the emails of the targets.")

if not os.path.isfile(args.csv):
	sys.exit("Please provide an existing CSV file.")

if args.name is None and not args.group_per_user:
	sys.exit("Please provide a Group name.")

if not os.path.isfile('config.config'):
	sys.exit("Configuration file is missing.")
	
config = configparser.ConfigParser()
config.read('config.config')

api = Gophish(config['DEFAULT']['API_KEY'], host=config['DEFAULT']['GOPHISH_URL'], verify=False)


with open(args.csv, newline='') as csvfile:

	reader = csv.DictReader(csvfile)

	if args.group_per_user:

		for row in reader:
			firstname = row['First Name'].strip()
			lastname = row['Last Name'].strip()
			email = row['Email'].strip()

			if args.tracking_codes:
				position = ''.join(random.choices(string.ascii_uppercase + string.ascii_lowercase + string.digits, k=args.tc_length))
			else:
				position = row['Position'].strip()

			targets = [User(first_name=firstname, last_name=lastname, email=email, position=position)]

			groupname = firstname.replace(".", "")+'_'+lastname.replace(".", "")
			groupname = groupname.upper()

			print('Creating new User group ({}, {}).'.format(firstname, lastname))

			group = Group(name=groupname, targets=targets)

			try:
				group = api.groups.post(group)
				print('New User group ID ({}, {}): {}.'.format(firstname, lastname, group.id))
			except Exception:
				print('User group already exists.')
				continue

	else:

		targets = []

		for row in reader:
			firstname = row['First Name'].strip()
			lastname = row['Last Name'].strip()
			email = row['Email'].strip()

			if args.tracking_codes:
				position = ''.join(random.choices(string.ascii_uppercase + string.ascii_lowercase + string.digits, k=args.tc_length))
			else:
				position = row['Position'].strip()

			targets.append(User(first_name=firstname, last_name=lastname, email=email, position=position))


		groupname = args.name

		group = Group(name=groupname, targets=targets)
		
		group = api.groups.post(group)

		print('New User group ID ({}, {}): {}.'.format(firstname, lastname, group.id))
		

#end