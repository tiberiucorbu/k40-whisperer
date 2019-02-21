# K40 Whisperer

A python based K40 laser software

## Roadmap 

 - Test             [development]
 - Extract api    
 - Add websocket  
 - create web-ui

## Build

The project was initialy build using shell scripts, there is no a Dockerfile that is supposed to build test and release the project.

You need docker for that. from the command line run:

    docker build -t k40-wishperer .


## Test

Run `python test.py` from the project directory.
