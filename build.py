# region Main
from os import name, chmod, remove, rmdir, system, walk
from pathlib import Path
from stat import S_IWUSR
from os.path import join, exists, isfile, isdir
import platform
from subprocess import run
from time import sleep
from math import floor
import shutil

python_path = shutil.which("python")
print(f"Python found at: {python_path}")


# def cls():
#     system("cls" if name == "nt" else "clear")


# def get_chars(num: int, c: str) -> str:
#     spaces = ""
#     for _ in range(num):
#         spaces += c
#     return spaces


# def get_spaces(num: int) -> str:
#     return get_chars(num, " ")


# def get_bar(percent: float, start_spaces=1, bars: int = 40) -> str:
#     result = f"{get_spaces(start_spaces)}["
#     real_bars = floor(bars * (percent / 100))
#     for i in range(bars):
#         if i < real_bars:
#             result += "❚"
#         else:
#             result += " "
#     result += "]"
#     return result


# cls()
# percent = 0
# print(f"{get_bar(percent)} {percent}% Removing previous build", end="\r")


# def rmtree(top):
#     for root, dirs, files in walk(top, topdown=False):
#         for name in files:
#             filename = join(root, name)
#             chmod(filename, S_IWUSR)
#             remove(filename)
#         for name in dirs:
#             rmdir(join(root, name))
#     rmdir(top)


# def remove_files_and_directories(*paths: str):
#     for path in paths:
#         if exists(path):
#             if isdir(path):
#                 rmtree(path)
#             elif isfile(path):
#                 remove(path)


# def fetch_parent_folder(name: str, path: str) -> str:
#     parts = list(Path(path).parts)
#     while len(parts) > 0:
#         part = parts[len(parts) - 1]
#         if name in part:
#             return "\\".join(parts)
#         parts.pop()
#     return ""


# main_folder = fetch_parent_folder("MAudioBugFix", __file__)

# venv_path = join(main_folder, "venv")
# remove_files_and_directories(
#     join(main_folder, "build", "maudio_bug_fix"),
#     join(main_folder, "dist", "maudio_bug_fix"),
#     venv_path,
# )


# requirements_path = join(main_folder, "requirements.txt")

# py_var = "python" if platform.system() == "Windows" else "python3"

# createvenv_path = join(venv_path, "createvenv.txt")

# cls()
# percent = 25
# print(
#     f"{get_bar(percent)} {percent}% Trying to create virtual environment",
#     end="\r",
# )

# if not exists(createvenv_path):
#     process = run(
#         [py_var, "-m", "venv", venv_path],
#         capture_output=True,
#     )
#     f = open(createvenv_path, "a")
#     f.write(
#         "Delete this file only if you want to recreate the venv! Do not include this file when you package/publish the extension."
#     )
#     f.close()

# py_var = join(venv_path, "Scripts/python.exe")

# if not exists(py_var):
#     py_var = join(venv_path, "bin/python")
#     if not exists(py_var):
#         raise Exception("venv doesn't seem to have a python path")

# cls()
# percent = 50
# print(
#     f"{get_bar(percent)} {percent}% Installing dependencies in requirements.txt",
#     end="\r",
# )

# process = run(
#     [py_var, "-m", "pip", "install", "-r", requirements_path],
#     capture_output=True,
# )

# py_installer = join(venv_path, "Scripts/pyinstaller.exe")
# if not exists(py_installer):
#     py_installer = join(venv_path, "bin/pyinstaller")
#     if not exists(py_installer):
#         raise Exception("venv doesn't seem to have a pyinstaller path")

# maudio_bug_fix_path = join(main_folder, "src/main.spec")

# if not exists(maudio_bug_fix_path):
#     maudio_bug_fix_path = join(main_folder, "src/main.pyw")
#     if not exists(maudio_bug_fix_path):
#         maudio_bug_fix_path = join(main_folder, "src/main.py")

# cls()
# percent = 75
# print(f"{get_bar(percent)} {percent}% Building executable", end="\r")
# process = run(
#     [
#         py_installer,
#         "--onefile",
#         "--distpath",
#         "./build/dist",
#         "--workpath",
#         "./build/build",
#         maudio_bug_fix_path,
#         "-y",
#     ],
#     capture_output=True,
# )

# cls()
# percent = 100
# print(f"{get_bar(percent)} {percent}% Built executable", end="\r")
# sleep(0.5)
# cls()
# endregion
