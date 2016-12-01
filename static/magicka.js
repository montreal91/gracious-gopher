const FIELD_COLOUR = "rgb(220, 230, 220)";
const SNAKE_COLOUR = "rgb(50, 200, 50)";
const APPLE_COLOUR = "rgb(50, 50, 200)";



function DrawSnakeBody(canvas, aray) {
    for (var i = 0; i < aray.length; i++) { 
         DrawSquare(canvas, aray[i], SNAKE_COLOUR);
    }
}

function DrawSquare(canvas, point, colour) {
    var context = canvas.getContext("2d");
    context.fillStyle = colour;
    context.fillRect(point.x * 50-1, point.y * 50-1, 49, 49);
}

function DrawEmptyField(canvas, params) {
    var context = canvas.getContext("2d");
    // console.log(colour);
    // context.fillStyle = colour;
    for (var i = 0; i < params.width; i++) {
        for (var j = 0; j < params.height; j++) {
            DrawSquare(canvas, {x:i, y:j}, FIELD_COLOUR);
        }
    }
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

function RenderEverything(everything) {
    var canvas = document.getElementById("snake_field");
    var ccontext = canvas.getContext("2d");
    ccontext.clearRect(0, 0, canvas.width, canvas.height);
    DrawEmptyField(canvas, everything.field);
    DrawSnakeBody(canvas, everything.snake.bodey);
    // console.log(everything.apple);
    DrawApple(canvas, everything.apple);
    if (everything.game_over) {
        DrawGameOver(canvas);
    }
}

function FieldUpdate(msg) {
    RenderEverything(msg);
}


namespace = '/test';
var socket = io.connect('http://' + document.domain + ':' + location.port + namespace);
console.log(document.domain);

function giOpenTab(event, tab_name) {
    // console.log(event);
    var i, tab_content, tab_links;

    tab_content = document.getElementsByClassName("tabcontent");
    for (i = 0; i < tab_content.length; i++) {
        tab_content[i].style.display = "none";
    }

    tab_links = document.getElementsByClassName("tablinks");
    for (i = 0; i < tab_links.length; i++) {
        tab_links[i].className = tab_links[i].className.replace(" active", "");
    }

    document.getElementById(tab_name).style.display = "block";
    event.currentTarget.className += " active";

    socket.emit("init_game", {});
}
        
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
    // console.log("Main");
    socket.on("field_change", FieldUpdate);

    // socket.on("connect", function(msg) {
    //     console.log(msg);
    //     // var div = document.getElementById("some_id");
    //     // div.innerText = msg.message;
    //      socket.emit('my event', {data: 'I\'m connected!'});
    // });

    socket.on("my response", function(msg) {
        console.log(msg);
    });

    socket.on("init_response", function(msg){
        console.log(msg);
        var canvas = document.getElementById("snake_field");
        DrawEmptyField(canvas, msg.field);
    });

    socket.on("poop", function(msg) {
        console.log(msg);
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
        // var ping_pong_div = document.getElementById("ping-pong");
        // ping_pong_div.innerText = Math.round(10 * sum / ping_pong_times.length) / 10;
    }
    socket.on("my pong", CalculatePingLatency);
}

document.body.onload = Main;
