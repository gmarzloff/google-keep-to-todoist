#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os, bs4, glob, unicodecsv as csv
from dateutil.parser import parse
from datetime import datetime
files = glob.glob("Keep/*.html")
notes = []

#Prep CSV file
now = datetime.now()
csvout = "notes_%s.csv" % now.strftime("%Y-%m-%d_%H%M")
writer = csv.writer(open(csvout, 'wb'))
writer.writerow(['TYPE', 'CONTENT', 'DESCRIPTION', 'PRIORITY', 'INDENT', 'AUTHOR', 'RESPONSIBLE', 'DATE', 'DATE_LANG', 'TIMEZONE', 'meta'])
writer.writerow(['section', 'Google Keep Notes','','','','','','','','','view_style=board'])

for file in files:
	print(file)
	page = open(file)
	soup = bs4.BeautifulSoup(page.read(), "html.parser")

	#Make Excel-Friendly date
	googDate = soup.select('.heading')[0].getText().strip()
	xlDate = datetime.strftime(parse(googDate), '%m/%d/%Y %H:%M')

	#Get title
	if len(soup.select('.title')) == 0:
		title = ''
	else:
		title = soup.select('.title')[0].getText()

	#Parse Content
	html = soup.select(".content")[0]
	#Convert linebreaks
	for br in soup.find_all("br"):
		br.replace_with("\n")
	content = html.getText()
	
	note = {
		"date": xlDate,
		"content": title,
		"description": content
	}
	writer.writerow(['task', note['content'], note['description'], '', '', '', '', note['date'], '', '', ''])

print('\n'+'-'*50 + '\nDone! %s notes saved to %s\n' % (len(files), csvout))
