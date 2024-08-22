# https://canvasapi.readthedocs.io/en/stable/examples.html

# Import the Canvas class
from canvasapi import Canvas

import ssl
from shutil import copy2
from zipfile import ZipFile
from sys import argv, platform
from urllib.request import urlopen, urlretrieve
from os import listdir, mkdir, chdir, remove, system, walk, path

class InvalidConfigException(Exception):
    pass

def unzipper():
    dirs = listdir()
    for idir in dirs:
        if idir[-4:].lower() == ".zip":
            mkdir(idir[:-4])
            with ZipFile(idir, 'r') as zipObj:
              zipObj.extractall(path=idir[:-4])
            remove(idir)

def header(part):
    clear()
    if part == 1:
        print("Welcome to Jimmy's Student Assignment Downloader!")
    elif part == 2:
        print("Welcome to Jimmy's Student Rubric Generator!")

def clear():
    if platform.startswith("win32"):
        system("cls")
    else:
        system("clear")

def choice(values, part, name = lambda n : str(n)):
    x = -1
    while x < 0 or x >= i - 1:
        header(part)
        i = 1
        for value in values:
            print(str(i) + ": " + name(value))
            i += 1
        try:
            n = input("Number: ")
            x = int(n) - 1
        except:
            pass
    return values[x]

def get_rubrics():
    rubrics = []
    for root, dirs, files in walk(".."):
        for file in files:
            if file.startswith("Assignment") and file.endswith("-Rubric.xlsx"):
                rubrics.append(path.join(root, file)[3:])
    return choice(rubrics, 2)

def generate_rubrics(assignment, names):
    file = path.split(assignment)[-1][:-5]
    folder = file + "s"
    mkdir(folder)
    chdir(folder)
    for name in names:
        print(name + "-" + file)
        copy2(path.join("..", "..", "") + assignment, name + "-" + file + ".xlsx")

try:
    # SSL Fix
    ssl._create_default_https_context = ssl._create_unverified_context

    # Path Fix
    try:
        chdir(path.sep.join(argv[0].split(path.sep)[:-1]))
    except:
        pass

    # Clear default terminal stuff
    clear()

    # Canvas API
    try:
        cfg = open("Canvas.cfg", "x")
        print("First time setup!")
        institution = input("Institution: ")
        API_URL = "https://" + institution + ".instructure.com/"
        API_KEY = input("Canvas Token: ")
        COURSE_ID = input("Course ID: ")
        cfg.write(institution + "\n")
        cfg.write(API_KEY + "\n")
        cfg.write(COURSE_ID + "\n")
        cfg.close()
    except:
        cfg = open("Canvas.cfg")
        data = cfg.read().splitlines()
        if len(data) != 3:
            raise InvalidConfigException("Invalid config file detected. Please fix or delete the config file and try again.")
        API_URL = "https://" + data[0] + ".instructure.com/"
        API_KEY = data[1]
        COURSE_ID = data[2]
        cfg.close()

    # Initialize a new Canvas object
    canvas = Canvas(API_URL, API_KEY)

    # Get Assignment
    course = canvas.get_course(COURSE_ID)
    assignments = list(course.get_assignments())
    i = 0
    while i < len(assignments):
        if assignments[i].submission_types[0] != "online_upload":
            assignments.pop(i)
        else:
            i += 1
    assignment = choice(assignments, 1, lambda n : n.name)
    submissions = assignment.get_submissions()

    print()
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
            # Get Student Name
            student = str(course.get_user(submission.user_id))
            student = student[:student.index(" (")]

            # Blacklist Test Student
            if student == "Test Student":
                continue

            # Record Student Name
            print(student)
            names.append(student.replace(" ", "").replace("-", ""))

            # Download Assignment
            attachment = submission.attachments[0]
            urlretrieve(attachment.url, attachment.filename)
    unzipper()

    # Get Rubrics (For students that submitted)
    rubric = get_rubrics()
    print()
    print("Downloading please wait...")
    generate_rubrics(rubric, names)

    clear()
except Exception as error:
    # Error Report
    clear()
    print("\033[4mAn error occured\033[0m")
    print()
    print("ErrorType: " + type(error).__name__)
    print()
    print("ErrorMsg:  " + str(error))
    print()
    input("Press enter to close...")
