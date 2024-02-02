# https://canvasapi.readthedocs.io/en/stable/examples.html

# Import the Canvas class
from canvasapi import Canvas

import ssl
from shutil import copy2
from zipfile import ZipFile
from sys import argv, platform
from urllib.request import urlopen, urlretrieve
from os import listdir, mkdir, chdir, remove, system

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
        print(name + "-" + assignment)
        copy2(assignment, name + "-" + assignment)
    remove(assignment)

if platform.startswith("darwin"):
    ssl._create_default_https_context = ssl._create_unverified_context
    try:
        os.chdir(os.path.sep.join(argv[0].split(os.path.sep)[:-1]))
    except:
        pass

try:
    # Canvas API
    API_URL = "https://sfsu.instructure.com/"
    COURSE_ID = 31427
    try:
        cfg = open("CanvasToken.cfg", "x")
        print("First time setup!")
        API_KEY = input("Canvas Token: ")
        cfg.write(API_KEY + "\n")
        cfg.write(COURSE_ID)
        cfg.close()
    except:
        cfg = open("CanvasToken.cfg")
        API_KEY = cfg.read()
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
    assignment = choice(assignments, 1)
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
            print(student)
            names.append(student.replace(" ", ""))

            # Download Assignment
            attachment = submission.attachments[0]
            urlretrieve(attachment.url, attachment.filename)
    unzipper()

    # Get Rubrics (For students that submitted)
    rubric = get_rubrics();
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