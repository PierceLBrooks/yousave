
# Author: Pierce Brooks

import os
import sys
import pytube
import inspect
import subprocess

def cwd():
	result = ""
	frame = inspect.currentframe()
	try:
		script = inspect.getsourcefile(frame)
		result = [os.path.realpath(os.path.dirname(script)), os.path.basename(script)]
	finally:
		del frame
	return result

def	convert(path, base, name):
	new = os.path.join(base, name+".mp3")
	try:
		command = []
		command.append("ffmpeg")
		command.append("-i")
		command.append(path)
		command.append(new)
		result = subprocess.check_output(command)
		os.remove(path)
	except Exception as error:
		print("Convert error @ "+new)
		print(error)
		new = None
	return new

def save(index, base, video, title, extension):
	name = title
	path = os.path.join(base, name+extension)
	try:
		video.download(base, name)
	except Exception as error:
		print("Save error @ "+path)
		print(error)
		name = str(index)
		path = os.path.join(base, name+extension)
		try:
			video.download(base, name)
		except Exception as error:
			print("Save error @ "+path)
			print(error)
			path = None
	if not (path == None):
		print(title+" -> "+path)
		if not (convert(path, base, name)):
			path = None
	return path

def work(index, base, target):
	temp = None
	try:
		remote = pytube.YouTube(target)
		title = remote.title
		videos = remote.streams.all()
		extension = None
		print(target+" -> "+title)
		for video in videos:
			tag = str(video)
			if ("audio/mp4" in tag):
				extension = True
				break
			else:
				if ("audio/webm" in tag):
					extension = False
					break
		if not (extension == None):
			if (extension):
				temp = save(index, base, video, title, ".mp4")
			else:
				temp = save(index, base, video, title, ".webm")
		else:
			print("No suitable format...")
	except Exception as error:
		print("Work error @ "+target)
		print(error)
	return temp

def run(target):
	success = True
	try:
		info = cwd()
		base = info[0]
		script = info[1]
		print(base)
		print(script)
		path = os.path.join(base, target)
		handle = open(path, "r")
		lines = handle.readlines()
		handle.close()
		paths = []
		index = 0
		for line in lines:
			temp = line.strip()
			if (len(temp) > 0):
				path = work(index, base, temp)
				if not (path == None):
					paths.append(path)
			index += 1
		path = os.path.join(base, script)
		path += "_output.txt"
		handle = open(path, "w")
		for path in paths:
			print(path)
			handle.write(path+"\n")
		handle.close()
	except Exception as error:
		print("Run error")
		print(error)
		success = False
	return success

if (__name__ == "__main__"):
	args = sys.argv
	if (len(args) == 2):
		if (run(args[1])):
			sys.exit(0)
		else:
			sys.exit(-1)
