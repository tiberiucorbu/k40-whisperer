app = socketio.WSGIApp(sio, static_files={

})

if __name__ == '__main__':
    eventlet.wsgi.server(eventlet.listen(('', 5000)), app)