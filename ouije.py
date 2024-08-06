from machine import Pin, I2C, UART
import ssd1306
import hmc5883l
import time
import network

# Initialize UART for serial communication
uart = UART(0, baudrate=115200)
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
threshold = 9
delay = 100
buffer = [' '] * 20

# Define alphabet
alphabet = 'abcdefghijklm nopqrstuvwxyz '

# Take baseline sensor reading
prev_reading = mag.read()

def draw_splash_screen():
    # Clear the screen and invert the background
    oled.fill(1)
    oled.show()

    # Display "Oui, Je?" in large letters centered on the screen
    oled.text("Oui, Je?", 10, 20, 0)
    oled.show()

    # Connect to AP "Hufford" with key "FloridaMan25!"
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.scan()
    wlan.connect('Hufford', 'FloridaMan25!')
    while not wlan.isconnected():
        pass
        uart.write("connecting...\n")

    # Display network information
    oled.text(" " + wlan.ifconfig()[0], 0, 40, 0)
    oled.show()

    # Print network information to serial
    uart.write("IP: " + wlan.ifconfig()[0] + "\n")
    # Pause for 5 seconds
    time.sleep(5)

    # Down wipe effect to clear the splash screen
    for i in range(64):
        oled.fill_rect(0, 63 - i, 128, 1, 0)
        oled.show()
        time.sleep_ms(10)

def draw_letters():
    # Print letters on the OLED display
    oled.fill(0)
    for i in range(28):
        oled.text(alphabet[i], (i % 14) * 8 + (128 - 14 * 8) // 2, 10 * (i // 14) + 5)
    oled.show()

def display_and_read(start, end, line):
    global prev_reading
    prev_reading = mag.read()
    for i in range(start, end):
        # uninvert previous letter
        oled.fill_rect((i - 1) % 14 * 8 + (128 - 14 * 8) // 2, line+5, 8, 10, 0)
        oled.text(alphabet[i - 1], (i - 1) % 14 * 8 + (128 - 14 * 8) // 2, line+5, 1)
        oled.show()
        # Invert the current letter
        oled.fill_rect((i % 14) * 8 + (128 - 14 * 8) // 2, line+5, 8, 10, 1)
        oled.text(alphabet[i], (i % 14) * 8 + (128 - 14 * 8) // 2, line+5, 0)
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
        prev_reading = reading

# Take sensor reading before displaying anything
draw_splash_screen()
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

