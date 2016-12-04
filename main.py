#!/usr/bin/python

import smbus
import math
import time
import sys, select, os
from MPU6050 import MPU6050
from PID import PID
import motor as MOTOR

gyro_scale = 131.0
accel_scale = 16384.0
RAD_TO_DEG = 57.29578
M_PI = 3.14159265358979323846

address = 0x68  # This is the address value read via the i2cdetect command
bus = smbus.SMBus(1)  # or bus = smbus.SMBus(1) for Revision 2 boards

now = time.time()

K = 0.98
K1 = 1 - K
KP = 100

FORWARD = 1
BACKWARD = -1
IDLE = 0
DIRECTION = IDLE

time_diff = 0.01

sensor = MPU6050(bus, address, "MPU6050")
sensor.read_raw_data()  # Reads current data from the sensor

rate_gyroX = 0.0
rate_gyroY = 0.0
rate_gyroZ = 0.0

gyroAngleX = 0.0 
gyroAngleY = 0.0 
gyroAngleZ = 0.0 

raw_accX = 0.0
raw_accY = 0.0
raw_accZ = 0.0

rate_accX = 0.0
rate_accY = 0.0
rate_accZ = 0.0

accAngX = 0.0

CFangleX = 0.0
CFangleX1 = 0.0
CFangleY1 = 0.0

K = 0.98

def dist(a, b):
    return math.sqrt((a * a) + (b * b))

def get_y_rotation(x,y,z):
    radians = math.atan2(x, dist(y,z))
    return -math.degrees(radians)

def get_x_rotation(x,y,z):
    radians = math.atan2(y, dist(x,z))
    return math.degrees(radians)

p = PID(0.9, 0.100,  -1.00)
p.setPoint(0.0)

while True:    
    print "Nobody can stop me. Except 'Enter' button:("
    if sys.stdin in select.select([sys.stdin], [], [], 0)[0]:
        line = raw_input()
        MOTOR.finish()
        break
    
    time.sleep(time_diff - 0.005) 
    sensor.read_raw_data()
    
    # Gyroscope value Degree Per Second / Scalled Data
    rate_gyroX = sensor.read_scaled_gyro_x()
    rate_gyroY = sensor.read_scaled_gyro_y()
    rate_gyroZ = sensor.read_scaled_gyro_z()
    
    # Accelerometer Raw Value
    raw_accX = sensor.read_raw_accel_x()
    raw_accY = sensor.read_raw_accel_y()
    raw_accZ = sensor.read_raw_accel_z()
    
    # Accelerometer value Degree Per Second / Scalled Data
    rate_accX = sensor.read_scaled_accel_x()
    rate_accY = sensor.read_scaled_accel_y()
    rate_accZ = sensor.read_scaled_accel_z()

    raw_gyroY = sensor.read_raw_gyro_y()
    
    # http://ozzmaker.com/2013/04/18/success-with-a-balancing-robot-using-a-raspberry-pi/    
    # http://blog.bitify.co.uk/2013/11/reading-data-from-mpu-6050-on-raspberry.html 

    accAngY = get_y_rotation(rate_accX, rate_accY, rate_accZ)
    CFangleY1 = ( K * ( CFangleY1 + rate_gyroY * time_diff) + K1 * accAngY )

    # Followed the Second example because it gives resonable pid reading
    pid = int(p.update(CFangleY1))
    speed = 30 + (abs(pid) * 3)

    if(pid > 0):
        DIRECTION = BACKWARD
        MOTOR.backward(abs(speed))
    elif(pid < 0):
        DIRECTION = FORWARD
        MOTOR.forward(abs(speed))
    else:
        MOTOR.stop(DIRECTION)
        DIRECTION = IDLE
