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

parser = argparse.ArgumentParser('Import HTML Templates to GoPhish')
parser.add_argument('-t', '--templates', help="Templates folder to upload to GoPhish.")
parser.add_argument('-s', '--subject', help="Email template subject.")


args = parser.parse_args()

if args.templates is None:
	sys.exit("Please provide a directory containing html templates.")

if not os.path.exists(args.templates):
	sys.exit("Please provide an existing templates directory.")

if not os.path.isfile('config.config'):
	sys.exit("Configuration file is missing.")

if args.subject is None:
	sys.exit("Please provide the subject of the email templates.")

config = configparser.ConfigParser()
config.read('config.config')

api = Gophish(config['DEFAULT']['API_KEY'], host=config['DEFAULT']['GOPHISH_URL'], verify=False)


for filename in os.listdir(args.templates):
	if filename.endswith(".txt"):
		f = os.path.join(args.templates, filename)
		if os.path.isfile(f):
			filename = os.path.splitext(filename)[0]
			filename = filename.replace(".", "_").replace(" ", "_")
			filename = filename.upper()
			with open(f, newline='') as htmlfile:
				html=htmlfile.read()
				template = Template(name=filename, html=html, subject=args.subject)
				template = api.templates.post(template)
				print('A new template has been imported with id {0}.'.format(template.id))

#end