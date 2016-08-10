
function DrawSnakeBody(canvas, aray) {
    for (var i = 0; i < aray.length; i++) { 
         DrawSquare(canvas, aray[i], "rgb(50, 200, 50)");
    }
}

function DrawSquare(canvas, point, colour) {
    var context = canvas.getContext("2d");
    context.fillStyle = colour;
    context.fillRect(point.x * 50, point.y * 50, 50, 50);
}

function DrawApple(canvas, apple) {
    DrawSquare(canvas, apple, "rgb(50, 50, 200)")
}

function DrawGameOver(canvas) {
    var context = canvas.getContext("2d");
    context.clearRect(0, 0, canvas.width, canvas.height);
    context.font = "20px Arial";
    context.fillText("Game Over", canvas.width / 2, canvas.height / 2);
}

function RenderEverything(snake, apple, game_over) {
    var canvas = document.getElementById("snake_field");
    var ccontext = canvas.getContext("2d");
    ccontext.clearRect(0, 0, canvas.width, canvas.height);
    DrawSnakeBody(canvas, snake);
    DrawApple(canvas, apple);
    if (game_over) {
        DrawGameOver(canvas);
    }
}

function FieldUpdate(msg) {
    RenderEverything(msg.snake.bodey, msg.apple, msg.game_over);
}


namespace = '/test';
var socket = io.connect('http://' + document.domain + ':' + location.port + namespace);
        
document.addEventListener("keydown", (event) => {
    if (event.key === "ArrowRight") {
        socket.emit("turn right", {key: event.key});
    }
    if (event.key === "ArrowLeft") {
        socket.emit("turn left", {key: event.key});
    }
    if (event.key === "ArrowUp") {
        socket.emit("turn up", {key: event.key});
    }
    if (event.key === "ArrowDown") {
        socket.emit("turn down", {key: event.key});
    }
    if (event.key === " ") {
        socket.emit("toggle pause", {key:event.key});
    }
    if (event.key === "R") {
        socket.emit("restart_game", {key:event.key});
    }
}, false);

function Main() {
    socket.on("field_change", FieldUpdate);

    socket.on("connect", function() {
         socket.emit('my event', {data: 'I\'m connected!'});
    });

    // Interval function that tests message latency by sending a "ping"
    // message. The server then responds with a "pong" message and the
    // round trip time is measured.
    var ping_pong_times = [];
    var start_time;
    window.setInterval(function() {
        start_time = (new Date).getTime();
        socket.emit('my ping');
    }, 1000);

    // Handler for the "pong" message.
    function CalculatePingLatency() {
        var latency = (new Date).getTime() - start_time;
        ping_pong_times.push(latency);
        ping_pong_times = ping_pong_times.slice(-30); // keep last 30 samples
        var sum = 0;
        for (var i = 0; i < ping_pong_times.length; i++)
            sum += ping_pong_times[i];
        var ping_pong_div = document.getElementById("ping-pong");
        ping_pong_div.innerText = Math.round(10 * sum / ping_pong_times.length) / 10;
    }
    socket.on("my pong", CalculatePingLatency);
}

document.body.onload = Main;
