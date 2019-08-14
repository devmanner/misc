#!/usr/bin/python

import pycurl
import StringIO
import json
from pprint import pprint
import argparse
import sys

parser = argparse.ArgumentParser(description='Conky Icinga warning checker. Add the following to your conky.conf:\n  ${color}${execi 60 python /home/tomas/repos/misc/icinga/bin/icinga_conky.py -c host:port -u user -p password}')
parser.add_argument('-c', type=str, dest="host", help='The host to connect to')
parser.add_argument('-u', type=str, dest="user", help='Username used for basic auth')
parser.add_argument('-p', type=str, dest="passwd", help='Password used for basic auth')
args = parser.parse_args()

response = StringIO.StringIO()
c = pycurl.Curl()
c.setopt(c.URL, "https://"+args.user+":"+args.passwd+"@"+args.host+'/v1/objects/services?filter=service.state!=ServiceOK')
c.setopt(c.WRITEFUNCTION, response.write)
c.setopt(c.HTTPHEADER, ['Content-Type: application/json'])
c.setopt(c.TIMEOUT, 5)

try:
	c.perform()
except pycurl.error:
	print " Failed to read data from: " + args.host
	sys.exit()

c.close()

jdata = json.loads(response.getvalue())

response.close()

for service in jdata['results']:
	print " " + service['attrs']['display_name'] + " @ " + service['attrs']['host_name']
	

