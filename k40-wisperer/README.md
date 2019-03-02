# K40 Whisperer

A python based K40 laser software

## Roadmap 

 - Test and Setup    [development]
 - Extract API    
 - Add websocket  
 - create web-ui

## Build setup

Create a virtual environment using python 3.7 

    $ virtualenv -p /usr/bin/python3.7 venv

Activate the virtual environment

    $ ./venv/Scripts/activate

After running activate your shell should have a (venv) prefix

Now you can install the requirements

    $ pip install -r requirements


$ ./venv/Scripts/deactivate

## Test

Run `python -m unittest discover -s ./ -p 'test_*.py'` from the project directory.
