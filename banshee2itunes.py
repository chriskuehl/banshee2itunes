#!/usr/bin/env python3
import sys, os.path, urllib.parse, sqlite3

# make an in-memory copy of the database in case Banshee changes it while
# we're using it
# 
# http://stackoverflow.com/q/4019081/612279
db = sqlite3.connect(":memory:")
live_db = sqlite3.connect(os.path.expanduser("~/.config/banshee-1/banshee.db"))

query = "".join(line for line in live_db.iterdump())
db.executescript(query)
db.commit()

live_db.close()

# get a complete list of tracks in Banshee
c = db.cursor()
c.execute("SELECT Uri FROM CoreTracks WHERE PrimarySourceID = 1")

for row in c:
	uri = urllib.parse.urlparse(row[0])

	if uri.scheme == "file":
		path = urllib.parse.unquote(uri.path)
		
		if not os.path.isfile(path):
			sys.stderr.write("File \"{}\" is in library but does not exist (?)".format(path))
