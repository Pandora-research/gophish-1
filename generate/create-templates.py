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

parser = argparse.ArgumentParser('Create HTML Templates for GoPhish')
parser.add_argument('-c', '--csv', help="A CSV file containing the User Groups names and their corresponding email templates filenames.")
parser.add_argument('-t', '--templates_dir', help="A directory containing all the email templates.")
parser.add_argument('-d', '--destination', help="Destination directory.")

TrackingCode_Template ='[tracking_code]'

args = parser.parse_args()

if args.csv is None:
	sys.exit("Please provide a CSV file containing the User Groups names and their corresponding email templates filenames.")

if not os.path.isfile(args.csv):
	sys.exit("Please provide an existing CSV file.")

if args.templates_dir is None:
	sys.exit("Please provide the directory which contains all the email templates.")

if not os.path.exists(args.templates_dir):
	sys.exit("Please provide an existing templates directory.")

if args.destination is None:
	sys.exit("Please provide a destination directory for the generated email templates.")

if not os.path.exists(args.destination):
	sys.exit("Please provide an existing destination directory.")

if not os.path.isfile('config.config'):
	sys.exit("Configuration file is missing.")
	
config = configparser.ConfigParser()
config.read('config.config')

api = Gophish(config['DEFAULT']['API_KEY'], host=config['DEFAULT']['GOPHISH_URL'], verify=False)

groups = api.groups.get()
groups.sort(key=lambda x: x.name)
groupsMap = {}

for group in groups:
	groupsMap[group.name] = group

with open(args.csv, newline='') as csvfile:

	reader = csv.DictReader(csvfile)

	for row in reader:

		groupName = row['UserGroupName'].strip()
		templateFilename = row['EmailTemplateFilename'].strip()
		templatePath = os.path.join(args.templates_dir, templateFilename)

		if groupName not in groupsMap:
			print("The user group name ({}) does not exist in the GoPhish database.\n".format(groupName))
			continue

		if not os.path.isfile(templatePath):
			print("The email template file ({}) does not exist in the directory.\n".format(templatePath))
			continue

		for target in groupsMap[groupName].targets:
			#target.position contains user tracking code

			tempdest = os.path.join(args.destination, groupName + '-temp-' + '.txt')
			finaldest = os.path.join(args.destination, groupName + '.txt')

			if os.path.isfile(tempdest):
				os.remove(tempdest)

			shutil.copyfile(templatePath, tempdest)

			print("Creating email template file for Group {}.\n".format(groupName))

			with open(tempdest, "rt") as fin:
				with open(finaldest, "wt") as fout:
					for line in fin:
						fout.write(line.replace(TrackingCode_Template, target.position))
					
			os.remove(tempdest)

#end