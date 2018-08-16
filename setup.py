# run this from the command line: python setup.py py2exe

from distutils.core import setup

try:
    import py2exe
except ImportError:
    pass

setup(
    options={
        "py2exe": {
            "compressed": 1, "optimize": 0,
            "includes": ["lxml.etree", "lxml._elementpath", "gzip"],
            }
        },
    zipfile=None,
    windows=[{
        "script":"k40_whisperer.py",
        "icon_resources":[(0,"assets/scorchworks.ico"),(1,"assets/scorchworks.ico")]
        }],
    )

