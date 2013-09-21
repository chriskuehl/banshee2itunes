#!/usr/bin/env python3
import sys, os, os.path

def make_m3u(path):
	m3u = "#EXTM3U\n\n"

	for file in os.listdir(path):
		filePath = path + "/" + file
		ext = os.path.splitext(filePath)[1]

		if ext in [".mp3", ".m4a", ".wav", ".aif"]:
			m3u += "#EXTINF,0,{}\n{}\n\n".format(filePath, filePath)
	
	return m3u

# kill iTunes
os.system("killall iTunes 2>/dev/null")

# remove the iTunes library files
files = ["iTunes Music Library.xml", "iTunes Library.itl"]

for file in files:
	path = os.path.expanduser("~/Music/iTunes/" + file)
	
	if os.path.isfile(path):
		os.remove(os.path.expanduser(path))

# launch iTunes so that it creates new library files
os.system("/Applications/iTunes.app/Contents/MacOS/iTunes &")
os.system("sleep 3 && killall iTunes 2>/dev/null")

exit(0)

# generate an M3U playlist with all of the files
m3u = make_m3u(os.path.expanduser("~/Desktop/music"))

if os.path.isfile("/tmp/music.m3u"):
	os.remove("/tmp/music.m3u")

with open("/tmp/music.m3u", "w") as file:
	file.write(m3u)


