from multiprocessing import shared_memory
import time
import sys
import array
import RPi.GPIO as GPIO

powerLedsPin = 23
drive8ActivityPin = 27
drive9ActivityPin = 22

DRIVE_8_ACTIVITY_INDEX = 1
DRIVE_9_ACTIVITY_INDEX = 3

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup([powerLedsPin,drive8ActivityPin,drive9ActivityPin],
        GPIO.OUT, initial=GPIO.HIGH)

print ("GPIO Pins initialized.")

def initializeLEDLighting():
    print ("Initializing LEDs. (NO-OP)")
def updateLEDLighting(driveDataString):
#    print ("Update LEDS based on String: "+driveDataString)
    if (driveDataString[DRIVE_8_ACTIVITY_INDEX] == '1'):
        GPIO.output(drive8ActivityPin,GPIO.HIGH)
    else:
        GPIO.output(drive8ActivityPin,GPIO.LOW)
    if (driveDataString[DRIVE_9_ACTIVITY_INDEX] == '1'):
        GPIO.output(drive9ActivityPin,GPIO.HIGH)
    else:
        GPIO.output(drive9ActivityPin,GPIO.LOW)
def uninitializeLEDLighting():
    print ("Power Down LEDs.")

try:
    print ("Consumix Python version starting up.")

    while (True):
        try:
            shm_vice = shared_memory.SharedMemory(name="vice-drive-led-shm", create=False, size=16)
            break;
        except Exception as e:
            print (e)
            print ("Error Trying to Open Shared Memory... Trying again in a bit.")
            time.sleep(.5)
            continue

    print ("Shared memory found, let's read it.")
    
    initializeLEDLighting()

    while (True):
        driveData = array.array('b',shm_vice.buf[:8])
        driveDataString = driveData.tostring().decode("utf-8")
        updateLEDLighting(driveDataString)
        time.sleep(0.025)

except KeyboardInterrupt:
  print ("I'm outta here, close my resources")
  shm_vice.close()
  uninitializeLEDLighting()
  sys.exit()

