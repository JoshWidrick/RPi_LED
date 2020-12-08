from flask import Flask, request, jsonify, current_app
import led_service as ls


app = Flask(__name__)


# {{url}}/led?red=255&green=255&blue=255&position=1
@app.route('/led', methods=['GET'])
def led():
    try:
        red = request.args.get('red')
        green = request.args.get('green')
        blue = request.args.get('blue')
        mode = request.args.get('mode')
        resp = ls.update_led(mode, red, green, blue)
    except:
        resp = "missing required param (red, green, blue, mode)"
    return jsonify({"message": resp})


@app.route('/check_vis_status', methods=['GET'])
def check_vis_status():
    return jsonify({"message": ls.check_visualization_status()})
