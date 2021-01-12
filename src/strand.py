from led import LED


class Strand:

    LEDs = []
    strip = None
    length = 0

    def __init__(self, strip):
        self.strip = strip
        for i in range(strip.numPixels()):
            self.LEDs.append(LED(strip, i))
        self.length = self.strip.numPixels()

    def update_all(self):
        for led in self.LEDs:
            led.update()

    def set_color(self, r, g, b, range_start=0, range_end=-1):
        def run_update(ledx):
            ledx.r = r
            ledx.g = g
            ledx.b = b
            ledx.update()
        count = 0
        for led in self.LEDs:
            if int(range_end) != -1:
                if int(range_start) <= count < int(range_end):
                    run_update(led)
            else:
                run_update(led)
            count = count + 1
