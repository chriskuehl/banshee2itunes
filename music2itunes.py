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

# generate an M3U playlist with all of the files
m3u = make_m3u(os.path.expanduser("~/Desktop/music"))
print(m3u)
