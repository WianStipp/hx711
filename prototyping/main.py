import machine
import utime
from machine import Pin, SPI, PWM
import framebuf

# LCD Pins
BL = 13
DC = 8
RST = 12
MOSI = 11
SCK = 10
CS = 9
# Constants for 0g and 461g
ZERO_READING = 203100
KNOWN_READING = 570000
KNOWN_WEIGHT = 461
CONVERSION_FACTOR = (ZERO_READING - KNOWN_READING) / KNOWN_WEIGHT

# HX711 Pins
data_pin = machine.Pin(14, machine.Pin.IN)
clock_pin = machine.Pin(19, machine.Pin.OUT)


class LCD_1inch14(framebuf.FrameBuffer):
    def __init__(self):
        self.width = 240
        self.height = 135

        self.cs = Pin(CS, Pin.OUT)
        self.rst = Pin(RST, Pin.OUT)

        self.cs(1)
        self.spi = SPI(1)
        self.spi = SPI(1, 1000_000)
        self.spi = SPI(
            1, 10000_000, polarity=0, phase=0, sck=Pin(SCK), mosi=Pin(MOSI), miso=None
        )
        self.dc = Pin(DC, Pin.OUT)
        self.dc(1)
        self.buffer = bytearray(self.height * self.width * 2)
        super().__init__(self.buffer, self.width, self.height, framebuf.RGB565)
        self.init_display()

        self.red = 0x07E0
        self.green = 0x001F
        self.blue = 0xF800
        self.white = 0xFFFF

    def write_cmd(self, cmd):
        self.cs(1)
        self.dc(0)
        self.cs(0)
        self.spi.write(bytearray([cmd]))
        self.cs(1)

    def write_data(self, buf):
        self.cs(1)
        self.dc(1)
        self.cs(0)
        self.spi.write(bytearray([buf]))
        self.cs(1)

    def init_display(self):
        """Initialize dispaly"""
        self.rst(1)
        self.rst(0)
        self.rst(1)

        self.write_cmd(0x36)
        self.write_data(0x70)

        self.write_cmd(0x3A)
        self.write_data(0x05)

        self.write_cmd(0xB2)
        self.write_data(0x0C)
        self.write_data(0x0C)
        self.write_data(0x00)
        self.write_data(0x33)
        self.write_data(0x33)

        self.write_cmd(0xB7)
        self.write_data(0x35)

        self.write_cmd(0xBB)
        self.write_data(0x19)

        self.write_cmd(0xC0)
        self.write_data(0x2C)

        self.write_cmd(0xC2)
        self.write_data(0x01)

        self.write_cmd(0xC3)
        self.write_data(0x12)

        self.write_cmd(0xC4)
        self.write_data(0x20)

        self.write_cmd(0xC6)
        self.write_data(0x0F)

        self.write_cmd(0xD0)
        self.write_data(0xA4)
        self.write_data(0xA1)

        self.write_cmd(0xE0)
        self.write_data(0xD0)
        self.write_data(0x04)
        self.write_data(0x0D)
        self.write_data(0x11)
        self.write_data(0x13)
        self.write_data(0x2B)
        self.write_data(0x3F)
        self.write_data(0x54)
        self.write_data(0x4C)
        self.write_data(0x18)
        self.write_data(0x0D)
        self.write_data(0x0B)
        self.write_data(0x1F)
        self.write_data(0x23)

        self.write_cmd(0xE1)
        self.write_data(0xD0)
        self.write_data(0x04)
        self.write_data(0x0C)
        self.write_data(0x11)
        self.write_data(0x13)
        self.write_data(0x2C)
        self.write_data(0x3F)
        self.write_data(0x44)
        self.write_data(0x51)
        self.write_data(0x2F)
        self.write_data(0x1F)
        self.write_data(0x1F)
        self.write_data(0x20)
        self.write_data(0x23)

        self.write_cmd(0x21)

        self.write_cmd(0x11)

        self.write_cmd(0x29)

    def show(self):
        self.write_cmd(0x2A)
        self.write_data(0x00)
        self.write_data(0x28)
        self.write_data(0x01)
        self.write_data(0x17)

        self.write_cmd(0x2B)
        self.write_data(0x00)
        self.write_data(0x35)
        self.write_data(0x00)
        self.write_data(0xBB)

        self.write_cmd(0x2C)

        self.cs(1)
        self.dc(1)
        self.cs(0)
        self.spi.write(self.buffer)
        self.cs(1)


def read_hx711():
    # Set the clock pin high and then low to start a conversion
    clock_pin.value(1)
    clock_pin.value(0)

    # Wait for the conversion to complete
    while data_pin.value() == 1:
        pass

    # Read the data from the HX711
    data = 0
    for _ in range(24):
        clock_pin.value(1)
        data = (data << 1) | data_pin.value()
        clock_pin.value(0)

    # Set the gain of the HX711 (optional)
    for _ in range(64):
        clock_pin.value(1)
        clock_pin.value(0)

    # Return the weight
    weight = (ZERO_READING - data) / CONVERSION_FACTOR
    return weight


if __name__ == "__main__":
    pwm = PWM(Pin(BL))
    pwm.freq(1000)
    pwm.duty_u16(32768)  # max 65535

    LCD = LCD_1inch14()
    # color BRG
    LCD.fill(LCD.white)

    LCD.show()
    LCD.text("github.com/WianStipp/hx711", 20, 50, LCD.red)

    LCD.hline(10, 10, 220, LCD.blue)
    LCD.hline(10, 125, 220, LCD.blue)
    LCD.vline(10, 10, 115, LCD.blue)
    LCD.vline(230, 10, 115, LCD.blue)

    LCD.rect(12, 12, 20, 20, LCD.red)
    LCD.rect(12, 103, 20, 20, LCD.red)
    LCD.rect(208, 12, 20, 20, LCD.red)
    LCD.rect(208, 103, 20, 20, LCD.red)

    LCD.show()

    while True:
        utime.sleep(0.1)
        weight = read_hx711()
        LCD.fill_rect(60, 70, 200, 30, LCD.white)  # Clear the previous weight
        LCD.text(f"Weight: {weight}", 60, 70, LCD.green)  # Display the weight
        LCD.show()
