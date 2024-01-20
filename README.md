# studentAssignmentDownloader

> Downloads, unpacks, and generates rubrics for all of your student’s assignments.

## Support
✔️ Windows

✔️ MacOS

✔️ Linux

## Direct Run
- Install [Python](https://www.python.org/)
- Open terminal in folder containing the program
- Run `pip install canvasapi` (Only needs to be run once)
- Run `python studentAssignmentDownloader.py`
- Profit

## Self Compilation
- Install [Python](https://www.python.org/)
- Install [PyInstaller](https://pyinstaller.org/en/stable/)
- (Optional) Download [UPX](https://upx.github.io/)
- Run `pyinstaller --onefile generateStudentRubrics.py`
- Grab the file from the `dist` folder
- Discard everything else it creates
