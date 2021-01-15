# DEPRECATED, in until release to allow old app to continue to work
LED_COUNT = 300
LED_S1 = 18
LED_S2 = 12
LED_FREQ_HZ = 800000
LED_DMA1 = 10
LED_DMA2 = 11
LED_BRIGHTNESS = 64
LED_INVERT = False
LED_CHANNEL1 = 0
LED_CHANNEL2 = 0
# END DEPRECATED

# add or remove indexes for strip labeling, must always contain `0`
# STRIPS = [0]  # ONE strip
STRIPS = [0, 1]  # TWO strips

# config for each strip in `STRIPS`, will not be used if index not also in `STRIPS`
CONFIGS = {
    0: {
        'LED_COUNT': 300,
        'PIN': 18,
        'FREQ_HZ': 800000,
        'DMA': 10,
        'BRIGHTNESS': 80,
        'INVERT': False,
        'CHANNEL': 0
    },
    1: {
        'LED_COUNT': 300,
        'PIN': 12,
        'FREQ_HZ': 800000,
        'DMA': 11,
        'BRIGHTNESS': 80,
        'INVERT': False,
        'CHANNEL': 0
    }
}
