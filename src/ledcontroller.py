import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from rpi_ws281x import *
import argparse
import sys
import config as c
import random


sys.stdout.write('init strips... ')
parser = argparse.ArgumentParser()
parser.add_argument('-c', '--clear', action='store_true', help='clear the display on exit')
args = parser.parse_args()

strip1 = Adafruit_NeoPixel(c.LED_COUNT, c.LED_S1, c.LED_FREQ_HZ, c.LED_DMA1, c.LED_INVERT, c.LED_BRIGHTNESS, c.LED_CHANNEL1)
strip1.begin()
strip2 = Adafruit_NeoPixel(c.LED_COUNT, c.LED_S2, c.LED_FREQ_HZ, c.LED_DMA2, c.LED_INVERT, c.LED_BRIGHTNESS, c.LED_CHANNEL2)
strip2.begin()
sys.stdout.write('done. \n')


def form_color(status, brightness_override=-1):
    def form_value(loc):
        return int((brightness_override if brightness_override != -1 else int(status[4])) * int(status[loc]) / 255)
    return Color(form_value(1), form_value(2), form_value(3))


def check_status():
    with open("./file/status.txt", "r") as f:
        try:
            status = f.read().strip().split(',')
            return status
        except:
            return 'failed'


def color_wipe(strip, color, wait_ms=30):
    for i in range(strip.numPixels()):
        strip.setPixelColor(i, color)
        strip.show()
        time.sleep(wait_ms/1000.0)


def color_block(strip, color):
    for i in range(strip.numPixels()):
        strip.setPixelColor(i, color)
    strip.show()


def theater_chase(strip, color, wait_ms=50, iterations=1):
    for j in range(iterations):
        for q in range(3):
            for i in range(0, strip.numPixels(), 3):
                strip.setPixelColor(i+q, color)
            strip.show()
            time.sleep(wait_ms/1000.0)
            for i in range(0, strip.numPixels(), 3):
                strip.setPixelColor(i+q, 0)


def wheel(pos):
    if pos < 85:
        return Color(pos * 3, 255 - pos * 3, 0)
    elif pos < 170:
        pos -= 85
        return Color(255 - pos * 3, 0, pos * 3)
    else:
        pos -= 170
        return Color(0, pos * 3, 255 - pos * 3)


def rainbow(strip, wait_ms=20, iterations=1):
    for j in range(256 * iterations):
        for i in range(strip.numPixels()):
            strip.setPixelColor(i, wheel((i + j) & 255))
        strip.show()
        time.sleep(wait_ms / 1000.0)


def rainbow_cycle(strip, wait_ms=50, iterations=1):
    for j in range(256*iterations):
        for i in range(strip.numPixels()):
            strip.setPixelColor(i, wheel((int(i * 256 / strip.numPixels()) + j) & 255))
        strip.show()
        time.sleep(wait_ms/1000.0)


def theater_chase_rainbow(strip, wait_ms=50):
    for j in range(256):
        for q in range(3):
            for i in range(0, strip.numPixels(), 3):
                strip.setPixelColor(i+q, wheel((i+j) % 255))
            strip.show()
            time.sleep(wait_ms/1000.0)
            for i in range(0, strip.numPixels(), 3):
                strip.setPixelColor(i+q, 0)


def pixels_to_shine(strip, normal_weight=(90, 10), on_weight=(30, 70), on_max_length=12):
    retval = []
    choices = [0, 1]
    previous = 0
    on_count = 0
    for i in range(0, strip.numPixels()):
        if previous is 0 or on_count >= on_max_length:
            new = random.choices(choices, weights=normal_weight, k=1)
            on_count = 0
        else:
            new = random.choices(choices, weights=on_weight, k=1)
            on_count = on_count + 1
        retval.append(new[0])
        previous = new
    return retval


def rave_helper(strip):
    return pixels_to_shine(strip)


def starlight_helper(strip):
    choices_normal_weight = (95, 5)
    choices_on_weight = (60, 40)
    return pixels_to_shine(strip, normal_weight=choices_normal_weight, on_weight=choices_on_weight)


def run_rave_helper(strip, color, wait_sec=0.5):
    pixels_to_shine = rave_helper(strip)
    for i in range(0, strip.numPixels()):
        if pixels_to_shine[i] == 1:
            strip.setPixelColor(i, color)
        else:
            strip.setPixelColor(i, 0)
    strip.show()
    time.sleep(wait_sec)


def run_starlight_helper(strip, color, pixels_to_shine, wait_sec=0.2):
    for i in range(0, strip.numPixels()):
        if pixels_to_shine[i] == 1:
            strip.setPixelColor(i, color)
        else:
            strip.setPixelColor(i, 0)
    strip.show()
    time.sleep(wait_sec)
    first = pixels_to_shine.pop(0)
    pixels_to_shine.append(first)
    return pixels_to_shine


