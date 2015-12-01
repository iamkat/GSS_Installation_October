#!/usr/bin/env python
 
from os import listdir
import subprocess, signal, psutil
from time import sleep
 
import RPi.GPIO as GPIO
 
GPIO.setmode(GPIO.BCM)
GPIO.setup(4, GPIO.IN)
GPIO.setup(23, GPIO.IN)

#keep track of whether the switch has just been activated (but not kept kept down)         
trigger = False
 
mp3_files = [ f for f in listdir('.') if f[-4:] == '.mp3' ]
 
if not (len(mp3_files) > 0):
    print "No mp3 files found!"
 
print '--- Available mp3 files ---'
print mp3_files
print '--- Press button #1 to select mp3, button #2 to play current. ---'
 
index = 0
while True:
    if (GPIO.input(23) == False):
        index += 1
        if index >= len(mp3_files):
            index = 0
#        print "--- " + mp3_files[index] + " ---"
 
    if (GPIO.input(4) == True):
#	print 'circuit closed'
	if trigger == False:
	#if there's an mp3 playing, kill it
		PROCNAME = "mpg123"
		for proc in psutil.process_iter():
    			if proc.name() == PROCNAME:
        			proc.kill()
		trigger = True 
		#play an mp3 from the list using mpg123
		subprocess.Popen(['mpg123', mp3_files[index]])
#        	print '--- Playing ' + mp3_files[index] + ' ---'
        sleep(1)
    if (GPIO.input(4) == False):
#	print 'circuit open'
	trigger = False
 
#    if (GPIO.input(25) == False):
#        subprocess.call(['killall', 'mpg123'])
#        print '--- Cleared all existing mp3s. ---'
 
    sleep(0.1);
