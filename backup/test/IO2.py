import mraa 
import time

BUTTON_GPIO = 14               # The button GPIO
btn = mraa.Gpio(BUTTON_GPIO)   # Get the button pin object
btn.dir(mraa.DIR_IN)           # Set the direction as input

while 1:
        if (btn.read() != 0):
			print("An")
		else:
			print("Aus")