import RPi.GPIO as GPIO
import time

data_pin = 14
clock_pin = 19
# Set up the GPIO pins
GPIO.setmode(GPIO.BCM)
GPIO.setup(data_pin, GPIO.IN)
GPIO.setup(clock_pin, GPIO.OUT)

# Read data from the HX711
def read_hx711():
    # Set the clock pin high and then low to start a conversion
    GPIO.output(clock_pin, GPIO.HIGH)
    GPIO.output(clock_pin, GPIO.LOW)

    # Wait for the conversion to complete
    while GPIO.input(data_pin) == GPIO.HIGH:
        pass

    # Read the data from the HX711
    data = 0
    for i in range(24):
        GPIO.output(clock_pin, GPIO.HIGH)
        data = (data << 1) | GPIO.input(data_pin)
        GPIO.output(clock_pin, GPIO.LOW)

    # Set the gain of the HX711 (optional)
    for i in range(64):
        GPIO.output(clock_pin, GPIO.HIGH)
        GPIO.output(clock_pin, GPIO.LOW)

    # Return the data
    return data


while True:
    time.sleep(0.1)
    data = read_hx711()
    print(data)
