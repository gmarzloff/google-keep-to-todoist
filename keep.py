#!/usr/bin/env python
# -*- coding: utf-8 -*-
import bs4, glob, unicodecsv as csv
from dateutil.parser import parse
from datetime import datetime
import json
import itertools
from operator import attrgetter
from collections import Counter


class Note:
    def __init__(self, title, listContent, textContent, timestamp, labels):
        self.listContent = listContent
        self.textContent = textContent
        self.title = title
        self.timestamp = datetime.fromtimestamp(float(timestamp)/1000000.0)
        self.labels = labels
    
    @property
    def description(self):
        print("listContent:", self.listContent, "\ntextContent:", self.textContent, "\ntitle:", self.title, "\ntimestamp:", self.timestamp, "\nlabel(s):", self.labels)

files = glob.glob("Keep/*.json")
notes = []
csvout = ""
writer = None

sub_tasks_mode = False  # for parsing checklists
sub_tasks = []

sub_tasks_counter = 0
checklist_counter = 0
parent_tasks_counter = 0
task_counter_for_current_csv_file = 0
csv_file_counter = 0


def create_new_csv_file():
    pass
#     global csv_file_counter, csvout, writer, task_counter_for_current_csv_file
#     csv_file_counter += 1
#     task_counter_for_current_csv_file = 0
#
#     csvout = "notes_%s_%s.csv" % (now.strftime("%Y-%m-%d_%H%M"), str(csv_file_counter))
#
#     writer = csv.writer(open(csvout, 'wb'))
#     writer.writerow(
#         ['TYPE', 'CONTENT', 'DESCRIPTION', 'PRIORITY', 'INDENT', 'AUTHOR', 'RESPONSIBLE', 'DATE', 'DATE_LANG',
#          'TIMEZONE', 'meta'])
#     writer.writerow(['section', section_title, '', '', '', '', '', '', '', '', 'view_style=board'])

# Parse JSON files to list
for file_path in files:
    # task_counter_for_current_csv_file += 1
    json_contents = ""
    file_obj = open(file_path, 'r')
    json_contents = json.load(file_obj)
    file_obj.close()

    note = Note(json_contents.get('title'),
                json_contents.get('listContent'),
                json_contents.get('textContent'),
                json_contents.get('createdTimestampUsec'),
                json_contents.get('labels'))
    notes.append(note)
    
    # print(note.description)
    
print(len(notes), "note objects loaded.\n\n")

# Run Label statistics
label_attr = attrgetter('labels')
notes_with_labels = [note for note in notes if label_attr(note) != None]
labels_from_list = [label['name'] for note_labels in [note.labels for note in notes_with_labels] for label in note_labels]
labels_summary = Counter(labels_from_list)
label_freq = labels_summary.most_common()
print("Label (Count)")
[print(item[0], item[1]) for item in label_freq]
print("Total notes with labels:",len(notes_with_labels),"\nKeep supports a one-note-to-many-labels relationship\n\n")

print("Todoist cannot import labels via its csv upload mechanism. If you use labels to categorize your notes in Keep,",
      "consider automatically creating Todoist projects for all Keep labels, and placing")


# new_list = [list(g) for k, g in itertools.groupby(sorted(notes, key=get_attr), get_attr)]
# print("List groups:")
# print(new_list)


#[n for n in notes if n.label != None]

# Prep CSV file
now = datetime.now()
create_new_csv_file()

# User inputs
print("Google Keep to Todoist CSV\n=================================")
section_title = input("Enter section title [Google Keep Notes]:") or "Google Keep Notes"
max_task_count_per_csv_file = int(input("Enter max task count per file [100]:") or 100)



# for file in files:
#     task_counter_for_current_csv_file += 1
#
#     print(file)
#     page = open(file)
#     soup = bs4.BeautifulSoup(page.read(), "html.parser")
#
#     # Make Excel-Friendly date
#     googDate = soup.select('.heading')[0].getText().strip()
#     xlDate = datetime.strftime(parse(googDate), '%m/%d/%Y %H:%M')
#
#     # Get title (aka content in todoist)
#     if len(soup.select('.title')) == 0:
#         title = ''
#     else:
#         title = soup.select('.title')[0].getText()
#
#     # Parse Content (aka description in todoist)
#     html = soup.select(".content")[0]
#
#     # Convert checklists to subtasks
#     try:
#         checklist = html.select(".list")[0].select(".text")
#         print("Checklist found. Converting to subtasks...")
#         checklist_counter += 1
#         sub_tasks_mode = True
#         for item in checklist:
#             sub_tasks.append(item.text)
#         html.decompose()
#     except:
#         pass
#
#     # Convert linebreaks
#     for br in soup.find_all("br"):
#         br.replace_with("\n")
#
#     content = html.getText()
#
#     note = {
#         "date": xlDate,
#         "content": title,
#         "description": content
#     }
#
#     # todoist will reject task without content (title), so copy part of the description
#     # to the content.
#     if len(note["content"]) == 0:
#         char_count = min(len(note['description']), 150)
#         note["content"] = note["description"][0:char_count]
#
#     if sub_tasks_mode:
#         # expected total row count in file after adding subtasks:
#         total = task_counter_for_current_csv_file + len(sub_tasks)
#     else:
#         total = task_counter_for_current_csv_file
#
#     if total > max_task_count_per_csv_file:
#         create_new_csv_file()
#
#     writer.writerow(['task', note['content'], note['description'], '4', '', '', '', note['date'], '', '', ''])
#     parent_tasks_counter += 1
#
#     if sub_tasks_mode:
#         for task in sub_tasks:
#             writer.writerow(['task', task, '', '4', '2', '', '', '', '', '', ''])
#             sub_tasks_counter += 1
#         sub_tasks = []
#         sub_tasks_mode = False
