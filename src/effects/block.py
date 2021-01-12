'''
wanna be able to fully block
block half
block alternating count
block half and rotate at speed
block alternating count and rotate at speed
'''


def full(strand, status):
    strand.set_color(status[1], status[2], status[3])


def half(strand, status):
    strand.set_color(status[1], status[2], status[3], range_start=0, range_end=strand.length/2)
    strand.set_color(status[6], status[7], status[8], range_start=strand.length/2, range_end=strand.length+1)


def alternating_count(strand, status):
    pass


def block(strand, status):
    # TODO rename 'block' in home.html to 'block_full'
    effect = status[0].replace('block_', '')
    # check for individual effects
