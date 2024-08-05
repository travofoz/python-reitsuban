from machine import Pin, I2C
import ssd1306
import hmc5883l
import time

# Initialize I2C bus
i2c = I2C(scl=Pin(5), sda=Pin(4))

# Initialize OLED display
oled_width = 128
oled_height = 64
oled = ssd1306.SSD1306_I2C(oled_width, oled_height, i2c)

# Initialize magnetometer
mag = hmc5883l.HMC5883L(scl=5, sda=4)
prev_reading = (0, 0, 0)
reading = (0, 0, 0)

# Define threshold and buffer
threshold = 5  # Increase the threshold to a more reasonable value
delay = 100  # Delay between character display
buffer = [' '] * 20

# Define alphabet
alphabet = 'ABCDEFGHIJKLM NOPQRSTUVWXYZ '

# Take baseline sensor reading
prev_reading = mag.read()

def draw_letters():
    # Print letters on the OLED display
    oled.fill(0)  # Clear the screen
    for i in range(28):
        oled.text(alphabet[i], (i % 14) * 8, 10 * (i // 14))
    oled.show()

def display_and_read(start, end, line):
    prev_reading = mag.read()
    for i in range(start, end):
        # Invert the current letter
        oled.fill_rect((i % 14) * 8, line, 8, 10, 1)
        oled.text(alphabet[i], (i % 14) * 8, line, 0)
        oled.show()

        # Take sensor reading for each character
        reading = mag.read()
        # Calculate delta from previous reading
        delta = abs(reading[0] - prev_reading[0]) + abs(reading[1] - prev_reading[1]) + abs(reading[2] - prev_reading[2])

        # If delta is greater than threshold, add character to buffer
        if delta > threshold:
            buffer.pop(0)
            buffer.append(alphabet[i])

        # Display the buffer on line 4
        oled.fill_rect(0, 40, 128, 8, 0)
        oled.text(''.join(buffer), 0, 40)
        oled.show()

        # Delay between each character
        #time.sleep_ms(delay)

        # Restore the previous letter
        oled.fill_rect((i % 14) * 8, line, 8, 10, 0)
        oled.text(alphabet[i], (i % 14) * 8, line)
        oled.show()

        # Update previous reading
        prev_reading = reading

# Take sensor reading before displaying anything
while True:
    # Draw all the letters
    draw_letters()
    # Display and read first 14 letters on line one
    display_and_read(0, 14, 0)

    # Display and read last 13 letters on line two
    display_and_read(14, 28, 10)

    # Blank the screen before starting the next iteration
    #oled.fill(0)
    #oled.show()