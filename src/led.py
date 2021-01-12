from rpi_ws281x import *


class LED:

    strip = None
    place = None
    r = 0
    g = 0
    b = 0
    brightness = 0
    dim_level = 100
    active = 1

    def __init__(self, strip, place):
        self.strip = strip
        self.place = place

    def check(self):
        # check status, and activity, if dimming, or whatever, run that, return 1 if completed and status updated
        pass

    def update(self, show=False):
        self.strip.setPixelColor(self.place, self.form_color(self.r, self.g, self.b, self.get_bo()))
        if show:
            self.strip.show()

    def set_color(self, color, show=False):
        self.strip.setPixelColor(self.place, color)
        if show:
            self.strip.show()

    def dim_in(self):
        if self.dim_level >= 100:
            return self.dim_level

    def dim_out(self):
        if self.dim_level <= 0:
            return self.dim_level

    def get_bo(self):
        return int(self.brightness) * int(self.dim_level) / 100

    def form_color(self, r, g, b, bo):
        def form_value(loc):
            return int((bo if bo != -1 else int(self.brightness)) * int(loc) / 255)
        return Color(form_value(r), form_value(g), form_value(b))

    def form_color_from_status(self, status, brightness_override=-1):
        return self.form_color(status[1], status[2], status[3], bo=brightness_override)
