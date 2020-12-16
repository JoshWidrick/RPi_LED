from flask import Flask, request, render_template, redirect, flash

import sys

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secr3t'


def get_controllers():
    with open("./file/controllers.txt", "r") as f:
        try:
            if f is None:
                return []
            return [l.strip().split(',') for l in f.readlines()]
        except:
            return 'failed'


def add_controller(name, ip, port):
    with open("./file/controllers.txt", "w") as f:
        try:
            lines = get_controllers()
            lines.append([name, ip, port])
            f.writelines([','.join(x) for x in lines])
            return 'Success'
        except Exception as e:
            return 'Failed'


@app.route('/panel', methods=['GET', 'POST'])
def panel():

    return render_template('panel.html', controllers=get_controllers())


@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':

        flash(add_controller(request.form['name'], request.form['ip_address'], request.form['port']))

        return redirect('/panel')

    return render_template('add.html')


sys.stdout.write('starting flask app. \n')
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=6969, debug=False)
