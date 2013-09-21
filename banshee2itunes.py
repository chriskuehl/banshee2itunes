#!/usr/bin/env python3
import sys, shutil, hashlib, os.path, urllib.parse, sqlite3

target_dir = os.path.expanduser("~/.banshee2itunes")

# remove the data directory if it exists
if os.path.lexists(target_dir):
	shutil.rmtree(target_dir)

os.makedirs(target_dir + "/music/")

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
			continue
		
		# the original idea was to use the file's hash as part of the 
		# name of the symlink, but that doesn't really provide any benefits
		# and can potentially result in many GBs of reads
		#
		# instead just hash the path
		hash_val = hashlib.sha1(path.encode("utf-8")).hexdigest()

		ext = os.path.splitext(path)[1].lower()
		os.symlink(path, target_dir + "/music/" + hash_val + ext)
