var socket = require('socket.io');

const leftRight = () => Math.random() < 0.5 ? 'left' : 'right'; 

// setInterval(function () {console.log(leftRight())}, 250) ; 

setInterval(function () {
    socket.emit('game command', leftRight());
    console.log(leftRight()); 
} , 250) ;
