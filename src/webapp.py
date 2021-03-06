from flask import Flask, request, render_template, redirect
import sys


# TODO renamae and make to deamon, add all controll functionality to web, and have a system to save deamon info and send cmds to it


sys.stdout.write('*===* STARTING APPLICATION *===* \n')

app = Flask(__name__)
app.config['SECRET_KEY'] = 'JgMWQ3X2c286Zv2gVqmC6PbPbWAcqZKg'


def hex_to_rgb(h):
    return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))


def rgb_to_hex(r, g, b):
    return '{:02x}{:02x}{:02x}'.format(int(r), int(g), int(b))


def check_status():
    with open("./file/status.txt", "r") as f:
        try:
            return f.read().strip().split(',')
        except:
            return 'failed'


def update_status(mode, r, g, b, brightness, power, sr, sg, sb):
    sys.stdout.write('updating status... ')
    with open("./file/status.txt", "w") as f:
        try:
            new_status = f'{mode},{r},{g},{b},{brightness},{power},{sr},{sg},{sb}'
            f.write(new_status)
            sys.stdout.write('success. \n')
        except Exception as e:
            sys.stdout.write('failed. \n')


@app.route('/', methods=('GET', 'POST'))
def submit():
    if request.method == 'POST':
        new_effect = request.form['effect']
        new_color_hex = request.form['hexcolor'][1:]
        new_color = hex_to_rgb(new_color_hex)
        new_secondary_color_hex = request.form['shexcolor'][1:]
        new_secondary_color = hex_to_rgb(new_secondary_color_hex)
        new_brightness = request.form['brightness']
        default_power = 1
        update_status(new_effect, new_color[0], new_color[1], new_color[2],
                      new_brightness, default_power, new_secondary_color[0],
                      new_secondary_color[1], new_secondary_color[2])
        return redirect('/')
    status = check_status()
    current_color_hex = rgb_to_hex(status[1], status[2], status[3])
    current_secondary_color_hex = rgb_to_hex(status[6], status[7], status[8])
    return render_template('home.html', status=status, current_color_hex=current_color_hex, current_secondary_color_hex=current_secondary_color_hex)


@app.route('/power', methods=['POST'])
def power():
    state = request.form['state']
    status = check_status()
    if state == 'on':
        update_status(status[0], status[1], status[2], status[3], status[4], 1, status[6], status[7], status[8])
    elif state == 'off':
        update_status(status[0], status[1], status[2], status[3], status[4], 0, status[6], status[7], status[8])
    return redirect('/')


@app.route('/panel', methods=['GET', 'POST'])
def panel():
    return render_template('panel.html')


@app.route('/status')
def status():
    return ','.join(i for i in check_status())


sys.stdout.write('starting flask app. \n')
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=False)
