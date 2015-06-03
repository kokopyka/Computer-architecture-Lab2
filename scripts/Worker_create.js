function createWorker() {
    var worker = new Worker("scripts/Worker.js");
    worker.onmessage = function(event) {
        $('#dots-to-calculate').html(event.data[0]);
        $('#last-min-way').html(event.data[1]);
    };
}