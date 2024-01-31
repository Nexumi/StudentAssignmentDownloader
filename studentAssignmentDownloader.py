# https://canvasapi.readthedocs.io/en/stable/examples.html

# Import the Canvas class
from canvasapi import Canvas

import ssl
from sys import platform
from shutil import copy2
from zipfile import ZipFile
from urllib.request import urlopen, urlretrieve
from os import listdir, mkdir, chdir, remove, system, name

def unzipper():
    zips = listdir()
    i = 0
    while i < len(zips):
        if zips[i][-4:].lower() != ".zip":
            zips.pop(i)
        else:
            i += 1
    for izip in zips:
        mkdir(izip[:-4])
        with ZipFile(izip, 'r') as zipObj:
          zipObj.extractall(path=izip[:-4])
        remove(izip)

def header(part):
    clear()
    if part == 1:
        print("Welcome to Jimmy's Student Assignment Downloader!")
    elif part == 2:
        print("Welcome to Jimmy's Student Rubric Generator!")

def clear():
    if name == "nt":
        system("cls")
    else:
        system("clear")

def choice(values, part):
    x = -1
    while x < 0 or x >= i - 1:
        header(part)
        i = 1
        for value in values:
            value = str(value)
            try:
                print(str(i) + ": " + value[:value.index(" (")])
            except:
                print(str(i) + ": " + value)
            i += 1
        try:
            x = int(input("Number: ")) - 1
        except:
            pass
    return values[x]

def get_rubrics():
    data = urlopen("https://web.jpkit.us/grader-rubrics/rubrics.txt")
    rubrics = []
    for info in data:
        rubrics.append(info.decode("utf-8").replace("\n", ""))
    return choice(rubrics, 2)

def generate_rubrics(assignment, names):
    folder = assignment[:-5] + "s"
    mkdir(folder)
    chdir(folder)
    urlretrieve("https://web.jpkit.us/grader-rubrics/" + assignment, assignment)
    for name in names:
        copy2(assignment, name + "-" + assignment)
    remove(assignment)

if platform.startswith("darwin"):
    ssl._create_default_https_context = ssl._create_unverified_context
    try:
        os.chdir(os.path.sep.join(argv[0].split(os.path.sep)[:-1]))
    except:
        pass

# Canvas API URL
API_URL = "https://sfsu.instructure.com/"

# Canvas API key
try:
    file = open("CanvasToken.cfg", "x")
    API_KEY = input("Canvas Token not found! Please enter your Canvas Token: ")
    file.write(API_KEY)
    file.close()
except:
    file = open("CanvasToken.cfg")
    API_KEY = file.read()
    file.close()

# Initialize a new Canvas object
canvas = Canvas(API_URL, API_KEY)

# Get Assignment
course = canvas.get_course(31427)
assignments = course.get_assignments()
assignment = choice(assignments, 1)
submissions = assignment.get_submissions()

print("Downloading please wait...")

# Generate Folder
folder = str(assignment)
folder = folder[:folder.index(" (")]
try:
    mkdir(folder)
except:
    i = 1
    while True:
        try:
            mkdir(folder + " (" + str(i) + ")")
            folder += " (" + str(i) + ")"
            break
        except:
            i += 1
chdir(folder)

# Getting Information
names = []
for submission in submissions:
    if len(submission.attachments):
        # Download Assignment
        attachment = submission.attachments[0]
        urlretrieve(attachment.url, attachment.filename)

        # Get Student Name
        student = str(course.get_user(submission.user_id))
        student = student[:student.index(" (")].replace(" ", "")
        names.append(student)
unzipper()

# Get Rubrics (For students that submitted)
rubric = get_rubrics();
print("Downloading please wait...")
generate_rubrics(rubric, names)

clear()