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

parser = argparse.ArgumentParser('Create new Campaigns - Send emails')
parser.add_argument('-c', '--csv', help="A CSV file containing the neccessary information to create the new campaigns.")

args = parser.parse_args()

if args.csv is None:
	sys.exit("Please provide a CSV file containing the neccessary information to create the new campaigns..")

if not os.path.isfile(args.csv):
	sys.exit("Please provide an existing CSV file.")

if not os.path.isfile('config.config'):
	sys.exit("Configuration file is missing.")

config = configparser.ConfigParser()
config.read('config.config')

api = Gophish(config['DEFAULT']['API_KEY'], host=config['DEFAULT']['GOPHISH_URL'], verify=False)


campaigns = api.campaigns.get()
campaigns.sort(key=lambda x: x.name)
campaignsMap = {}

for campaign in campaigns:
	campaignsMap[campaign.name] = campaign

with open(args.csv, newline='') as csvfile:

	reader = csv.DictReader(csvfile)

	for row in reader:
		campaignName = row['CampaignName'].strip()

		if campaignName in campaignsMap:
			print("The campaign ({}) already exists in the GoPhish database.\n".format(campaignName))
			continue

		userGroupName = row['UserGroupName'].strip()
		emailTemplateName = row['EmailTemplateName'].strip()
		landingPageName = row['LandingPageName'].strip()
		sendingProfileName = row['SendingProfileName'].strip()
		gophishListener = row['GophishListener'].strip()
		
		groups = [Group(name=userGroupName)]
		page = Page(name=landingPageName)
		template = Template(name=emailTemplateName)
		smtp = SMTP(name=sendingProfileName)
		url = gophishListener
		campaign = Campaign(
		    name=campaignName, groups=groups, page=page, template=template, smtp=smtp, url=url)


		print("Creating New Campaign: {}".format(campaignName))

		try:
			campaign = api.campaigns.post(campaign)
			print("New Campaign ID: {}".format(campaign.id))
		except Exception:
			print('Campaign already exists.')
			continue

#end