def run_rainbow_rave_helper(strip, wait_sec=0.5):
    pixels_to_shine = rave_helper(strip)
    for j in range(256):
        for i in range(strip.numPixels()):
            if pixels_to_shine[i] == 1:
                strip.setPixelColor(i, wheel((i + j) & 255))
            else:
                strip.setPixelColor(i, 0)
        strip.show()
        time.sleep(2.0/1000.0)
    # time.sleep(wait_sec)


def rave_a(strip, color):
    theater_chase(strip, color, iterations=10)
    run_rave_helper(strip, color)
    for i in range(0, 50):
        run_rave_helper(strip, color, wait_sec=0.06)
    run_rave_helper(strip, color)
    for i in range(0, 30):
        run_rave_helper(strip, color, wait_sec=0.07)


def rave_rainbow_a(strip):
    # theater_chase_rainbow(strip)
    run_rainbow_rave_helper(strip)
    # for i in range(0, 5):
    #     run_rainbow_rave_helper(strip, wait_sec=0.06)
    # run_rainbow_rave_helper(strip)
    # for i in range(0, 30):
    #     run_rainbow_rave_helper(strip, wait_sec=0.07)


# def starlight_a(strip, color):
#     pixels_to_shine = starlight_helper(strip)
#     for i in range(strip.numPixels()):
#         pixels_to_shine = run_starlight_helper(strip, color, pixels_to_shine)
#     # for i in range(0, 50):
#     #     run_starlight_helper(strip, color, wait_sec=0.7)


def dim_pixel_out_step(strip, pixel_to_dim, status, dim_level=100):
    dim_level = dim_level - 1
    bo = int(status[4]) * dim_level / 100
    strip.setPixelColor(pixel_to_dim, form_color(status, brightness_override=bo))
    strip.show()
    return dim_level


def dim_pixel_in_step(strip, pixel_to_dim, status, dim_level=0):
    dim_level = dim_level + 1
    bo = int(status[4]) * dim_level / 100
    strip.setPixelColor(pixel_to_dim, form_color(status, brightness_override=bo))
    strip.show()
    return dim_level


def dim_pixels_out(strip, pixels_to_dim_solo, status, dim_level=100):
    while dim_level > 0:
        dim_level = dim_level - 1
        bo = int(status[4]) * dim_level / 100
        for i in range(strip.numPixels()):
            if i in pixels_to_dim_solo:
                strip.setPixelColor(i, form_color(status, brightness_override=bo))
        strip.show()
        time.sleep(0.25)
    for i in range(strip.numPixels()):
        if i in pixels_to_dim_solo:
            strip.setPixelColor(i, Color(0, 0, 0))
            strip.show()


def dim_pixels_in(strip, pixels_to_dim_solo, status, dim_level=0):
    while dim_level < 100:
        dim_level = dim_level + 1
        bo = int(status[4]) * dim_level / 100
        for i in range(strip.numPixels()):
            if i in pixels_to_dim_solo:
                strip.setPixelColor(i, form_color(status, brightness_override=bo))
        strip.show()
        time.sleep(0.25)
    for i in range(strip.numPixels()):
        if i in pixels_to_dim_solo:
            strip.setPixelColor(i, form_color(status))
            strip.show()


def starlight_a(strip, status):
    for i in range(strip.numPixels()):
        strip.setPixelColor(i, Color(0, 0, 0))
    strip.show()
    pixels_to_dim = pixels_to_shine(strip, normal_weight=(98, 2), on_weight=(85, 15), on_max_length=2)
    pixels_to_dim_solo = [i for i in range(strip.numPixels()) if pixels_to_dim[i] == 1]
    pixels_to_dim_info = {i: {'wait_time': random.randint(1, 50), 'dim_level': 0} for i in pixels_to_dim_solo}
    while True:
        count = 0
        for i in pixels_to_dim_info:
            if pixels_to_dim_info[i]['wait_time'] > 0:
                pixels_to_dim_info[i]['wait_time'] = pixels_to_dim_info[i]['wait_time'] - 1
                count = count + 1
            elif pixels_to_dim_info[i]['dim_level'] < 100:
                pixels_to_dim_info[i]['dim_level'] = dim_pixel_in_step(strip, int(i), status,
                                                                       dim_level=pixels_to_dim_info[i]['dim_level'])
                count = count + 1
        time.sleep(0.1)
        if count == 0:
            break
    for i in range(strip.numPixels()):
        if i in pixels_to_dim_solo:
            strip.setPixelColor(i, form_color(status))
            strip.show()
    # dim_pixels_in(strip, pixels_to_dim_solo, status)
    for i in pixels_to_dim_info:
        pixels_to_dim_info[i]['wait_time'] = random.randint(1, 50)
    while True:
        count = 0
        for i in pixels_to_dim_info:
            if pixels_to_dim_info[i]['wait_time'] > 0:
                pixels_to_dim_info[i]['wait_time'] = pixels_to_dim_info[i]['wait_time'] - 1
                count = count + 1
            elif pixels_to_dim_info[i]['dim_level'] > 0:
                pixels_to_dim_info[i]['dim_level'] = dim_pixel_out_step(strip, int(i), status,
                                                                       dim_level=pixels_to_dim_info[i]['dim_level'])
                count = count + 1
        time.sleep(0.1)
        if count == 0:
            break
    for i in range(strip.numPixels()):
        if i in pixels_to_dim_solo:
            strip.setPixelColor(i, Color(0, 0, 0))
            strip.show()
    # dim_pixels_out(strip, pixels_to_dim_solo, status)


