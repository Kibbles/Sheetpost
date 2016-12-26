import uu
import gspread
import sys
import os
from oauth2client.service_account import ServiceAccountCredentials


# AUTH
# -------------------------------------------------------]]
# Authentication files & configuration.
# Be sure to replace your own json file name here.
# See here for details:
# https://gspread.readthedocs.io/en/latest/oauth2.html
# -------------------------------------------------------]]

# Insert the path & name of your own .json auth file here.
# This is the only thing you need to edit in the script itself.
json_file = '[your file here].json'
scope = ['https://spreadsheets.google.com/feeds']
credentials = ServiceAccountCredentials.from_json_keyfile_name(json_file, scope)


# Split a string into chunks so we can work around
# the Google Sheets' per-cell value limit.
def chunk_str(bigchunk, chunk_size):
    return [bigchunk[i:i + chunk_size] for i in range(0, len(bigchunk), chunk_size)]


# UPLOAD
# -------------------------------------------------------]]
# File upload process for 'put'.
# -------------------------------------------------------]]
def sheetpost_put(sheet_id, filename):
    try:
        gc = gspread.authorize(credentials)
        print "Logged into Sheets!"
    except Exception:
        sys.exit("Error logging into Google Sheets. Check your authentication.")

    # Set a name and path for your to-be-uploaded file

    # UU-encode the source file
    uu.encode(filename, filename + ".out")

    print "Encoded file into uu format! Starting the upload.\nThis'll take a while."

    with open(filename + ".out", "rb") as uploadfile:
        encoded = uploadfile.read()
    uploadfile.close()

    # Write the chunks to Drive
    cell = 1
    chunk = chunk_str(encoded, 45000)
    wks = gc.open_by_key(sheet_id).sheet1

    for part in chunk:
        part = "'" + part
        wks.update_cell(cell, 1, part)
        cell += 1

    # Delete the UU-encoded file
    os.remove(filename + ".out")
    print "All done! " + str(cell) + " cells filled in Sheets."


# DOWNLOAD
# -------------------------------------------------------]]
# File download process for 'get'.
# -------------------------------------------------------]]
def sheetpost_get(sheet_id, filename):

    downfile = filename + ".uu"

    try:
        gc = gspread.authorize(credentials)
        wks = gc.open_by_key(sheet_id).sheet1
        print "Logged into Sheets! Downloading the UU spaghetti. This might take a bit."
    except Exception:
        sys.exit("Error logging into Google Sheets.\n Check your authentication and make sure you"
                 "gave it a sheetpost to work with.")

    # Trim out the extra single quotes
    values_list = wks.col_values(1)
    for value in values_list:
        value = value[1:]
    values_list = "".join(values_list)

    # Save to file
    with open(downfile, "w") as recoverfile:
        recoverfile.write(values_list)
    recoverfile.close()

    print "Saved Sheets data to decode! Decoding now. Beep boop."
    uu.decode(downfile, filename)
    os.remove(downfile)
    print "Data decoded! All done!"

# HELP
# -------------------------------------------------------]]
# The help message that displays if none or too
# few arguments are given to properly execute.
# -------------------------------------------------------]]
help_message = '''To upload a sheetpost:
\t sheetpost.py put [GSheets key from URL] [Input filename]"
To retrieve a sheetpost:
\t sheetpost.py get [GSheets key from URL] [Output filename]"'''


# MAIN
# -------------------------------------------------------]]
# Where the magic happens!
# -------------------------------------------------------]]
if len(sys.argv) <= 2:
    print "Too few arguments!"
    sys.exit(help_message)

sheet_id = str(sys.argv[2])
filename = str(sys.argv[3])

if sys.argv[1] == "put":
    sheetpost_put(sheet_id, filename)

elif sys.argv[1] == "get":
    sheetpost_get(sheet_id, filename)

else:
    print "Unknown operation (accepts either 'get' or 'put')"
    sys.exit(help_message)
