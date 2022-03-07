from tkinter.filedialog import askopenfile, askdirectory
from pathlib import Path
from tkinter import Tk
import platform
import os

def is_windows():
    return platform.system() == "Windows"

def create_dir(file_path):
    if is_windows():
        Path(file_path).mkdir(parents=True, exist_ok=True)
    else:
        os.system(f"sudo mkdir -p -m 700 '{file_path}'")
        os.system(f"sudo chown -R $USER '{file_path}'")

def ask_file_location():
    Tk().withdraw()
    return askopenfile(title="Import CSV").name

def ask_directory_location():
    Tk().withdraw()
    return askdirectory(title="Export CSV")