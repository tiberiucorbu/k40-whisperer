#!/usr/bin/python
"""
    Setup k40 usb package

    Copyright (C) <2019>  <@tiberiucorbu>

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""
from setuptools import setup, find_packages

with open('README.md', 'r') as f:
    long_description = f.read()
with open('requirements.txt', 'r') as f:
    requirements = f.read().splitlines()

setup(
    name="k40usb",
    version="0.0.1",
    packages=find_packages(),
    # scripts=['main/main.py'],

    # installed or upgraded on the target machine
    install_requires=requirements,

    package_data={
        # If any package contains *.txt or *.rst files, include them:
        # '': ['*.txt', '*.rst'],
        # And include any *.msg files found in the 'hello' package, too:
        # 'hello': ['*.msg'],
    },

    # metadata to display on PyPI
    author="Tiberiu CORBU",
    author_email="hello@tiberiucorbu.ro",
    description="K40 Usb Python facade",
    license="GPL-3.0",
    keywords="k40 laser cutter usb facade",
    url="https://github.com/tiberiucorbu/k40-socket-bridge",  # project home page, if any
    project_urls={
        "Bug Tracker": "https://github.com/tiberiucorbu/k40-socket-bridge/issues",
        "Documentation": "https://github.com/tiberiucorbu/k40-socket-bridge",
        "Source Code": "https://github.com/tiberiucorbu/k40-socket-bridge",
    },
    long_description=long_description,
    long_description_content_type="text/markdown",
    include_package_data=True,
    zip_safe=False,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GPL-3.0 License",
        "Operating System :: OS Independent",
    ],

    # could also include long_description, download_url, classifiers, etc.
)
