import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from rpi_ws281x import *
import argparse
import sys
import config as c


sys.stdout.write('init strips... ')
parser = argparse.ArgumentParser()
parser.add_argument('-c', '--clear', action='store_true', help='clear the display on exit')
args = parser.parse_args()

strip1 = Adafruit_NeoPixel(c.LED_COUNT, c.LED_S1, c.LED_FREQ_HZ, c.LED_DMA1, c.LED_INVERT, c.LED_BRIGHTNESS, c.LED_CHANNEL1)
strip1.begin()
strip2 = Adafruit_NeoPixel(c.LED_COUNT, c.LED_S2, c.LED_FREQ_HZ, c.LED_DMA2, c.LED_INVERT, c.LED_BRIGHTNESS, c.LED_CHANNEL2)
strip2.begin()
sys.stdout.write('done. \n')


def form_color(status):
    def form_value(loc):
        return int(int(status[4]) * int(status[loc]) / 255)
    return Color(form_value(1), form_value(2), form_value(3))


def check_status():
    with open("./file/status.txt", "r") as f:
        try:
            status = f.read().strip().split(',')
            return status
        except:
            return 'failed'


def color_wipe(strip, color, wait_ms=30):
    """Wipe color across display a pixel at a time."""
    for i in range(strip.numPixels()):
        strip.setPixelColor(i, color)
        strip.show()
        time.sleep(wait_ms/1000.0)


def color_block(strip, color):
    for i in range(strip.numPixels()):
        strip.setPixelColor(i, color)
    strip.show()


def theater_chase(strip, color, wait_ms=50, iterations=1):
    """Movie theater light style chaser animation."""
    for j in range(iterations):
        for q in range(3):
            for i in range(0, strip.numPixels(), 3):
                strip.setPixelColor(i+q, color)
            strip.show()
            time.sleep(wait_ms/1000.0)
            for i in range(0, strip.numPixels(), 3):
                strip.setPixelColor(i+q, 0)


def wheel(pos):
    """Generate rainbow colors across 0-255 positions."""
    if pos < 85:
        return Color(pos * 3, 255 - pos * 3, 0)
    elif pos < 170:
        pos -= 85
        return Color(255 - pos * 3, 0, pos * 3)
    else:
        pos -= 170
        return Color(0, pos * 3, 255 - pos * 3)


def rainbow(strip, wait_ms=20, iterations=1):
    """Draw rainbow that fades across all pixels at once."""
    for j in range(256 * iterations):
        for i in range(strip.numPixels()):
            strip.setPixelColor(i, wheel((i + j) & 255))
        strip.show()
        time.sleep(wait_ms / 1000.0)


def rainbow_cycle(strip, wait_ms=50, iterations=1):
    """Draw rainbow that uniformly distributes itself across all pixels."""
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


def rave(strip):
    pass


def main_check():
    with open("./file/status.txt", "r") as f:
        try:
            colors = f.read().strip().split(',')
            if int(colors[5]) == 0:
                strip1.setBrightness(0)
                strip1.show()
            else:
                if colors[0].lower() == 'wipe':
                    strip1.setBrightness(255)
                    color_wipe(strip1, form_color(colors))
                elif colors[0].lower() == 'block':
                    strip1.setBrightness(255)
                    color_block(strip1, form_color(colors))
                elif colors[0].lower() == 'chase':
                    strip1.setBrightness(255)
                    theater_chase(strip1, form_color(colors))
                    main_check()
                elif colors[0].lower() == 'rainbow':
                    strip1.setBrightness(int(colors[4]))
                    rainbow(strip1)
                    main_check()
                elif colors[0].lower() == 'rainbow_cycle':
                    strip1.setBrightness(int(colors[4]))
                    rainbow_cycle(strip1)
                    main_check()
                elif colors[0].lower() == 'rainbow_chase':
                    strip1.setBrightness(int(colors[4]))
                    theater_chase_rainbow(strip1)
                    main_check()
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
