import sys

from cx_Freeze import setup, Executable

build_exe_options = {
    "include_files": [
        "assets/"
        ],
    "packages": ["PIL", "codecs"],
    }

base = None
if sys.platform == "win32":
    base = "Win32GUI"

setup(name="K40-Whisperer",
      version="0.21-beta",
      description="Chinese K40 Laser control software",
      executables=[Executable("k40_whisperer.py", base=base)],
      options={"build_exe": build_exe_options})
