from machine import Pin, I2C
import ssd1306
import hmc5883l

# Initialize I2C bus
i2c = I2C(scl=Pin(5), sda=Pin(4))

# Initialize OLED display
oled_width = 128
oled_height = 64
oled = ssd1306.SSD1306_I2C(oled_width, oled_height, i2c)

# Initialize magnetometer
mag = hmc5883l.HMC5883L(scl=5, sda=4)

while True:
    # Read magnetometer data
    x, y, z = mag.read()

    # Clear the OLED display
    oled.fill(0)

    # Write the magnetometer data to the OLED display
    oled.text('X: ' + str(x), 0, 0)
    oled.text('Y: ' + str(y), 0, 10)
    oled.text('Z: ' + str(z), 0, 20)

    # Show the OLED display
    oled.show()
