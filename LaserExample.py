#!/usr/bin/python3
 
import sys
import binascii
import struct
import time
from time import sleep
from bluepy.btle import UUID, Peripheral

startPosition = 0
endPosition = 12543
motorSpeed = 255

laserServiceUuid = UUID("SLASER SERVICE  ".encode("ascii").hex()) # Laser service
laserStatusUuid  = UUID("LASER STATUS    ".encode("ascii").hex()) # Laser status

motorServiceUuid = UUID("SMOTOR SERVICE  ".encode("ascii").hex()) # Motor service
motorCposUuid    = UUID("MOTOR CPOS      ".encode("ascii").hex()) # Motor position notification
motorIposUuid    = UUID("MOTOR IPOS      ".encode("ascii").hex()) # Motor posision
motorMModeUuid   = UUID("MOTOR MMODE     ".encode("ascii").hex()) # No clue what this does
motorSModeUuid   = UUID("MOTOR SMODE     ".encode("ascii").hex()) # I guess this could be the microstepping of the motor
motorSpeedUuid   = UUID("MOTOR SPEED     ".encode("ascii").hex()) # Motor speed

ledServiceUuid   = UUID("SLED SERVICE    ".encode("ascii").hex()) # Led service
ledTypeUuid      = UUID("LED TYPE        ".encode("ascii").hex()) # Led type

device = Peripheral("F2:33:8B:40:86:D0", "random")

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
    LaserService = device.getServiceByUUID(laserServiceUuid)
    MotorService = device.getServiceByUUID(motorServiceUuid)
    LedService = device.getServiceByUUID(ledServiceUuid)

    laserStatusCharacteristics = LaserService.getCharacteristics(laserStatusUuid)[0]

    motorIposCharacteristics = MotorService.getCharacteristics(motorIposUuid)[0]
    motorMModeCharacteristics = MotorService.getCharacteristics(motorMModeUuid)[0]
    motorSModeCharacteristics = MotorService.getCharacteristics(motorSModeUuid)[0]
    motorSpeedCharacteristics = MotorService.getCharacteristics(motorSpeedUuid)[0]

    print("Waiting until device has calibrated")
    sleep(30)

    print("Enable laser")
    laserStatusCharacteristics.write(b"\x01")

    print("Move to endposition")
    motorSpeedCharacteristics.write(motorSpeed.to_bytes(1, byteorder="little"))
    motorIposCharacteristics.write(endPosition.to_bytes(4, byteorder="little"))

    print("Wait for move to finish")
    sleep(10)

    print("Move back to start position")
    motorSpeedCharacteristics.write(motorSpeed.to_bytes(1, byteorder="little"))
    motorIposCharacteristics.write(startPosition.to_bytes(4, byteorder="little"))

    print("Wait for move to finish")
    sleep(10)

    print("Disable laser")
    laserStatusCharacteristics.write(b"\x00")
finally:
    device.disconnect()
