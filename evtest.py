from evdev import list_devices, InputDevice, categorize, ecodes
from select import select
import time

def list_devs():
	for path in list_devices():
		dev = InputDevice(path)
		print(dev.path, dev.name, dev.phys)

def find_gamepad():
	devs = []
	for path in list_devices():
#	for path in ['/dev/input/event7', '/dev/input/event8']:
		dev = InputDevice(path)
		if dev.name == "USB Gamepad ":
			devs.append(dev)
	return devs

def select_events():
	# A mapping of file descriptors (integers) to InputDevice instances.
	#devices = map(InputDevice, ('/dev/input/event7', '/dev/input/event8'))
	#devices = []
	devices = find_gamepad()
	devices = {dev.fd: dev for dev in devices}
	for dev in devices.values():
		print(dev)
	while True:
		r, w, x = select(devices, [], [])
		for fd in r:
			for event in devices[fd].read():
				print(fd)
				print_event(event)

def loop_events():
	dev = InputDevice('/dev/input/event7')
	print(dev.path, dev.name, dev.phys)
	for event in dev.read_loop():
		print_event(event)

def active_check():
	dev = InputDevice('/dev/input/event7')
	print(dev.path, dev.name, dev.phys)
	while True:
		keys = dev.active_keys()
		if len(keys):
			print keys
		pad = dev.absinfo(ecodes.ABS_X)
		if pad.value != 127:
			print ("DPAD X: ",  pad.value)

		pad = dev.absinfo(ecodes.ABS_Y)
		if pad.value != 127:
			print ("DPAD Y: ",  pad.value)
		time.sleep(0.1)


def print_event(event):
	if event.type == ecodes.EV_KEY:
		#print(categorize(event))
		#print(event.code, event.value)
		if (event.code == ecodes.BTN_THUMB and event.value == 1):
			print "KEY A pressed"
		elif (event.code == ecodes.BTN_THUMB and event.value == 0):
			print "KEY A released"
		elif (event.code == ecodes.BTN_THUMB2 and event.value == 1):
			print "KEY B pressed"
		elif (event.code == ecodes.BTN_THUMB2 and event.value == 0):
			print "KEY B released"

		if (event.code == ecodes.BTN_JOYSTICK and event.value == 1):
			print "KEY X pressed"
		elif (event.code == ecodes.BTN_JOYSTICK and event.value == 0):
			print "KEY X released"
		elif (event.code == ecodes.BTN_TOP and event.value == 1):
			print "KEY Y pressed"
		elif (event.code == ecodes.BTN_TOP and event.value == 0):
			print "KEY Y released"

		if (event.code == ecodes.BTN_BASE4 and event.value == 1):
			print "KEY START pressed"
		elif (event.code == ecodes.BTN_BASE4 and event.value == 0):
			print "KEY START released"
		elif (event.code == ecodes.BTN_BASE3 and event.value == 1):
			print "KEY SELECT pressed"
		elif (event.code == ecodes.BTN_BASE3 and event.value == 0):
			print "KEY SELECT released"

		if (event.code == ecodes.BTN_PINKIE and event.value == 1):
			print "KEY R-TRIG pressed"
		elif (event.code == ecodes.BTN_PINKIE and event.value == 0):
			print "KEY R-TRIG released"
		elif (event.code == ecodes.BTN_TOP2 and event.value == 1):
			print "KEY L-TRIG pressed"
		elif (event.code == ecodes.BTN_TOP2 and event.value == 0):
			print "KEY L-TRIG released"

	if event.type == ecodes.EV_ABS:
		if (event.code == ecodes.ABS_X and event.value == 0):
			print "DPAD LEFT pressed"
		elif (event.code == ecodes.ABS_X and event.value == 127):
			print "DPAD released"
		elif (event.code == ecodes.ABS_X and event.value == 255):
			print "DPAD RIGHT pressed"
		#print(event.code, event.value)
		elif (event.code == ecodes.ABS_Y and event.value == 0):
			print "DPAD UP pressed"
		elif (event.code == ecodes.ABS_Y and event.value == 127):
			print "DPAD released"
		elif (event.code == ecodes.ABS_Y and event.value == 255):
			print "DPAD DOWN pressed"

def main():
	#list_devs()
	#loop_events()
	#select_events()
	active_check()


main()

