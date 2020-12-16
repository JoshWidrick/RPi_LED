from flask import Flask, request, render_template, redirect
import sys

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secr3t'


sys.stdout.write('starting flask app. \n')
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=False)
