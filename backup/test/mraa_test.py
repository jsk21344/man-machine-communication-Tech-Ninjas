import mraa
import time

# initialise gpio 23
gpio_1 = mraa.Gpio(17)

# initialise gpio 24
gpio_2 = mraa.Gpio(18)

# set gpio 23 to output
gpio_1.dir(mraa.DIR_OUT)

# set gpio 24 to output
gpio_2.dir(mraa.DIR_OUT)

# toggle both gpio's
while True:
    gpio_1.write(1)
    gpio_2.write(0)

    time.sleep(1)

    gpio_1.write(0)
    gpio_2.write(1)

    time.sleep(1)
