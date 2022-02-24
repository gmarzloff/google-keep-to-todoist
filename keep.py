#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os, bs4, glob, unicodecsv as csv
from dateutil.parser import parse
from datetime import datetime
files = glob.glob("Keep/*.html")
notes = []
csvout = ""
writer = None

sub_tasks_mode = False 	# for parsing checklists
sub_tasks = []

sub_tasks_counter = 0
checklist_counter = 0
parent_tasks_counter = 0
task_counter_for_current_csv_file = 0
csv_file_counter = 0

# User inputs
print("Google Keep to Todoist CSV\n=================================")
section_title = input("Enter section title [Google Keep Notes]:") or "Google Keep Notes"
max_task_count_per_csv_file = int(input("Todoist has trouble importing a large count. Enter max task count per file [100]:") or 100)

def create_new_csv_file():
	global csv_file_counter, csvout, writer, task_counter_for_current_csv_file
	csv_file_counter += 1
	task_counter_for_current_csv_file = 0
	
	csvout = "notes_%s_%s.csv" % (now.strftime("%Y-%m-%d_%H%M"), str(csv_file_counter))
	
	writer = csv.writer(open(csvout, 'wb'))
	writer.writerow(['TYPE', 'CONTENT', 'DESCRIPTION', 'PRIORITY', 'INDENT', 'AUTHOR', 'RESPONSIBLE', 'DATE', 'DATE_LANG', 'TIMEZONE', 'meta'])
	writer.writerow(['section', section_title, '','','','','','','','','view_style=board'])

# Prep CSV file
now = datetime.now()
create_new_csv_file()

for file in files:
	task_counter_for_current_csv_file += 1
	
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
		checklist_counter += 1
		sub_tasks_mode = True
		for item in checklist:
			sub_tasks.append(item.text)
		html.decompose()
	except:
		pass
	
	# Convert linebreaks
	for br in soup.find_all("br"):
		br.replace_with("\n")

	content = html.getText()
	
	note = {
		"date": xlDate,
		"content": title,
		"description": content
	}
	
	# todoist will reject task without content (title), so copy part of the description
	# to the content.
	if len(note["content"]) == 0:
		char_count = min(len(note['description']), 150)
		note["content"] = note["description"][0:char_count]
	
	if sub_tasks_mode:
		# expected total row count in file after adding subtasks:
		total = task_counter_for_current_csv_file + len(sub_tasks)
	else:
		total = task_counter_for_current_csv_file
		
	if total > max_task_count_per_csv_file:
		create_new_csv_file()
		
	writer.writerow(['task', note['content'], note['description'], '4', '', '', '', note['date'], '', '', ''])
	parent_tasks_counter += 1
	
	if sub_tasks_mode:
		for task in sub_tasks:
			writer.writerow(['task', task, '', '4', '2', '', '', '', '', '', ''])
			sub_tasks_counter += 1
		sub_tasks = []
		sub_tasks_mode = False
	
print('\n' +'-' * 50 + '\nDone! %s notes saved across %s .csv files.\n%s parent tasks created, %s checklists detected containing %s subtasks\n' % (len(files), csv_file_counter, parent_tasks_counter, checklist_counter, sub_tasks_counter))
