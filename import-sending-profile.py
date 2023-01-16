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

parser = argparse.ArgumentParser('Import Sending profile into GoPhish')

parser.add_argument('-n', '--name', type=str, help="SMTP profile name.")
parser.add_argument('-x', '--host', type=str, help="SMTP host.")
parser.add_argument('-p', '--port', type=str, help="SMTP port.")
parser.add_argument('-f', '--fromaddr', type=str, help="SMTP From address.")


args = parser.parse_args()

if args.name is None:
	sys.exit("Please provide an SMTP profile name.")

if args.host is None:
	sys.exit("Please provide an SMTP Host.")

if args.port is None:
	sys.exit("Please provide an SMTP Port.")

if args.fromaddr is None:
	sys.exit("Please provide an SMTP From address.")

config = configparser.ConfigParser()
config.read('config.config')

api = Gophish(config['DEFAULT']['API_KEY'], host=config['DEFAULT']['GOPHISH_URL'], verify=False)

smtp = SMTP(name=args.name)
smtp.host = "{}:{}".format(args.host, args.port)
smtp.from_address = args.fromaddr
smtp.interface_type = "SMTP"
smtp.ignore_cert_errors = True

smtp = api.smtp.post(smtp)
print("SMTP profile ID: {}".format(smtp.id))

#end