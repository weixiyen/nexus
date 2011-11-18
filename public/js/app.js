var socket = io.connect('http://localhost:8888', {
    resource: 'socket'
});

socket.on('connect', function () {
    console.log('connected')
});

socket.on('message', function (message) {
    console.log(message)
});

socket.on('disconnect', function () {
    console.log('disconnceted')
});

socket.send('Hello from ' + navigator.userAgent);