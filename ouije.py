'''reitsuban - spirit communication box '''

from machine import Pin, I2C
import ssd1306
import hmc5883l
import time
import network
import framebuf
import machine

machine.freq(160000000)

# Initialize I2C bus
i2c = I2C(scl=Pin(5), sda=Pin(4),freq=400000)

# Initialize OLED display
oled_width = 128
oled_height = 64
oled = ssd1306.SSD1306_I2C(oled_width, oled_height, i2c)

# Initialize magnetometer
mag = hmc5883l.HMC5883L(scl=5, sda=4)
prev_reading = (0, 0, 0)
reading = (0, 0, 0)

# Define threshold and buffer
threshold = 9
delay = 100
buffer = [' '] * 20

# Define alphabet
alphabet = 'abcdefghijklmnopqrstuvwxyz '

# Take baseline sensor reading
prev_reading = mag.read()

def draw_splash_screen():
    fb = framebuf.FrameBuffer(bytearray(
    b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x80\xc0\xc0\xe0\xe0\xf0\xf0\xf0\xf0\xf0\xf0\xf0\xf0\xe0\xe0\xe0\xc0\x80\x00\x00\x00\x00'
    b'\x00\x00\x00\x30\x30\x30\x30\x30\x30\x30\x30\x30\x30\xf0\xf0\xf0\x30\x30\x30\x30\x30\x30\x30\x30\x30\x30\x00\x00\x00\x00\x00\x00'
    b'\x00\x00\x00\x60\xf0\xe0\xc0\x80\x00\x00\x70\x70\x70\x70\x70\xf0\x70\x70\x70\x70\x70\xf0\xf0\xf0\xf0\x70\x20\x20\x00\x00\x00\x00'
    b'\x00\x00\x00\x00\x00\xc0\xc0\xc0\xc0\xf8\xf8\xc8\xc0\xc0\xc0\x00\x00\x00\x00\xf0\xf0\x30\x30\x30\xf0\xf0\x00\x00\x00\x00\x00\x00'
    b'\x00\x00\x00\x00\x00\x00\x00\xf0\xfe\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xfe\xf8\x00'
    b'\x3f\x3f\x3f\x03\xb3\xb3\xb3\xb3\xb3\xb3\xb3\xb3\x03\xff\xff\xff\x03\xb3\xb3\xb3\xb3\xb3\xb3\xb3\x03\x3f\x3f\x3f\x00\x00\x00\x00'
    b'\x00\x00\x00\x00\x00\x01\x03\x03\x01\x00\xf0\xf0\xf0\x30\x33\x33\x33\xf7\xf7\xff\x3f\x3f\x35\x30\x30\xf0\xf0\xf0\x00\x00\x00\x00'
    b'\x00\x10\x70\x30\x30\xff\xff\x30\x31\xf7\xf6\x30\x10\xff\xff\x18\x18\x60\x6e\xef\xe3\x60\x60\x60\x67\xe7\xec\xec\x4e\x0f\x07\x00'
    b'\x00\x00\x00\x00\x00\x00\x00\x03\x1f\x7f\xff\xc7\x01\x01\x01\x01\x83\xff\xff\xff\xff\xc7\x01\x01\x01\x01\x83\xff\xff\x3f\x07\x00'
    b'\x00\x80\x80\x80\x99\x99\x99\x99\x99\x99\x99\x99\x98\x9b\x9b\x9b\x98\x99\x99\x99\x99\x99\x99\x99\x98\x80\x80\x00\x00\x00\x00\x00'
    b'\x00\x07\x07\x07\xff\xff\xff\x00\x00\x00\xff\xff\xff\x63\x63\x63\x63\xff\xff\xff\x63\x63\x63\x63\x63\xff\xff\xff\x00\x00\x00\x00'
    b'\x00\x00\x20\x30\x3c\x1f\xc7\xc0\xc0\xc7\xc7\xf0\xf0\xff\xdf\xc0\xd0\xf0\xf8\xd8\xd9\xdf\xce\xce\xdf\xdb\xd9\x38\x38\x30\x30\x00'
    b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x07\x0f\x0f\xdf\x9f\x3f\x7f\x73\x71\x70\x71\x7f\x7f\x1f\xdf\x0f\x0f\x07\x01\x00\x00\x00'
    b'\xc0\xc1\xc1\xc1\xc5\xdf\xff\xd9\xc1\xc1\xc1\xff\xff\xc1\xc1\xc1\xff\xff\xc1\xc1\xc1\xd9\xff\xdf\xc5\xc1\xc1\xc0\xc0\x00\x00\x00'
    b'\x00\xe0\xe0\xf0\x7f\x3f\x1f\x38\x70\xe0\xef\xef\xef\xe0\xe0\xe0\xe0\xef\xef\xef\xe0\xe0\xe0\xfc\xfc\xff\xff\xe7\xe0\xe0\x00\x00'
    b'\x00\x00\xc0\xc0\xc0\xc0\xff\xff\xc0\xc0\xc0\xc0\xff\xff\xc0\xc0\xc0\xc0\xff\xff\xc0\xc0\xc0\xc0\xc0\xff\xff\xc0\xc0\xc0\xc0\x00'
    b'\x00\x00\x60\xf0\xf0\xf0\xe0\xc0\x80\x00\x00\x00\x00\x03\x07\x06\x1c\x3c\x3c\x3c\x3c\x1c\x0e\x07\x03\x00\x00\x00\x00\x00\x80\xc0'
    b'\xe0\xe0\xe0\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
    b'\x00\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
    b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
    b'\x00\x04\x0e\x0f\x0f\x07\x07\x07\x07\x0f\x0e\x0e\x1e\x1c\x3c\xb8\xf8\xf0\xf0\xf0\xf0\xf8\xf8\x38\x3c\x1c\x1e\x0e\x0f\x07\x07\x07'
    b'\x0f\x0f\x1f\x1e\x00\x00\x00\x00\x00\x00\x00\xc0\xc0\xc0\xc0\xc0\xc0\xc0\x80\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
    b'\x00\xc0\xc0\x00\x00\x00\xc0\xc0\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
    b'\x00\xe0\xe0\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
    b'\x00\xc0\xe0\xe0\xf0\xf0\xf0\xf0\xf0\xf8\x7c\x3c\x1e\x0f\x0f\x07\x03\x03\x01\x01\x03\x03\x07\x07\x0f\x1e\x3e\x7c\xf8\xf8\xf0\xf0'
    b'\xf0\xf0\xe0\xe0\x00\x00\x00\x00\x00\x00\x00\xff\xff\x30\x30\x70\xf0\xd9\x9f\x07\x00\xf8\xfc\x6c\x66\x66\x66\x66\x6c\x7c\x70\x00'
    b'\x00\xfe\xfe\x00\x00\x06\xff\xff\x06\x06\x06\x06\x3c\x3e\x66\x66\x66\x46\xc6\x8c\x00\x00\xfe\xfe\x00\x00\x00\x00\xfe\xfe\x00\x00'
    b'\x00\xff\xff\x04\x06\x06\x06\x8e\xfc\xf0\x00\xc0\xe6\x76\x36\x36\x36\x36\xfc\xf8\x00\x00\x00\xfe\xfe\x0c\x06\x06\x0e\xfe\xf8\x00'
    b'\x00\x01\x03\x03\x03\x03\x07\x07\x07\x03\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01\x03\x07\x07'
    b'\x03\x01\x01\x00\x00\x00\x00\x00\x00\x00\x00\x07\x07\x00\x00\x00\x00\x01\x03\x07\x04\x01\x03\x03\x06\x06\x06\x06\x06\x06\x03\x00'
    b'\x00\x07\x07\x00\x00\x00\x03\x07\x06\x06\x06\x06\x03\x06\x06\x06\x06\x06\x03\x01\x00\x00\x03\x07\x06\x06\x06\x03\x07\x07\x00\x00'
    b'\x00\x07\x07\x06\x06\x06\x06\x03\x03\x00\x00\x03\x07\x06\x06\x06\x02\x03\x07\x07\x00\x00\x00\x07\x07\x00\x00\x00\x00\x07\x07\x00'),
    128, 64, framebuf.MONO_VLSB)
    oled.blit(fb, 0, 0)
    oled.show()
    time.sleep(2)

