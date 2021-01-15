import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from rpi_ws281x import *
import argparse
import sys
import config as C
import random
from strand import Strand


STRANDS = []


sys.stdout.write('init strips and strands... ')
parser = argparse.ArgumentParser()
parser.add_argument('-c', '--clear', action='store_true', help='clear the display on exit')
args = parser.parse_args()

for s in C.STRIPS:
    strip = Adafruit_NeoPixel(C.CONFIGS[s]['LED_COUNT'],
                              C.CONFIGS[s]['PIN'],
                              C.CONFIGS[s]['FREQ_HZ'],
                              C.CONFIGS[s]['DMA'],
                              C.CONFIGS[s]['INVERT'],
                              C.CONFIGS[s]['BRIGHTNESS'],
                              C.CONFIGS[s]['CHANNEL'])
    strip.begin()
    STRANDS.append(Strand(strip))

sys.stdout.write('done. \n')


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