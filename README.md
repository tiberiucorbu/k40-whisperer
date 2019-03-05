# K40 Socket Bridge

A fork of https://github.com/scorchworks/K40-Whisperer that aims to improve the codebase and its re-usability and adds a network, web interface and 
multi-user features

----- 

This is a monorepo that contains the following packages:

   - k40-whisperer - the original application
   - k40-usb-bridge - a library that exposes the M2nano commands via USB
   - k40-socket-server - a https/wss server that exposes k40-usb-bridge over the network
   - k40-web-interface - a single page application that controls the k40-socket-server