'''
    # Connect to AP "Hufford" with key "FloridaMan25!"
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.scan()
    wlan.connect('Hufford', 'FloridaMan25!')
    while not wlan.isconnected():
        pass


    #time.sleep(2)
    # Clear the OLED display
    oled.fill(0)
    oled.show()
'''

def draw_letters():
    # Open the bitmap file

    fbuf = framebuf.FrameBuffer(bytearray(
    b'\x00\x00\x00\x00\x00\xc0\xe0\xa0\xa0\xe0\xc0\x00\x00\x00\x00\x00\x00\x00\x00\xe0\xe0\xa0\xa0\xe0\x40\x00\x00\x00\x00\x00\x00\x00'
    b'\x00\xc0\xe0\x20\x20\x60\x40\x00\x00\x00\x00\x00\x00\x00\x00\xe0\xe0\x20\x20\xe0\xc0\x00\x00\x00\x00\x00\x00\x00\x00\xe0\xe0\xa0'
    b'\xa0\x20\x20\x00\x00\x00\x00\x00\x00\x00\x00\xe0\xe0\xa0\xa0\x20\x20\x00\x00\x00\x00\x00\x00\x00\x00\xc0\xe0\x20\xa0\xa0\xa0\x00'
    b'\x00\x00\x00\x00\x00\x00\x00\xe0\xe0\x80\x80\xe0\xe0\x00\x00\x00\x00\x00\x00\x00\x00\x00\x20\xe0\xe0\x20\x00\x00\x00\x00\x00\x00'
    b'\x00\x00\x00\x00\x00\x1f\x1f\x01\x01\x1f\x1f\x00\x00\x00\x00\x00\x00\x00\x00\x1f\x1f\x19\x19\x1f\x0f\x00\x00\x00\x00\x00\x00\x00'
    b'\x00\x0f\x1f\x18\x18\x1c\x0c\x00\x00\x00\x00\x00\x00\x00\x00\x1f\x1f\x18\x18\x1f\x0f\x00\x00\x00\x00\x00\x00\x00\x00\x1f\x1f\x19'
    b'\x19\x18\x18\x00\x00\x00\x00\x00\x00\x00\x00\x1f\x1f\x01\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x0f\x1f\x18\x19\x1f\x0f\x00'
    b'\x00\x00\x00\x00\x00\x00\x00\x1f\x1f\x01\x01\x1f\x1f\x00\x00\x00\x00\x00\x00\x00\x00\x00\x18\x1f\x1f\x18\x00\x00\x00\x00\x00\x00'
    b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\xe0\xe0\x00\x00\x00\x00\x00\x00\x00\x00\xe0\xe0\x80\xc0\x60\x20\x00\x00\x00\x00\x00\x00\x00'
    b'\x00\xe0\xe0\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xe0\xe0\xc0\xc0\xe0\xe0\x00\x00\x00\x00\x00\x00\x00\x00\xe0\xe0\xc0'
    b'\x80\xe0\xe0\x00\x00\x00\x00\x00\x00\x00\x00\xc0\xe0\x20\x20\xe0\xc0\x00\x00\x00\x00\x00\x00\x00\x00\xe0\xe0\xa0\xa0\xe0\x40\x00'
    b'\x00\x00\x00\x00\x00\x00\x00\xc0\xe0\x20\x20\xe0\xc0\x00\x00\x00\x00\x00\x00\x00\x00\xe0\xe0\xa0\xa0\xe0\x40\x00\x00\x00\x00\x00'
    b'\x00\x00\x00\x00\x00\x0c\x1c\x18\x18\x1f\x0f\x00\x00\x00\x00\x00\x00\x00\x00\x1f\x1f\x01\x03\x1f\x1e\x00\x00\x00\x00\x00\x00\x00'
    b'\x00\x1f\x1f\x18\x18\x18\x18\x00\x00\x00\x00\x00\x00\x00\x00\x1f\x1f\x01\x01\x1f\x1f\x00\x00\x00\x00\x00\x00\x00\x00\x1f\x1f\x01'
    b'\x03\x1f\x1f\x00\x00\x00\x00\x00\x00\x00\x00\x0f\x1f\x18\x18\x1f\x0f\x00\x00\x00\x00\x00\x00\x00\x00\x1f\x1f\x01\x01\x01\x00\x00'
    b'\x00\x00\x00\x00\x00\x00\x00\x0f\x1f\x18\x1c\x1f\x1f\x00\x00\x00\x00\x00\x00\x00\x00\x1f\x1f\x01\x01\x1f\x1f\x00\x00\x00\x00\x00'
    b'\x00\x00\x00\x00\x00\x40\xe0\xa0\xa0\xa0\x20\x00\x00\x00\x00\x00\x00\x00\x00\x20\x20\xe0\xe0\x20\x20\x00\x00\x00\x00\x00\x00\x00'
    b'\x00\xe0\xe0\x00\x00\xe0\xe0\x00\x00\x00\x00\x00\x00\x00\x00\xe0\xe0\x00\x00\xe0\xe0\x00\x00\x00\x00\x00\x00\x00\x00\xe0\xe0\x00'
    b'\x00\xe0\xe0\x00\x00\x00\x00\x00\x00\x00\x00\x20\x60\xc0\xc0\x60\x20\x00\x00\x00\x00\x00\x00\x00\x00\x20\x60\xc0\xc0\x60\x20\x00'
    b'\x00\x00\x00\x00\x00\x00\x00\x20\x20\x20\xa0\xe0\x60\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
    b'\x00\x00\x00\x00\x00\x0c\x1d\x19\x19\x1f\x0f\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x1f\x1f\x00\x00\x00\x00\x00\x00\x00\x00\x00'
    b'\x00\x0f\x1f\x18\x18\x1f\x0f\x00\x00\x00\x00\x00\x00\x00\x00\x03\x0f\x1e\x1e\x0f\x03\x00\x00\x00\x00\x00\x00\x00\x00\x1f\x1f\x0e'
    b'\x0e\x1f\x1f\x00\x00\x00\x00\x00\x00\x00\x00\x1e\x1f\x03\x03\x1f\x1e\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x1f\x1f\x00\x00\x00'
    b'\x00\x00\x00\x00\x00\x00\x00\x1c\x1e\x1f\x1b\x19\x18\x00\x00\x00\x00\x00\x00\x00\x00\x20\x20\x20\x20\x20\x20\x00\x00\x00\x00\x00'
    b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
    b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
    b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
    b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
    b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
    b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
    b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
    b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'),
    128, 64, framebuf.MONO_VLSB)


    # Draw the frame buffer on the OLED display
    oled.blit(fbuf, 0, 0)
    #oled.show()

def draw_box(row_index, column_index, invert_toggle):
    x = column_index * 14 + 4
    y = row_index * 16 + 4
    oled.rect(x-2, y-2, 13, 15, invert_toggle)  # Increased width and height by 2 pixels

def sense(current_letter, letter_index, threshold=13):
    global prev_reading
    reading = mag.read()
    delta = abs(reading[0] - prev_reading[0]) + abs(reading[1] - prev_reading[1]) + abs(reading[2] - prev_reading[2])
    prev_reading = reading
    if delta > threshold:
        buffer.pop(0)
        buffer.append(current_letter)
    oled.fill_rect(0, 52, 128, 8, 0)
    oled.text(''.join(buffer), 0, 52, 1)
    #oled.text(str(letter_index) + " " + current_letter, 0, 52, 1)

def display_and_read(start, end):
    letter_index = 0
    for row_index in range(3):
        for column_index in range(9):
            draw_box(row_index, column_index, 1) # draw box around current letter
            oled.show()
            sense(alphabet[letter_index],letter_index)
            draw_box(row_index, column_index, 0) # undraw box around current letter
            oled.show()

            letter_index += 1

draw_splash_screen()
draw_letters()
prev_reading = mag.read()

# Main loop
while True:
    display_and_read(0, 27)
    #oled.fill(0)
    oled.show()
