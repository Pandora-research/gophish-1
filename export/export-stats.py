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

parser = argparse.ArgumentParser('Export GoPhish Statistics to CSV.')

parser.add_argument('-c', '--csv', help="CSV file to export Statistics.")

args = parser.parse_args()

if args.csv is None:
	sys.exit("Please provide a CSV file to export Statistics.")

if not os.path.isfile('config.config'):
	sys.exit("Configuration file is missing.")
	
config = configparser.ConfigParser()
config.read('config.config')

api = Gophish(config['DEFAULT']['API_KEY'], host=config['DEFAULT']['GOPHISH_URL'], verify=False)

with open(args.csv, 'w') as f:

	f.write('Status, First Name,Last Name,Email,Position, IP, Latitude, Longtitude\n')

	for campaign in api.campaigns.get():
		for result in campaign.results:
			f.write("{}, {}, {}, {}, {}, {}, {}, {}\n".format(
				result.status, result.first_name, result.last_name, result.email, 
				result.position, result.ip, result.latitude, result.longitude))

#end