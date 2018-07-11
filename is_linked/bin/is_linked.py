#!/usr/bin/python

import time
import re
import argparse
import os
from io import BytesIO
from lxml import etree

def has_link(fname):
	import zipfile
	import tempfile
	import shutil
	from subprocess import call

	re_xmlfile = re.compile(".*\\.xml$|.*\\.xml\\.rels$")

	tempdir = tempfile.mkdtemp()

	zip_ref = zipfile.ZipFile(fname, 'r')
	zip_ref.extractall(tempdir)
	zip_ref.close()

	# Sloppy check. This is a spped-up trick
	ret = call(["grep", "-qR", "TargetMode=\"External\"", tempdir])

	if ret == 0:
		for root, directories, filenames in os.walk(tempdir):
			for filename in filenames: 
				if re_xmlfile.match(filename) is not None:
					if xml_has_link(os.path.join(root,filename)):
						shutil.rmtree(tempdir)
						return True
	shutil.rmtree(tempdir)
	return False

def is_path(s):
	prog = re.compile("^file:///")
	result = prog.match(s)
	return result is not None

def is_oleObject(x):
	return x == "http://schemas.openxmlformats.org/officeDocument/2006/relationships/oleObject"
def is_externalLinkPath(x):
	return x == "http://schemas.openxmlformats.org/officeDocument/2006/relationships/externalLinkPath"

def xml_has_link(fname):
	tree = etree.parse(fname)
	for x in tree.findall(".//*[@TargetMode='External']"):
#		print x.tag
#		print x.attrib
#		print x.attrib["Target"]
		if is_path(x.attrib["Target"]) and is_oleObject(x.attrib["Type"]):
			return True
		if is_externalLinkPath(x.attrib["Type"]):
			return True
	return False

parser = argparse.ArgumentParser(description='Check if a pptx or xlsx file contains external links. Return 1 if file contain link')
parser.add_argument('-v', action='store_true', help='Verbose mode')
parser.add_argument('file', metavar='FILE', type=argparse.FileType('r'), nargs=1, help='The excel file to check')
args = parser.parse_args()

fname = args.file[0].name

if has_link(fname):
	statbuf = os.stat(fname)
	print(fname + " link found. Last modified: %s" % time.ctime(os.path.getmtime(fname)))
	exit(1)
if args.v:
	print(fname + " contain no link")
exit(0)

