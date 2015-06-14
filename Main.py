__author__ = 'Oleh'

import time
from functions import generate_array
from bottle import run, debug, template, static_file, post, get, request


all_dots_number = 30000000    # Dots number to calculate
server_state = 2            # 0 - Stop, 1 - pause, 2 - open
clients_number = 0          # Global variable. Holds number of clients

main_dot = [10, 10, 10]     # Dot from which the closest distance is being calculated
parts_number = 100         # Defines how big data task will be divided
parts_sent = []             # Variable that holds numbers of sent task parts
parts_received = []         # Variable that holds numbers of received task parts
minimal_ways_from_nodes = []  # Holds calculated closest dots from each cluster node

time_taken = 0
start_time = 0
percentage = 0
result = -1                 # Closest dot position


# Displays server data html page for request localhost:8080/server
@get('/server')
def server():
    return template('Server.html')


# Displays worker data html page for request localhost:8080/worker
@get('/worker')
def worker():
    return template('Worker.html')


# Returns static file. Used for getting JavaScript files from /static folder
@get('/static/:filename#.*#')
def send_static(filename):
    return static_file(filename, root='./static/')

# Returns static file. Used for getting JavaScript files from /static folder
@get('/scripts/:filename#.*#')
def send_scripts(filename):
    return static_file(filename, root='./scripts/')

# Returns global server variables when /ServerData is requested
@get('/ServerData')
def server_get():
    return {'clients_number': clients_number, 'percentage': percentage,
            'time_taken': time_taken, 'result': result}


# Receives data from Server.js through request key
@post('/ServerData')
def server_post():
    global parts_sent, parts_received, start_time, percentage, minimal_ways_from_nodes, server_state, time_taken, result

    data = request.forms.get('data')

    if data == 'pause':
        server_state = 1
    elif data == 'resume':
        server_state = 2
    elif data == 'restart':
        parts_sent = []
        parts_received = []
        minimal_ways_from_nodes = []
        start_time = percentage = time_taken = 0
        result = -1
        server_state = 2


# Returns global web worker variables when /WorkerData is requested
@get('/WorkerData')
def worker_get():
    if server_state == 1:
        return {'state': 'PAUSE', 'task': [], 'main_dot': main_dot, 'worker_number': -1}
    elif server_state == 0:
        return {'state': 'STOP', 'task': [], 'main_dot': [], 'worker_number': -1}

    global start_time, clients_number

    if start_time == 0:
        start_time = time.time()

    # Firstly send dots with no % from division
    for i in range(1, parts_number + 1):
        if i not in parts_sent and i not in parts_received:
            parts_sent.append(i)
            clients_number = len(parts_sent) - len(parts_received)
            task = generate_array(all_dots_number / parts_number)
            return {'state': 'WORK', 'task': task, 'main_dot': main_dot, 'worker_number': i}

    # If there's a % from division
    rest = all_dots_number % parts_number
    if len(parts_received) == parts_number and rest:
        parts_sent.append(parts_number + 1)
        clients_number = len(parts_sent) - len(parts_received)
        task = generate_array(rest)  # random.sample(range(rest), rest)
        return {'state': 'WORK', 'task': task, 'main_dot': main_dot, 'worker_number': parts_number + 1}

    if len(minimal_ways_from_nodes) >= parts_number:
        return {'state': 'WORK', 'task': minimal_ways_from_nodes, 'main_dot': main_dot,
                'worker_number': parts_number + 1}

    return {'state': 'STOP', 'task': [], 'main_dot': [], 'worker_number': -1}


# Receives data from Worker.js through request keys
@post('/WorkerData')
def worker_post():
    global result, percentage, time_taken, server_state

    if server_state == 0:
        return

    worker_number = request.forms.get('worker_number')
    best_dot = request.forms.get('best_dot')

    rest = all_dots_number % parts_number

    if rest and len(minimal_ways_from_nodes) == parts_number + 1 \
            or not rest and len(minimal_ways_from_nodes) == parts_number:
        time_taken = time.time() - start_time
        result = best_dot
        server_state = 0
        return

    minimal_ways_from_nodes.append(best_dot)
    parts_received.append(worker_number)
    percentage = int(100 * len(parts_received) / parts_number)

if __name__ == '__main__':
    # debug(True)   # To see detailed errors description
    run()           # Run the server"""
