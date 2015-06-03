// Handler that every 500ms calls updateServer()
function update() {
    setInterval(function () {
        updateServer();
    }, 500);
}

var ask = new XMLHttpRequest();

function updateServer() {
    ask.open("GET", "/ServerData", false);
    ask.send();

    var answer = JSON.parse(ask.responseText);
    var clients_number = answer['clients_number'];
    var percentage = answer['percentage'];
    var time_taken = answer['time_taken'];
    var result = answer['result'];

    $('#percentage-number').html(percentage);
    $('#time-taken').html(time_taken);
    $('#clients-number').html(clients_number);
    $('#closest-dot').html(result);
}

function pause() {
    var request = new XMLHttpRequest();
    request.open("POST", "/ServerData", true);
    request.send("data=pause");
}

function resume() {
    var request = new XMLHttpRequest();
    request.open("POST", "/ServerData", true);
    request.send("data=resume");
}

function restart() {
    var request = new XMLHttpRequest();
    request.open("POST", "/ServerData", true);
    request.send("data=restart");

    $('#clients-number').html("");
    $('#time-taken').html("");
    $('#percentage-number').html("");
    $('#closest-dot').html("");
}