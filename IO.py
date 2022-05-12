import mraa
import time

# initialise gpio 18
gpio_1 = mraa.Gpio(18)

# set gpio 23 to output
gpio_1.dir(mraa.DIR_OUT)


# toggle both gpio's
while True:
    if gpio_1.read() = true
		print("An")
	else:
	 print("Aus")
	time.sleep(0.25)