var socket = io.connect('http://localhost:8888');

socket.on('connect', function () {
    console.log('connected')
});

socket.on('message', function () {
    console.log(arguments)
});

socket.on('disconnect', function () {
    console.log('disconnceted')
});

socket.send('hi there');