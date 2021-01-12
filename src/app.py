from flask import Flask, request, render_template, redirect, jsonify
import sys

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secr3t'

STATUS_KEY = ['mode', 'r', 'g', 'b', 'sr', 'sg', 'sb', 'brightness', 'power', 'speed', 'wait_time', 'percentage', 'spercentage']


def get_status():
    with open("./file/status.txt", "r") as f:
        try:
            return f.read().strip()
        except:
            return 'failed'


@app.route('/led')
def led():
    return 'x'


@app.route('/status')
def status():
    return jsonify({'status': str(get_status())})


@app.route('/ping')
def ping():
    return 'success'


sys.stdout.write('starting flask app. \n')
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=6969, debug=False)