def starlight_b(strip, status):
    '''
    light up whole strip, randomly twinkle individual leds, in pairs from 1 to 3
    turn off for random time between .1 and 1 seconds
    dim in and out
    
    :param strip: 
    :param color: 
    :return: 
    '''
    for i in range(strip.numPixels()):
        strip.setPixelColor(i, form_color(status))
    strip.show()
    pixels_to_dim = pixels_to_shine(strip, normal_weight=(97, 3), on_weight=(70, 30), on_max_length=2)
    pixels_to_dim_solo = [i for i in range(strip.numPixels()) if pixels_to_dim[i] == 1]
    dim_pixels_out(strip, pixels_to_dim_solo, status)
    time.sleep(5)
    dim_pixels_in(strip, pixels_to_dim_solo, status)


def starlight_rainbow_helper(strip):
    count = 0
    while count < 20:
        pixels_to_shine = rave_helper(strip)
        for i in range(strip.numPixels()):
            for j in range(256):
                if pixels_to_shine[i] == 1:
                    strip.setPixelColor(i, wheel((i + j) & 255))
                else:
                    strip.setPixelColor(i, 0)
        strip.show()
        time.sleep(1.0 / 1000.0)
        count = count + 1


def starlight_rainbow(strip):
    starlight_rainbow_helper(strip)


def main_check():
    with open("./file/status.txt", "r") as f:
        try:
            status = f.read().strip().split(',')
            if int(status[5]) == 0:
                strip1.setBrightness(0)
                strip1.show()
            else:
                if status[0].lower() == 'wipe':
                    strip1.setBrightness(255)
                    color_wipe(strip1, form_color(status))
                elif status[0].lower() == 'block':
                    strip1.setBrightness(255)
                    color_block(strip1, form_color(status))
                elif status[0].lower() == 'chase':
                    strip1.setBrightness(255)
                    while check_status() == status:
                        theater_chase(strip1, form_color(status))
                elif status[0].lower() == 'rainbow':
                    strip1.setBrightness(int(status[4]))
                    while check_status() == status:
                        rainbow(strip1)
                elif status[0].lower() == 'rainbow_cycle':
                    strip1.setBrightness(int(status[4]))
                    while check_status() == status:
                        rainbow_cycle(strip1)
                elif status[0].lower() == 'rainbow_chase':
                    strip1.setBrightness(int(status[4]))
                    while check_status() == status:
                        theater_chase_rainbow(strip1)
                elif status[0].lower() == 'rave_a':
                    strip1.setBrightness(255)
                    while check_status() == status:
                        rave_a(strip1, form_color(status))
                elif status[0].lower() == 'rave_b':
                    strip1.setBrightness(255)
                    while check_status() == status:
                        rave_a(strip1, form_color(status))
                elif status[0].lower() == 'rave_rainbow_a':
                    strip1.setBrightness(255)
                    while check_status() == status:
                        rave_rainbow_a(strip1)
                elif status[0].lower() == 'starlight_a':
                    strip1.setBrightness(255)
                    while check_status() == status:
                        starlight_a(strip1, status)
                elif status[0].lower() == 'starlight_b':
                    strip1.setBrightness(255)
                    while check_status() == status:
                        starlight_b(strip1, status)
                elif status[0].lower() == 'starlight_rainbow':
                    strip1.setBrightness(255)
                    while check_status() == status:
                        starlight_rainbow(strip1)
        except Exception as e:
            print(e)
            print("could not read file, trying again")
            MyHandler()


class MyHandler(FileSystemEventHandler):
    def on_modified(self, event):
        if event.src_path == "./file/status.txt":
            print('modification detected')
            main_check()


if __name__ == '__main__':
    sys.stdout.write('init observer... ')
    event_handler = MyHandler()
    observer = Observer()
    observer.schedule(event_handler, path='./file', recursive=False)
    observer.start()
    sys.stdout.write('done. \n')

    observer.join()

    main_check()
