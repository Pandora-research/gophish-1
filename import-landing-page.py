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

parser = argparse.ArgumentParser('Import Landing page into GoPhish')

parser.add_argument('-n', '--name', type=str, help="SMTP profile name.")
parser.add_argument('-p', '--html', help="HTML page.")

args = parser.parse_args()

if args.name is None:
	sys.exit("Please provide a Landing page name.")

if args.html is None:
	sys.exit("Please provide an HTML page containing the landing page.")

if not os.path.isfile(args.html):
	sys.exit("Please provide an existing HTML file.")

config = configparser.ConfigParser()
config.read('config.config')

api = Gophish(config['DEFAULT']['API_KEY'], host=config['DEFAULT']['GOPHISH_URL'], verify=False)

with open(args.html, newline='') as htmlfile:
	html=htmlfile.read()
	page = Page(name=args.name, html=html)
	page = api.pages.post(page)
	print("Landing page ID: {}".format(page.id))

#end