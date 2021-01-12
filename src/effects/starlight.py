def starlight(strip):
    for i in range(strip.numPixels()):
        strip.setPixelColor(i, Color(0, 0, 0))
    strip.show()
    pixels_to_dim = pixels_to_shine(strip, normal_weight=(96, 4), on_weight=(85, 15), on_max_length=2)
    pixels_to_dim_solo = [i for i in range(strip.numPixels()) if pixels_to_dim[i] == 1]
    pixels_to_dim_info = {i: {'wait_time': random.randint(1, 1000), 'dim_level': 0, 'dim': 'in'} for i in pixels_to_dim_solo}

    while True:
        count = 0
        for i in pixels_to_dim_info:
            if pixels_to_dim_info[i]['dim'] == 'in':
                if pixels_to_dim_info[i]['wait_time'] > 0:
                    pixels_to_dim_info[i]['wait_time'] = pixels_to_dim_info[i]['wait_time'] - 1
                    count = count + 1
                elif pixels_to_dim_info[i]['dim_level'] < 100:
                    pixels_to_dim_info[i]['dim_level'] = dim_pixel_in_step(strip, int(i), status,
                                                                           dim_level=pixels_to_dim_info[i]['dim_level'])
                    count = count + 1
                elif pixels_to_dim_info[i]['wait_time'] <= 0 and pixels_to_dim_info[i]['dim_level'] >= 100:
                    pixels_to_dim_info[i]['dim'] = 'out'
                    pixels_to_dim_info[i]['wait_time'] = random.randint(1, 50)
                    count = count + 1
            elif pixels_to_dim_info[i]['dim'] == 'out':
                if pixels_to_dim_info[i]['wait_time'] > 0:
                    pixels_to_dim_info[i]['wait_time'] = pixels_to_dim_info[i]['wait_time'] - 1
                    count = count + 1
                elif pixels_to_dim_info[i]['dim_level'] > 0:
                    pixels_to_dim_info[i]['dim_level'] = dim_pixel_out_step(strip, int(i), status,
                                                                            dim_level=pixels_to_dim_info[i]['dim_level'])
                    count = count + 1
        if count == 0 or check_status() != status:
            break


    # import choosing from utils
# update led active state


'''
all have basically the same effect, allow for percentage multiplier.
'''


def mono_color():
    pass


def dual_color():
    pass


def multi_color():
    pass


def starlight(strand, status):
    effect = status[0].replace('starlight_', '')
