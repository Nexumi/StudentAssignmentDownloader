# https://canvasapi.readthedocs.io/en/stable/examples.html

# Import the Canvas class
from canvasapi import Canvas

import ssl
from shutil import copy2
from zipfile import ZipFile
from threading import Thread
from json import dumps, loads
from sys import argv, platform
from urllib.request import urlopen, urlretrieve
from os import listdir, mkdir, chdir, remove, system, walk, path

class InvalidConfigException(Exception):
    pass

def downloader(url, filename):
    urlretrieve(url, filename)
    if filename.endswith(".zip"):
        mkdir(filename[:-4])
        with ZipFile(filename, 'r') as zipObj:
            zipObj.extractall(path=filename[:-4])
        remove(filename)

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
            if n in ["!q", "quit", "cancel", "exit", "done"]:
                return False
            x = int(n) - 1
        except KeyboardInterrupt:
            return False
        except:
            pass
    return values[x]

def get_local_rubrics():
    rubrics = []
    for root, dirs, files in walk(".."):
        for file in files:
            if file.startswith("Assignment") and file.endswith("-Rubric.xlsx"):
                rubrics.append(path.join(root, file)[3:])
    return choice(rubrics, 2)

def generate_local_rubrics(assignment, names):
    file = path.split(assignment)[-1]
    folder = file[:-5] + "s"
    mkdir(folder)
    chdir(folder)
    for name in names:
        print(name + "-" + file)
        copy2(path.join("..", "..", "") + assignment, name + "-" + file)

def get_online_rubrics():
    data = urlopen(f"{config['RUBRIC_SOURCE']}rubrics.txt")
    rubrics = []
    for info in data:
        rubrics.append(info.decode("utf-8").strip("\n\r"))
    return choice(rubrics, 2)

def generate_online_rubrics(assignment, names):
    folder = assignment[:-5] + "s"
    mkdir(folder)
    chdir(folder)
    urlretrieve(config["RUBRIC_SOURCE"] + assignment, assignment)
    for name in names:
        print(name + "-" + assignment)
        copy2(assignment, name + "-" + assignment)
    remove(assignment)

def urlfix(url):
    if url:
        if not url.startswith("https://") and not url.startswith("http://"):
            url = f"https://{url}"
        if not url.endswith("/"):
            url += "/"
    return url

def main():
    global config

    # Canvas API
    clear()
    try:
        with open("Canvas.cfg", "x") as cfg:
            print("First time setup!")
            config = {
                "API_URL": "https://" + (institution := input("Institution: ")) + ".instructure.com/",
                "API_KEY": input("Canvas Token: "),
                "COURSE_ID": input("Course ID: "),
                "RUBRIC_SOURCE": urlfix(input("(Optional) Rubric Source: "))
            }
            cfg.write(dumps(config))
    except:
        with open("Canvas.cfg") as cfg:
            try:
                config = loads(cfg.read())
                if not config.get("API_URL") or not config.get("API_KEY") or not config.get("COURSE_ID"):
                    raise
            except:
                raise InvalidConfigException("Invalid config file detected. Please fix or delete the config file and try again.")


    # Initialize a new Canvas object
    canvas = Canvas(config["API_URL"], config["API_KEY"])

    # Get Assignment
    course = canvas.get_course(config["COURSE_ID"])
    assignments = list(course.get_assignments())
    i = 0
    while i < len(assignments):
        if assignments[i].submission_types[0] != "online_upload":
            assignments.pop(i)
        else:
            i += 1
    assignment = choice(assignments, 1, lambda n : n.name)
    if assignment:
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
        downloading = []
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
                downloading.append(Thread(target=downloader, args=(attachment.url, attachment.filename)))
                downloading[-1].start()
        for download in downloading:
            download.join()

        # Get Rubrics (For students that submitted)
        if config.get("RUBRIC_SOURCE"):
            get_rubrics = get_online_rubrics
            generate_rubrics = generate_online_rubrics
        else:
            get_rubrics = get_local_rubrics
            generate_rubrics = generate_local_rubrics

        rubric = get_rubrics()
        if rubric:
            print()
            print("Downloading please wait...")
            generate_rubrics(rubric, names)
    clear()

if __name__ == "__main__":
    try:
        # SSL Fix
        ssl._create_default_https_context = ssl._create_unverified_context

        # Path Fix
        try:
            chdir(path.sep.join(argv[0].split(path.sep)[:-1]))
        except:
            pass

        main()
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