function R(dot1, dot2)
{
    return Math.sqrt( (dot1[0] - dot2[0])*(dot1[0] - dot2[0]) +
                      (dot1[1] - dot2[1])*(dot1[1] - dot2[1]) +
                      (dot1[2] - dot2[2])*(dot1[2] - dot2[2]));
}

function getMinWay(dots, dot)
{
    var min = R(dots[0], dot);
    var closest_dot = dots[0];

    for(var i = 1; i < dots.length; i++)
    {
        var tmp = R(dots[i], dot);
        if(tmp < min)
        {
            min = tmp;
            closest_dot = dots[i];
        }
    }
    return closest_dot;
}

postMessage(["Data awaiting", "Data awaiting"]);

var state = "WORK", task, best_dot, main_dot;

while(state != 'STOP') {
    var requestGET = new XMLHttpRequest();
    requestGET.open("GET", "/WorkerData", false);
    requestGET.send();

    var answer = JSON.parse(requestGET.responseText);
    task = answer['task'];
    main_dot = answer['main_dot']
    state = answer['state'];
    worker_number = answer['worker_number']

    if(state == 'WORK'){
        best_dot = getMinWay(task, main_dot);

        var requestPOST = new XMLHttpRequest();
        requestPOST.open("POST", "/WorkerData", true);
        requestPOST.send("worker_number=" + worker_number + "&best_dot=" + best_dot);

        postMessage([task.length, best_dot])
    }
    else if (state == 'PAUSE')
        postMessage(["PAUSED", "PAUSED"]);
    else if (state == 'STOP')
        postMessage(["STOPPED", "STOPPED"]);
    else
        postMessage(["WAITING FOR TASK", "WAITING FOR TASK"])
}