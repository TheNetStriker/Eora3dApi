#!/usr/bin/python3
 
import sys
import binascii
import struct
import time
from bluepy.btle import UUID, Peripheral

motorSteps = 6512 # 6512 seems to be a full 360 turn
motorSpeed = 255
motorAccel = 255

motorServiceUuid = UUID("TMOTOR SERVICE  ".encode("ascii").hex()) # Motor service
motorCposUuid    = UUID("MOTOR CPOS      ".encode("ascii").hex()) # Motor position notification
motorIposUuid    = UUID("MOTOR IPOS      ".encode("ascii").hex()) # Motor posision
motorMModeUuid   = UUID("MOTOR MMODE     ".encode("ascii").hex()) # No clue what this does
motorSModeUuid   = UUID("MOTOR SMODE     ".encode("ascii").hex()) # I guess this could be the microstepping of the motor
motorSpeedUuid   = UUID("MOTOR SPEED     ".encode("ascii").hex()) # Motor speed
motorAccelUuid   = UUID("MOTOR ACCEL     ".encode("ascii").hex()) # Motor acceleration

device = Peripheral("FA:63:A6:C0:79:FD", "random")

def decodeUuid(uuid):
    try:
        return bytes.fromhex(str(uuid).replace("-", "")).decode("ascii") 
    except:
        return ""

def listServices():
    print ("Services...")
    for svc in device.services:
        serviceName = decodeUuid(svc.uuid)
        print (str(svc.uuid) + ": '" + serviceName + "'")

        for ch in svc.getCharacteristics():
            channelName = decodeUuid(ch.uuid)
            print ("    " + str(ch.uuid) + ": '" + channelName + "'")

# To debug services
# listServices()

try:
    MotorService = device.getServiceByUUID(motorServiceUuid)

    motorIposCharacteristics = MotorService.getCharacteristics(motorIposUuid)[0]
    motorMModeCharacteristics = MotorService.getCharacteristics(motorMModeUuid)[0]
    motorSModeCharacteristics = MotorService.getCharacteristics(motorSModeUuid)[0]
    motorSpeedCharacteristics = MotorService.getCharacteristics(motorSpeedUuid)[0]
    motorAccelCharacteristics = MotorService.getCharacteristics(motorAccelUuid)[0]

    motorSpeedCharacteristics.write(motorSpeed.to_bytes(1, byteorder="little"))
    motorAccelCharacteristics.write(motorAccel.to_bytes(1, byteorder="little"))
    motorIposCharacteristics.write(motorSteps.to_bytes(4, byteorder="little"))
finally:
    device.disconnect()
