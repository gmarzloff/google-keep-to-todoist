# Google Keep Scraper to Todoist
Apparently there's no simple way to export your notes from Google Keep to CSV. 
This script accepts the Keep folder Google Takeout archive, and outputs all of the Keep notes as lines in a 
single CSV file.

This fork modifies the CSV output to todoist format for easy importing. CSV structure is based on the [todoist documentation](https://todoist.com/help/articles/how-to-format-your-csv-file-so-you-can-import-it-into-todoist).   

## Install
1. Clone or download this repository
1. Open a terminal to the repository folder (`google-keep-to-todoist`)
1. Run `pip install -r requirements.txt` to install dependencies

## Run
First we need to download all the Keep files through Google Takeout.
1. Go to [Google Takeout](https://takeout.google.com/settings/takeout)
2. Make sure the 'Keep' checkbox is selected (you can deselect all others)
3. Download and export the archive to a folder that has the 'Keep' folder
4. Move the `Keep` folder into this folder, so it's alongside `keep.py`
5. If you have multiple Takeout folders, move the `.html` files within each `Keep` folder so they are all in the same `Keep` folder.   
6. Run `python keep.py`
7. All of your Keep notes should be exported to CSV in the same folder

## Import to Todoist

In the top right of Todoist, click the three dots then "Import from template"

![Import](img/import.png)

## Troubleshooting
If you get an error about a missing dependency, be sure to run `pip install -r requirements.txt` prior to running the script so that it can download the dependencies needed.
