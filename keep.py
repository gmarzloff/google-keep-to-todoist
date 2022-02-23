#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os, bs4, glob, unicodecsv as csv
from dateutil.parser import parse
from datetime import datetime
files = glob.glob("Keep/*.html")
notes = []

sub_tasks_mode = False 	# for parsing checklists
sub_tasks = []

# Ask for section title
print("Google Keep to Todoist CSV\n=================================")
section_title = input("Enter section title [Google Keep Notes]:") or "Google Keep Notes"

# Prep CSV file
now = datetime.now()
csvout = "notes_%s.csv" % now.strftime("%Y-%m-%d_%H%M")
writer = csv.writer(open(csvout, 'wb'))
writer.writerow(['TYPE', 'CONTENT', 'DESCRIPTION', 'PRIORITY', 'INDENT', 'AUTHOR', 'RESPONSIBLE', 'DATE', 'DATE_LANG', 'TIMEZONE', 'meta'])
writer.writerow(['section', section_title, '','','','','','','','','view_style=board'])

for file in files:
	print(file)
	page = open(file)
	soup = bs4.BeautifulSoup(page.read(), "html.parser")

	# Make Excel-Friendly date
	googDate = soup.select('.heading')[0].getText().strip()
	xlDate = datetime.strftime(parse(googDate), '%m/%d/%Y %H:%M')

	# Get title (aka content in todoist)
	if len(soup.select('.title')) == 0:
		title = ''
	else:
		title = soup.select('.title')[0].getText()

	# Parse Content (aka description in todoist)
	html = soup.select(".content")[0]
	
	# Convert checklists to subtasks
	try:
		checklist = html.select(".list")[0].select(".text")
		print("Checklist found. Converting to subtasks...")
		sub_tasks_mode = True
		for item in checklist:
			sub_tasks.append(item.text)
		html.decompose()
	except:
		pass
	
	# Handle embedded images
	# TODO
	# collect base64 data in .attachments/contents[]
	
	# Convert linebreaks
	for br in soup.find_all("br"):
		br.replace_with("\n")

	content = html.getText()
	
	note = {
		"date": xlDate,
		"content": title,
		"description": content
	}
	writer.writerow(['task', note['content'], note['description'], '', '', '', '', note['date'], '', '', ''])

	if sub_tasks_mode:
		for task in sub_tasks:
			writer.writerow(['task', task, '', '', '2', '', '', '', '', '', ''])
			
		sub_tasks = []
		sub_tasks_mode = False
	
print('\n'+'-'*50 + '\nDone! %s notes saved to %s\n' % (len(files), csvout))
