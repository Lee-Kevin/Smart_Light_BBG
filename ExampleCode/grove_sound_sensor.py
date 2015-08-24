#!/usr/bin/python
# -*- coding: utf-8 -*-

import time

import grove_i2c_adc
import Adafruit_BBIO.GPIO as GPIO

# Connect the Grove LED to GPIO P9_22
LED = "P9_22"            # GPIO P9_22
GPIO.setup(LED, GPIO.OUT)

# Reference voltage of ADC is 3.0v
ADC_REF = 3.0

# Vcc of the grove interface is normally 3.3v
GROVE_VCC = 3.3

# The threshold to turn the led on 0.2v
THRESHOLD_VOLTAGE = 0.15

adc = grove_i2c_adc.I2cAdc()

def read_sound_sensor_values():
    "Read voltage values from Grove Sound Sensor"
    total_value = 0
    for index in range(5):
        sensor_value = adc.read_adc()
#        print "sensor_value = ", sensor_value
        total_value += sensor_value
        time.sleep(0.01)
#    print "total_value = ", total_value
    average_value = float(total_value / 5)
    #voltage_value = average_value / 2047 * GROVE_VCC
    voltage_value = average_value / 4095 * ADC_REF * 2
    return voltage_value

# Function: If the sound sensor senses a sound that is up to the threshold you set in the code, the LED is on for 1s.
# Hardware: Grove - Sound Sensor, Grove - LED
if __name__== '__main__':

    while True:
        try:
            # Read sensor value from Grove Sound Sensor
            sensor_voltage_value = read_sound_sensor_values()
            
            # If loud, illuminate LED, otherwise dim
            if sensor_voltage_value > THRESHOLD_VOLTAGE:
                # Send HIGH to switch on LED
                GPIO.output(LED, GPIO.HIGH)
            else:
                # Send LOW to switch off LED
                GPIO.output(LED, GPIO.LOW)
            
            print "sensor_voltage_value = ", sensor_voltage_value
#            time.sleep(1)
            
        except KeyboardInterrupt:
            GPIO.output(LED, GPIO.LOW)
            break

        except IOError:
            print "Error"

