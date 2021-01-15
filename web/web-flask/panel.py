from flask import Flask, request, render_template, redirect, flash
import requests, json
import sys

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secr3t'

STATUS_KEY = ['mode', 'r', 'g', 'b', 'sr', 'sg', 'sb', 'brightness', 'power', 'speed', 'wait_time', 'percentage', 'spercentage']
CONTROLLER_KEY = ['name', 'ip', 'port']


def import_controllers():
    retval = {}
    for i in get_controllers():
        retval[i[0]] = [i[1], i[2]]
    return retval


def get_controllers():
    with open("file/controllers.txt", "r") as f:
        try:
            if f is None:
                return []
            return [l.strip().split(',') for l in f.readlines()]
        except:
            return 'failed'


def add_controller(name, ip, port):
    with open("file/controllers.txt", "a") as f:
        try:
            f.write(f'{name},{ip},{port}\n')
            print(f'{name},{ip},{port}')
            return 'Success'
        except Exception as e:
            return 'Failed' + str(e)


def import_status(resp_status):
    listx = resp_status.split(',')
    retval = {'list': listx}
    count = 0
    for item in listx:
        retval[STATUS_KEY[count]] = item
        count = count + 1
    return retval


def get_controller_status(ip, port):
    resp = requests.get(f'http://{ip}:{port}/status')
    resp = resp.json()
    return import_status(resp['status'])


def get_all_controller_status(controllers):
    retval = {}
    for i in controllers:
        ip = i[1]
        port = i[2]
        retval[i[0]] = get_controller_status(ip, port)
    return retval


@app.route('/panel', methods=['GET', 'POST'])
def panel():
    # controllers = get_controllers()
    controllers = import_controllers()
    return redirect(f'/panel/{list(controllers.keys())[0]}')
    # cstatuses = get_all_controller_status(controllers)
    # return render_template('panel.html', controller=controllers[list(controllers.keys())[0]], controllers=list(controllers.keys()))


@app.route('/panel/<controller>', methods=['GET', 'POST'])
def panel_c(controller):
    controllers = import_controllers()
    print(controllers)
    x = controllers[controller]
    print(x)
    status = get_controller_status(x[0], x[1])
    # controllers = get_controllers()

    return render_template('panel.html', controller=controller, controllers=list(controllers.keys()), status=status)


@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        retval = add_controller(request.form['name'], request.form['ip_address'], request.form['port'])
        flash(retval)
        return redirect('/panel')
    return render_template('add.html')


@app.route('/power/<toggle>/<controller>')
def power(toggle, controller):
    print(toggle)
    return redirect(f'/panel/{controller}')


sys.stdout.write('starting flask app. \n')
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=420, debug=False)
