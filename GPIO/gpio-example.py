'''Justin Johnson
Raspberry Pi GPIO with Python
Notes listed below taken from https://sourceforge.net/p/raspberry-gpio-python/wiki/BasicUsage/

PNP Communication between vision system and control system

Need simple communication with with PIC microcontroller to handle below functionality:
Line 1 = A
Line 2 = B
A B | Procedure
------------------------------------------------------------------------------------------
0 0 | Do nothing
0 1 | Capture image of fiducial
1 0 | Capture image of component in light box, find orientation, adjust rotation as needed
1 1 | TBD

???
How to communicate to PIC any error or displacement found when checking fiducial locations or when checking IC center position
Simple GPIO communication may not suffice if required to send PIC displacement values or move commands 
???

Another option is to allow PIC and PC to communciate through USB, and PC and Raspi to communicate through SSH
pick up part
move to light box
PIC -> PC (USB) "rotate component"
PC -> Raspi (SSH) "rotate component"
Raspi -> PC (SSH) "rotation complte, xDisplacement = -0.023, yDisplacement = 0.00"
PC -> PIC (USB) "rotation complete, xDisplacement = -0.023, yDisplacement= 0.00"

Goal: Direct PIC <--> Raspi communication will increase speed, reduce error, and simplify debug
'''
import RPi.GPIO as GPIO

'''
There are two ways of numbering the IO pins on a Raspberry Pi within RPi.GPIO. The first is using the BOARD numbering system. This refers to the pin numbers on the P1 header of the Raspberry Pi board. The advantage of using this numbering system is that your hardware will always work, regardless of the board revision of the RPi. You will not need to rewire your connector or change your code.
The second numbering system is the BCM numbers. This is a lower level way of working - it refers to the channel numbers on the Broadcom SOC. You have to always work with a diagram of which channel number goes to which pin on the RPi board. Your script could break between revisions of Raspberry Pi boards.
To specify which you are using using (mandatory):
GPIO.setmode(GPIO.BOARD)
  # or
GPIO.setmode(GPIO.BCM)
To detect which pin numbering system has been set (for example, by another Python module):
mode = GPIO.getmode()
'''

GPIO.setmode(GPIO.BOARD)


'''
You need to set up every channel you are using as an input or an output. To configure a channel as an input:
GPIO.setup(channel, GPIO.IN)
You can also specify an initial value for your output channel:
GPIO.setup(channel, GPIO.OUT, initial=GPIO.HIGH)
'''

GPIO.setup(pic_input, GPIO.IN)
GPIO.setup(led1, GPIO.OUT, initial=GPIO.HIGH)


'''
To read the value of a GPIO pin:
GPIO.input(channel)
(where channel is the channel number based on the numbering system you have specified (BOARD or BCM)). This will return either 0 / GPIO.LOW / False or 1 / GPIO.HIGH / True.
'''
pic_signal = GPIO.input(pic_input)

#while waiting for signal from PIC system, do nothing
while pic_signal == GPIO.LOW:
  sleep()

  
'''
Interrupts and Edge detection
An edge is the change in state of an electrical signal from LOW to HIGH (rising edge) or from HIGH to LOW (falling edge). Quite often, we are more concerned by a change in state of an input than it's value. This change in state is an event.
To avoid missing a button press while your program is busy doing something else, there are two ways to get round this:
the wait_for_edge() function
the event_detected() function
a threaded callback function that is run when an edge is detected
'''

'''
wait_for_edge() function
The wait_for_edge() function is designed to block execution of your program until an edge is detected. In other words, the example above that waits for a button press could be rewritten as:
GPIO.wait_for_edge(channel, GPIO.RISING)
Note that you can detect edges of type GPIO.RISING, GPIO.FALLING or GPIO.BOTH. The advantage of doing it this way is that it uses a negligible amount of CPU, so there is plenty left for other tasks.
If you only want to wait for a certain length of time, you can use the timeout parameter:
# wait for up to 5 seconds for a rising edge (timeout is in milliseconds)
channel = GPIO.wait_for_edge(channel, GPIO_RISING, timeout=5000)
if channel is None:
    print('Timeout occurred')
else:
    print('Edge detected on channel', channel)
'''

GPIO.wait_for_edge(pic_input, GPIO_RISING)

'''
event_detected() function
The event_detected() function is designed to be used in a loop with other things, but unlike polling it is not going to miss the change in state of an input while the CPU is busy working on other things. This could be useful when using something like Pygame or PyQt where there is a main loop listening and responding to GUI events in a timely basis.
GPIO.add_event_detect(channel, GPIO.RISING)  # add rising edge detection on a channel
do_something()
if GPIO.event_detected(channel):
    print('Button pressed')
Note that you can detect events for GPIO.RISING, GPIO.FALLING or GPIO.BOTH.
'''

GPIO.add_event_detect(pic_input, GPIO.RISING)
do_something()
if GPIO.event_detected(pic_input):
  print('PIC signalled Pi\nProcessing Image...\n')
  
'''
Threaded callbacks
RPi.GPIO runs a second thread for callback functions. This means that callback functions can be run at the same time as your main program, in immediate response to an edge. For example:

def my_callback(channel):
    print('This is a edge event callback function!')
    print('Edge detected on channel %s'%channel)
    print('This is run in a different thread to your main program')

GPIO.add_event_detect(channel, GPIO.RISING, callback=my_callback)  # add rising edge detection on a channel
...the rest of your program...

def my_callback_one(channel):
    print('Callback one')

def my_callback_two(channel):
    print('Callback two')

GPIO.add_event_detect(channel, GPIO.RISING)
GPIO.add_event_callback(channel, my_callback_one)
GPIO.add_event_callback(channel, my_callback_two)
Note that in this case, the callback functions are run sequentially, not concurrently. This is because there is only one thread used for callbacks, in which every callback is run, in the order in which they have been defined.
'''

def pic_input_A_triggered(pic_input_A):
    do_something_A()
    print('This is a edge event callback function!')
    print('This is run in a different thread to your main program')
    
def pic_input_B_triggered(pic_input_B):
    do_something_A()
    print('This is a edge event callback function!')
    print('This is run in a different thread to your main program')

GPIO.add_event_detect(pic_input_A, GPIO.RISING, callback = pic_input_B_triggerred, bouncetime=200)
GPIO.add_event_detect(pic_input_B, GPIO.RISING, callback = pic_input_B_triggerred, bouncetime=200)



'''
Switch debounce
You may notice that the callbacks are called more than once for each button press. This is as a result of what is known as 'switch bounce'. There are two ways of dealing with switch bounce:
add a 0.1uF capacitor across your switch.
software debouncing
a combination of both
To debounce using software, add the bouncetime= parameter to a function where you specify a callback function. Bouncetime should be specified in milliseconds. For example:
# add rising edge detection on a channel, ignoring further edges for 200ms for switch bounce handling
GPIO.add_event_detect(channel, GPIO.RISING, callback=my_callback, bouncetime=200)
or
GPIO.add_event_callback(channel, my_callback, bouncetime=200)
'''