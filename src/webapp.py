from flask import Flask, request, render_template, redirect
import sys
from forms import HomeForm


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
            status = f.read().strip().split(',')
            return status
        except:
            return 'failed'


def update_status(mode, r, g, b, brightness, power):
    try:
        with open("./file/status.txt", "w") as f:
            new_status = f'{mode},{r},{g},{b},{brightness},{power}'
            f.write(new_status)
        return "success"
    except Exception as e:
        return "failed"


@app.route('/', methods=('GET', 'POST'))
def submit():

    if request.method == 'POST':

        new_effect = request.form['effect']
        new_color_hex = request.form['hexcolor'][1:]
        new_color = hex_to_rgb(new_color_hex)
        new_brightness = request.form['brightness']
        power = 1

        sys.stdout.write('updating status... ')
        x = update_status(new_effect, new_color[0], new_color[1], new_color[2], new_brightness, power)
        sys.stdout.write(f'{x}. \n')

        print(request.form['effect'])
        print(request.form['hexcolor'])

        return redirect('/')

    status = check_status()
    current_color_hex = rgb_to_hex(status[1], status[2], status[3])
    print(current_color_hex)
    current_brightness = int(status[4])

    print(status[0])

    return render_template('home.html', status=status, current_color_hex=current_color_hex)


@app.route('/power', methods=['POST'])
def power():
    state = request.form['state']
    status = check_status()
    if state == 'on':
        sys.stdout.write('updating status... ')
        x = update_status(status[0], status[1], status[2], status[3], status[4], 1)
        sys.stdout.write(f'{x}. \n')
    elif state == 'off':
        sys.stdout.write('updating status... ')
        x = update_status(status[0], status[1], status[2], status[3], status[4], 0)
        sys.stdout.write(f'{x}. \n')
    return redirect('/')


sys.stdout.write('starting flask app. \n')
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=False)
