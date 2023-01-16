#! python

import sys
import argparse
import shutil
import csv
import os

parser = argparse.ArgumentParser('Create HTML Templates for GoPhish')
parser.add_argument('-t', '--template', help="An HTML template to copy and replace links.")
parser.add_argument('-d', '--destination', help="Destination directory.")
parser.add_argument('-c', '--csv', help="Targets and URL codes CSV.")
parser.add_argument('-l', '--link', help="URL link to replace.")

args = parser.parse_args()

if args.template is None:
	sys.exit("Please provide a template.")

if not os.path.isfile(args.template):
	sys.exit("Please provide an existing template file.")

if args.destination is None:
	sys.exit("Please provide a destination directory.")

if not os.path.exists(args.destination):
	sys.exit("Please provide an existing destination directory.")

if args.csv is None:
	sys.exit("Please provide a CSV file containing the targets and the corresponding URL codes.")

if not os.path.isfile(args.csv):
	sys.exit("Please provide an existing CSV file.")

if args.link is None:
	sys.exit("Please provide a URL link to replace.")

with open(args.csv, newline='') as csvfile:

	reader = csv.DictReader(csvfile)

	for row in reader:

		name = row['Name'].strip().replace(" ", "_")
		code = row['Code'].strip()

		tempdest = os.path.join(args.destination, name + '-temp-' + '.txt')
		finaldest = os.path.join(args.destination, name + '.txt')

		if os.path.isfile(tempdest):
			os.remove(tempdest)

		shutil.copyfile(args.template, tempdest)

		with open(tempdest, "rt") as fin:
			with open(finaldest, "wt") as fout:
				for line in fin:
					fout.write(line.replace(args.link, args.link + '?' + code))
					
		os.remove(tempdest)

#end