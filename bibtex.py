#!/usr/bin/python2.7

# Created on Nov 21, 2012
# @author: laura

import os

def read_folder(folder):
	items = []
	for root, dirs, files in os.walk(folder):
		for f in files:
			if f.endswith(".bib"):
				read_bibtex_file(root+"/"+f, items)
	return items

def read_bibtex_file(bib, items):
	print bib
	f = open(bib,'r')
	current = None
	for line in f:
		line = trim(line)
		if line.startswith('@'):
			if current != None:
				items.append(current)
			current = []
		current.append(line)
	items.append(current)

def parse(item):
	bib_id = ""
	bib_author = ""
	bib_title = ""
	bib_year = 0
	for line in item:
		if line.startswith('@'):
			bib_id = line.split('{')[1].split(',')[0]
		else:
			keys = line.split('=')
			if len(keys) == 2 :
				key = trim(keys[0]).lower()
				value = trim(keys[1])
			if key == "author" :
				bib_author = extract_authors(clean(value))
			elif key == "title" :
				bib_title = clean(value)
			elif key == "year" :
				bib_year = clean(value)
	return {"id":bib_id, "author":bib_author, "title":bib_title, "year":bib_year}

def extract_authors(string):
	authors = []
	parts = string.split("and")
	for part in parts:
		authors.append(trim(part))
	return authors

def trim(s):
	return s.lstrip().rstrip()

def clean(s):
	return s.lstrip('{').rstrip('},')


items = read_folder("/home/laura/Projects/bibtex2html/")
for item in items:
	print repr(parse(item))

