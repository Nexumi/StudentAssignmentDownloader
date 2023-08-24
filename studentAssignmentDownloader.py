# https://canvasapi.readthedocs.io/en/stable/examples.html

# Import the Canvas class
import os
from canvasapi import Canvas
from zipfile import ZipFile
from urllib.request import urlopen, urlretrieve

def unzipper():
    zips = os.listdir()
    i = 0
    while i < len(zips):
        if zips[i][-4:].lower() != ".zip":
            zips.pop(i)
        else:
            i += 1
    for izip in zips:
        os.mkdir(izip[:-4])
        with ZipFile(izip, 'r') as zipObj:
          zipObj.extractall(path=izip[:-4])
        os.remove(izip)

def header():
    clear()
    print("Welcome to Jimmy's Student Assignment Downloader!")

def clear():
    if os.name == "nt":
        os.system("cls")
    else:
        os.system("clear")

def choice(values):
    x = -1
    while x < 0 or x >= i - 1:
        header()
        i = 1
        for value in values:
            print(str(i) + ": " + str(value))
            i += 1
        try:
            x = int(input("Number: ")) - 1
        except:
            pass
    return values[x]

# Canvas API URL
API_URL = "https://sfsu.instructure.com/"

try:
	file = open("CanvasToken.txt", "x")
	file.close()
	input("Canvas Token not found! Please enter your Canvas Token into the CanvasToken.txt file then try again.")
except:
	# Canvas API key
	file = open("CanvasToken.txt")
	API_KEY = file.read()
	file.close()

	# Initialize a new Canvas object
	canvas = Canvas(API_URL, API_KEY)

	# CSC 215 - Fall 2023
	course = canvas.get_course(26589)

	assignments = course.get_assignments()

	assignment = choice(assignments)

	submissions = assignment.get_submissions()

	os.mkdir(str(assignment))
	os.chdir(str(assignment))

	for submission in submissions:
		if len(submission.attachments):
			attachment = submission.attachments[0]
			urlretrieve(attachment.url, attachment.filename)
			unzipper()