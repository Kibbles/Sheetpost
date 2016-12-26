# Sheetpost
[p1]: https://github.com/Kibbles/Sheetpost/blob/master/screenshots/p1.png
[p2]: https://github.com/Kibbles/Sheetpost/blob/master/screenshots/p2.png
[p3]: https://github.com/Kibbles/Sheetpost/blob/master/screenshots/p3.png

## WHAT
Upload & download UU-encoded data with Google Sheets.

![p1]

![p2]

![p3]

This abomination uses [uu](http://linux.die.net/man/1/uuencode) and [gspread](https://github.com/burnash/gspread) to post single files to Google Sheets. You can encode videos, music, pictures and more in a hilariously inefficient manner that won't count towards your Google Drive storage space. There is no size limit I am aware of; the largest file I tested it with was 200MB.

Uploading takes forever, but downloading is surprisingly snappy.

## WHY
Why not!

## Setup
You'll need gspread and oauth2client.
```pip install gspread

pip install oauth2client```

gspread requires valid Drive API credentials for use in OAuth2. [Here's how to do this](https://gspread.readthedocs.io/en/latest/oauth2.html).

On line 16 in sheetpost.py, edit the following value:
```
json_file = '[your file here].json'
```

Additionally, you'll need to spoonfeed it a Google Sheet to start off with (via key, which is found in the URL when opening the spreadsheet in a browser), and that blank sheet must be "shared" with the service account you created (so the program can write to it).

## Usage

To sheetpost:
```
sheetpost.py put [GSheets key from URL] [Input filename]
```
This will delete all previously existing content in the target sheet.

To retrieve a sheetpost:
```
sheetpost.py get [GSheets key from URL] [Output filename]
```

Example:

```
sheetpost.py put 1cagGaHFBk5rFjJ6klMRwdVsUvTgslWtg9x8B-rz5C-I "C:\potato\potato.png"

sheetpost.py get 1cagGaHFBk5rFjJ6klMRwdVsUvTgslWtg9x8B-rz5C-I "C:\potato\reassembled_potato.png"
```

Note that sheetpost has no idea what format your files actually are, so you'll have to somehow remember what each sheetpost contains.

You could use a spreadsheet to keep track of that.


## Quirks
- Uploading is slow. A 5MB file takes roughly ~3 minutes. Download is a lot faster though!
- It doesn't support multiple files, but you can upload a .zip or .7z archive.
- Google Sheets has a hardcoded character limit of 50,000 per cell. Sheetpost utilizes 49,500 character per cell, just to be safe. You can probably tweak this and gain some more "performance".
- Sheets interprets a cell starting with "=" as a formula. To combat this, Sheetpost prepends every single line with a single quote (').
This is stupid, but it works. The `get` mode consequently trims out the first single quote per cell when reassembling the file.
- If you open your Sheet in a browser after an upload, it ~~might~~ *WILL* vomit blood.
