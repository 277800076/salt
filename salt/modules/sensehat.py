# -*- coding: utf-8 -*-
'''
Module for controlling the LED matrix on the SenseHat of a Raspberry Pi.
:maintainer:    Benedikt Werner <1benediktwerner@gmail.com>
:maturity:      new
:depends:       sense_hat Python module
'''

from __future__ import absolute_import
import logging

try:
    from sense_hat import SenseHat
    _sensehat = SenseHat()
    has_sense_hat = True
except ImportError, NameError:
    _sensehat = None
    has_sense_hat = False

log = logging.getLogger(__name__)

def __virtual__():
    '''
    Only load the module if SenseHat is available
    '''
    if has_sense_hat:
        return True
    else:
        return False, "The SenseHat excecution module can not be loaded: SenseHat unavailable.\nThis module can only be used on a Raspberry Pi with a SenseHat. Also make sure that the sense_hat python library is installed!"

def set_rotation(rotation, redraw=True):
    '''
    Sets the rotation of the Pi. This is useful if you are using it upside down
    or sideways to correct the orientation of the image being shown.

    rotation
        The angle to rotate the LED matrix to.
        Valid values are 0, 90, 180 and 270.
    redraw
        Whether to redraw what is already being displayed on the LED matrix.

    CLI Example:

    .. code-block:: bash

    salt 'raspberry' sensehat.set_rotation 90
    salt 'raspberry' sensehat.set_rotation 180 False
    '''
    _sensehat.set_rotation(rotation, redraw)
    return {'rotation': rotation}

def set_pixels(pixels):
    '''
    Sets the entire LED matrix based on a list of 64 pixel values

    pixels
        A list of 64 color values [R, G, B].
    '''
    _sensehat.set_pixels(pixels)

def get_pixels():
    '''
    Returns a list of 64 smaller lists of `[R, G, B]` pixels representing the
    the currently displayed image on the LED matrix.

    Note: When using `set_pixels` the pixel values can sometimes change when
    you read them again using `get_pixels`. This is because we specify each
    pixel element as 8 bit numbers (0 to 255) but when they're passed into the
    Linux frame buffer for the LED matrix the numbers are bit shifted down
    to fit into RGB 565. 5 bits for red, 6 bits for green and 5 bits for blue.
    The loss of binary precision when performing this conversion
    (3 bits lost for red, 2 for green and 3 for blue) accounts for the
    discrepancies you see.

    The `get_pixels` method provides an accurate representation of how the
    pixels end up in frame buffer memory after you have called `set_pixels`.
    '''
    return _sensehat.get_pixels()

def set_pixel(x, y, color):
    '''
    Sets the a single pixel on the LED matrix to a specified color.

    x
        The x coodrinate of th pixel. Ranges from 0 on the left to 7 on the right.
    y
        The y coodrinate of th pixel. Ranges from 0 at the top to 7 at the bottom.
    color
        The new color of the pixel as a list of `[R, G, B]` values.

    CLI Example:

    .. code-block:: bash

    salt 'raspberry' sensehat.set_pixel 0 0 [255, 0, 0]
    '''
    _sensehat.set_pixel(x, y, color)

def get_pixel(x, y):
    '''
    Returns the color of a single pixel on the LED matrix.

    x
        The x coodrinate of th pixel. Ranges from 0 on the left to 7 on the right.
    y
        The y coodrinate of th pixel. Ranges from 0 at the top to 7 at the bottom.

    Note: Please read the note for `get_pixels`
    '''
    _sensehat.get_pixel(x, y)

def low_light(low_light=True):
    '''
    Sets the LED matrix to low light mode. Useful in a dark environment.

    CLI Example:

    .. code-block:: bash

    salt 'raspberry' sensehat.low_light
    salt 'raspberry' sensehat.low_light False
    '''

def show_message(message, msg_type=None,
        scroll_speed=0.1, text_color=[255, 255, 255], back_color=[0, 0, 0]):
    '''
    Displays a message on the LED matrix.

    message
        The message to display
    msg_type
        The type of the message. Changes the appearence of the message.
        Available types are:
            error:        red text
            warning:    orange text
            success:    green text
            info:        blue text
    scroll_speed
        The speed at which the message moves over the LED matrix.
        This value represents the time paused for between shifting the text
        to the left by one column of pixels.
    text_color
        The color in which the message is shown.
    back_color
        The background color of the display.

    CLI Example:

    .. code-block:: bash

        salt 'raspberry' sensehat.show_message 'Status ok'
        salt 'raspberry' sensehat.show_message 'Something went wrong' error
        salt 'raspberry' sensehat.show_message 'Red' text_color='[255, 0, 0]'
        salt 'raspberry' sensehat.show_message 'Hello world' None 0.2 [0, 0, 255] [255, 255, 0]
    '''

    color_by_type = {
        'error': [255, 0, 0],
        'warning': [255, 100, 0],
        'success': [0, 255, 255],
        'info': [0, 0, 255]
    }

    if msg_type in color_by_type:
        text_color = color_by_type[msg_type]

    _sensehat.show_message(message, scroll_speed, text_color, back_color)
    return {'message': message}

def show_letter(letter, text_color, back_color):
    '''
    Displays a single letter on the LED matrix.

    letter
        The letter to display
    text_color
        The color in which the letter is shown.
    back_color
        The background color of the display.

    CLI Example:

    .. code-block:: bash

    salt 'raspberry' sensehat.show_letter O
    salt 'raspberry' sensehat.show_letter X [255, 0, 0]
    salt 'raspberry' sensehat.show_letter B [0, 0, 255] [255, 255, 0]
    '''
    _sensehat.show_letter(letter, text_color, back_color)
    return {'letter': letter}

def show_image(image):
    '''
    Displays a 8 x 8 image on the LED matrix.

    image
        The path to the image to display. The image must be 8 x 8 pixels in size.

    CLI Example:

    .. code-block:: bash

    salt 'raspberry' sensehat.show_image /tmp/my_image.png
    '''
    _sensehat.load_image(image)
    return True

def clear(color=None):
    '''
    Sets the LED matrix to a single color or turns all LEDs off

    CLI Example:

    .. code-block:: bash

    salt 'raspberry' sensehat.clear
    salt 'raspberry' sensehat.clear [255, 0, 0]
    '''
    if color is None:
        _sensehat.clear()
    else:
        _sensehat.clear(color)
    return True
