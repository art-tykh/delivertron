# A program to control the movement of a single motor using the RTK MCB!
# Composed by The Raspberry Pi Guy to accompany his tutorial!
# Let's import the modules we will need!
import time
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(True)

mhz = 100

M1_FORWARD = 7
M1_BACKWARD = 11
M2_FORWARD = 13
M2_BACKWARD = 15

FORWARD = 1
BACKWARD = -1
IDLE = 0

GPIO.setup(M1_FORWARD, GPIO.OUT) # 21
GPIO.setup(M1_BACKWARD, GPIO.OUT) # 20
GPIO.setup(M2_FORWARD, GPIO.OUT) # 16
GPIO.setup(M2_BACKWARD, GPIO.OUT) # 12

m1 = GPIO.PWM(M1_FORWARD, mhz)
m2 = GPIO.PWM(M1_BACKWARD, mhz)
m3 = GPIO.PWM(M2_FORWARD, mhz)
m4 = GPIO.PWM(M2_BACKWARD, mhz)

def backward(speed):
    if(speed > 100):
        speed = 100  
    
    print "BACKWARD speed: ", speed
    m2.start(0)
    m4.start(0)
    m1.start(speed)
    m3.start(speed - 7)
    
def forward(speed):
    if(speed > 100):
        speed = 100  
    print "FORWARD speed: ", speed
    m1.start(0)
    m3.start(0)
    m2.start(speed) 
    m4.start(speed - 7)

def stop(direction):    
    print('Motor is stoped!')
    if direction != IDLE:
        m1.start(0)
    	m3.start(0)
    	m2.start(0)
    	m4.start(0)
        
def finish():
	print('Finishing up!')
	GPIO.cleanup()
	quit()
