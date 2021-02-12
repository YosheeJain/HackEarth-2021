
#- cardstate.py

from future import print_function
from smartcard.scard import *
import smartcard.util
from time import *
from smartcard.Exceptions import CardConnectionException, NoCardException
from smartcard.System import *
from smartcard import util

srTreeATR = \
    [0x3B, 0x77, 0x94, 0x00, 0x00, 0x82, 0x30, 0x00, 0x13, 0x6C, 0x9F, 0x22]
srTreeMask = \
    [0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF]
CLA = 0x90
INS = 0xB8
P1 = 0x00
P2 = 0x00
LE = 0x07
# apdu chip info apdu
CHIP_INFO = [CLA, INS, P1, P2, LE]


def printstate(state):
    reader, eventstate, atr = state
    print(reader + " " + smartcard.util.toHexString(atr, smartcard.util.HEX))
    if eventstate & SCARD_STATE_ATRMATCH:
        print('\tCard found')
        return(1)
    if eventstate & SCARD_STATE_UNAWARE:
        print('\tState unware')
        return(2)
    if eventstate & SCARD_STATE_IGNORE:
        print('\tIgnore reader')
        return(3)
    if eventstate & SCARD_STATE_UNAVAILABLE:
        print('\tReader unavailable')
        return(4)
    if eventstate & SCARD_STATE_EMPTY:
        print('\tReader empty')
        return(5)
    if eventstate & SCARD_STATE_PRESENT:
        print('\tCard present in reader')
        return(6)
    if eventstate & SCARD_STATE_EXCLUSIVE:
        print('\tCard allocated for exclusive use by another application')
        return(7)
    if eventstate & SCARD_STATE_INUSE:
        print('\tCard in used by another application but can be shared')
        return(8)
    if eventstate & SCARD_STATE_MUTE:
        print('\tCard is mute')
        return(9)
    if eventstate & SCARD_STATE_CHANGED:
        print('\tState changed')
        return(10)
    if eventstate & SCARD_STATE_UNKNOWN:
        print('\tState unknowned')
        return(11)


def get_reader_context():
    hresult, hcontext = SCardEstablishContext(SCARD_SCOPE_USER)
    if hresult != SCARD_S_SUCCESS:
        print('Failed to establish context: ' +
              SCardGetErrorMessage(hresult))
        return (0, 0)
    print('Context established!')

    return (1, hcontext)


def get_readers(hcontext):
    hresult, readers = SCardListReaders(hcontext, [])
    if hresult != SCARD_S_SUCCESS:
        print('Failed to list readers: ' +
              SCardGetErrorMessage(hresult))
        return (0, 0)
    print('PCSC Readers:', readers)
    return (1, readers)


def get_card_state(hcontext, readers):
    readerstates = []
    for i in range(len(readers)):
        readerstates += [(readers[i], SCARD_STATE_UNAWARE)]
    hresult, newstates = SCardGetStatusChange(hcontext, 0, readerstates)
    for i in newstates:
        ret = printstate(i)
    return (ret, newstates)


def wait_card_state_change(hcontext, readers, newstates):
    print('----- Please insert or remove a card ------------')
    hresult, newstates = SCardGetStatusChange(
        hcontext,
        INFINITE,
        newstates)

    print('----- New reader and card states are: -----------')
    for i in newstates:
        ret = printstate(i)
        return(ret, newstates)


def release_context(hcontext):
    hresult = SCardReleaseContext(hcontext)
    if hresult != SCARD_S_SUCCESS:
        print(
            'Failed to release context: ' +
            SCardGetErrorMessage(hresult))
        return(0)
    print('Released context.')
    return(1)


def read_fp_from_card():
    sc_readers = readers()
    print(sc_readers)
    # create a connection to the first reader
    first_reader = sc_readers[0]
    connection = first_reader.createConnection()

    # get ready for a command
    get_uid = util.toBytes("FF 20 00 00 02 FF FF")

    try:
        # send the command and capture the response data and status
        connection.connect()
        data, sw1, sw2 = connection.transmit(get_uid)

        # print the response
        uid = util.toHexString(data)
        status = util.toHexString([sw1, sw2])
        print("UID = {}\tstatus = {}".format(uid, status))

        read_payload = []

        for i in range(0, 512, 64):

read_command = [0xFF, 0xB0, i/64, 0x00, 0x40]
            #get_uid = util.toBytes("FF B0 00 00 40")
            data, sw1, sw2 = connection.transmit(read_command)
            read_payload = read_payload + data
            print("UID = {}\tstatus = {}".format(
                util.toHexString(data), util.toHexString([sw1, sw2])))
        print(read_payload)
        return read_payload
    except NoCardException:
        print("ERROR: Card not present")
        raise Exception("ERROR: Card not present")


def erase_card(connection):
    try:
        write_command = [0xFF, 0x0E, 0x80, 0x00]
        payload = write_command
        print(payload)
        data, sw1, sw2 = connection.transmit(payload)
        uid = util.toHexString(data)
        status = util.toHexString([sw1, sw2])
        print("UID = {}\tstatus = {}".format(uid, status))

        write_command = [0xFF, 0x0E, 0x81, 0x00]
        payload = write_command
        print(payload)
        data, sw1, sw2 = connection.transmit(payload)
        uid = util.toHexString(data)
        status = util.toHexString([sw1, sw2])
        print("UID = {}\tstatus = {}".format(uid, status))

        write_command = [0xFF, 0x0E, 0x82, 0x00]
        payload = write_command
        print(payload)
        data, sw1, sw2 = connection.transmit(payload)
        uid = util.toHexString(data)
        status = util.toHexString([sw1, sw2])
        print("UID = {}\tstatus = {}".format(uid, status))

        write_command = [0xFF, 0x0E, 0x83, 0x00]
        payload = write_command
        print(payload)
        data, sw1, sw2 = connection.transmit(payload)
        uid = util.toHexString(data)
        status = util.toHexString([sw1, sw2])
        print("UID = {}\tstatus = {}".format(uid, status))

        write_command = [0xFF, 0x0E, 0x84, 0x00]
        payload = write_command
        print(payload)
        data, sw1, sw2 = connection.transmit(payload)
        uid = util.toHexString(data)
        status = util.toHexString([sw1, sw2])
        print("UID = {}\tstatus = {}".format(uid, status))

        write_command = [0xFF, 0x0E, 0x85, 0x00]
        payload = write_command
        data, sw1, sw2 = connection.transmit(payload)
        uid = util.toHexString(data)
        status = util.toHexString([sw1, sw2])
        print("UID = {}\tstatus = {}".format(uid, status))

        write_command = [0xFF, 0x0E, 0x86, 0x00]
        payload = write_command
        print(payload)
        data, sw1, sw2 = connection.transmit(payload)
        uid = util.toHexString(data)
        status = util.toHexString([sw1, sw2])
        print("UID = {}\tstatus = {}".format(uid, status))

        write_command = [0xFF, 0x0E, 0x87, 0x00]
        payload = write_command
        print(payload)
        data, sw1, sw2 = connection.transmit(payload)
        uid = util.toHexString(data)
        status = util.toHexString([sw1, sw2])
        print("UID = {}\tstatus = {}".format(uid, status))
    except NoCardException:
        print("ERROR: Card not present")


def write_card(connection, characterics):
    try:
        write_command = [0xFF, 0xD0, 0x80, 0x00, 0x40]
        payload = write_command + characterics[0:64]
        print(payload)
        data, sw1, sw2 = connection.transmit(payload)
        uid = util.toHexString(data)
        status = util.toHexString([sw1, sw2])
        print("UID = {}\tstatus = {}".format(uid, status))

        write_command = [0xFF, 0xD0, 0x81, 0x00, 0x40]
        payload = write_command + characterics[64:128]
        print(payload)
        data, sw1, sw2 = connection.transmit(payload)
        uid = util.toHexString(data)
        status = util.toHexString([sw1, sw2])
        print("UID = {}\tstatus = {}".format(uid, status))

        write_command = [0xFF, 0xD0, 0x82, 0x00, 0x40]
        payload = write_command + characterics[128:192]
        print(payload)
        data, sw1, sw2 = connection.transmit(payload)
        uid = util.toHexString(data)
        status = util.toHexString([sw1, sw2])
        print("UID = {}\tstatus = {}".format(uid, status))

write_command = [0xFF, 0xD0, 0x83, 0x00, 0x40]
        payload = write_command + characterics[192:256]
        print(payload)
        data, sw1, sw2 = connection.transmit(payload)
        uid = util.toHexString(data)
        status = util.toHexString([sw1, sw2])
        print("UID = {}\tstatus = {}".format(uid, status))

        write_command = [0xFF, 0xD0, 0x84, 0x00, 0x40]
        payload = write_command + characterics[256:320]
        print(payload)
        data, sw1, sw2 = connection.transmit(payload)
        uid = util.toHexString(data)
        status = util.toHexString([sw1, sw2])
        print("UID = {}\tstatus = {}".format(uid, status))

        write_command = [0xFF, 0xD0, 0x85, 0x00, 0x40]
        payload = write_command + characterics[320:384]
        print(payload)
        data, sw1, sw2 = connection.transmit(payload)
        uid = util.toHexString(data)
        status = util.toHexString([sw1, sw2])
        print("UID = {}\tstatus = {}".format(uid, status))

        write_command = [0xFF, 0xD0, 0x86, 0x00, 0x40]
        payload = write_command + characterics[384:448]
        print(payload)
        data, sw1, sw2 = connection.transmit(payload)
        uid = util.toHexString(data)
        status = util.toHexString([sw1, sw2])
        print("UID = {}\tstatus = {}".format(uid, status))

        write_command = [0xFF, 0xD0, 0x87, 0x00, 0x40]
        payload = write_command + characterics[448:512]
        print(payload)
        data, sw1, sw2 = connection.transmit(payload)
        uid = util.toHexString(data)
        status = util.toHexString([sw1, sw2])
        print("UID = {}\tstatus = {}".format(uid, status))

        read_payload = []

        read_command = [0xFF, 0xB0, 0x80, 0x00, 0x40]
        data, sw1, sw2 = connection.transmit(read_command)
        read_payload = read_payload + data

        read_command = [0xFF, 0xB0, 0x81, 0x00, 0x40]
        data, sw1, sw2 = connection.transmit(read_command)
        read_payload = read_payload + data

        read_command = [0xFF, 0xB0, 0x82, 0x00, 0x40]
        data, sw1, sw2 = connection.transmit(read_command)
        read_payload = read_payload + data

        read_command = [0xFF, 0xB0, 0x83, 0x00, 0x40]
        data, sw1, sw2 = connection.transmit(read_command)
        read_payload = read_payload + data

        read_command = [0xFF, 0xB0, 0x84, 0x00, 0x40]
        data, sw1, sw2 = connection.transmit(read_command)
        read_payload = read_payload + data

        read_command = [0xFF, 0xB0, 0x85, 0x00, 0x40]
        data, sw1, sw2 = connection.transmit(read_command)
        read_payload = read_payload + data

        read_command = [0xFF, 0xB0, 0x86, 0x00, 0x40]
        data, sw1, sw2 = connection.transmit(read_command)
        read_payload = read_payload + data

        read_command = [0xFF, 0xB0, 0x87, 0x00, 0x40]
        data, sw1, sw2 = connection.transmit(read_command)
        read_payload = read_payload + data

        # print the response
        print(read_payload)

    except NoCardException:
        print("ERROR: Card not present")


def write_fp_to_card(write_payload):
    sc_readers = readers()
    print(sc_readers)
    # create a connection to the first reader
    first_reader = sc_readers[0]
    connection = first_reader.createConnection()

    # get ready for a command
    get_uid = util.toBytes("FF 20 00 00 02 FF FF")

    try:
        # send the command and capture the response data and status
        connection.connect()
        data, sw1, sw2 = connection.transmit(get_uid)

        # print the response
        uid = util.toHexString(data)
        status = util.toHexString([sw1, sw2])
        print("UID = {}\tstatus = {}".format(uid, status))
        erase_card(connection)
        write_card(connection, write_payload)
    except Exception as e:
        print(e)
        print("Operation Failed")


class MustBeEvenException(Exception):
    pass

#- fp_delete.py

#!/usr/bin/env python
# -- coding: utf-8 --

"""
PyFingerprint
Copyright (C) 2015 Bastian Raschke <bastian.raschke@posteo.de>
All rights reserved.

"""

from pyfingerprint.pyfingerprint import PyFingerprint


## Deletes a finger from sensor
##


## Tries to initialize the sensor
try:
    f = PyFingerprint('/dev/ttyUSB0', 57600, 0xFFFFFFFF, 0x00000000)

    if ( f.verifyPassword() == False ):
        raise ValueError('The given fingerprint sensor password is wrong!')

except Exception as e:
    print('The fingerprint sensor could not be initialized!')
    print('Exception message: ' + str(e))
    exit(1)

## Gets some sensor information
print('Currently used templates: ' + str(f.getTemplateCount()) +'/'+ str(f.getStorageCapacity()))

## Tries to delete the template of the finger
try:
    positionNumber = input('Please enter the template position you want to delete: ')
    positionNumber = int(positionNumber)

    if ( f.deleteTemplate(positionNumber) == True ):
        print('Template deleted!')

except Exception as e:
    print('Operation failed!')
    print('Exception message: ' + str(e))
    exit(1)

#- gsm.py

import serial
import RPi.GPIO as GPIO      
import os, time

def sendsms():
    GPIO.setmode(GPIO.BCM)    
    # Enable Serial Communication
    port = serial.Serial("/dev/ttyAMA0", baudrate=115200, timeout=1)
    port.write('AT+CMGF=1'+'\r\n')  # Select Message format as Text mode 
    time.sleep(1)
    port.write('AT+CMGS="+918527732908"'+'\r\n')
    time.sleep(1)
    port.write('ALERT: THEFT THREAT FOR CAR HR26 CP 1234'+'\r\n')  # Message
    port.write("\x1A") # Enable to send SMS

#- i2c_lib.py

import smbus
from time import *

class i2c_device:
   def init(self, addr, port=1):
      self.addr = addr
      self.bus = smbus.SMBus(port)

# Write a single command
   def write_cmd(self, cmd):
      self.bus.write_byte(self.addr, cmd)
      sleep(0.0001)

# Write a command and argument
   def write_cmd_arg(self, cmd, data):
      self.bus.write_byte_data(self.addr, cmd, data)
      sleep(0.0001)

# Write a block of data
   def write_block_data(self, cmd, data):
      self.bus.write_block_data(self.addr, cmd, data)
      sleep(0.0001)

# Read a single byte
   def read(self):
      return self.bus.read_byte(self.addr)

# Read
   def read_data(self, cmd):
      return self.bus.read_byte_data(self.addr, cmd)

# Read a block of data
   def read_block_data(self, cmd):
      return self.bus.read_block_data(self.addr, cmd)

#- lcddriver.py

import sys
sys.path.append("./lib")

import i2c_lib
from time import *

# LCD Address
ADDRESS = 0x27

# commands
LCD_CLEARDISPLAY = 0x01
LCD_RETURNHOME = 0x02
LCD_ENTRYMODESET = 0x04
LCD_DISPLAYCONTROL = 0x08
LCD_CURSORSHIFT = 0x10
LCD_FUNCTIONSET = 0x20
LCD_SETCGRAMADDR = 0x40
LCD_SETDDRAMADDR = 0x80

# flags for display entry mode
LCD_ENTRYRIGHT = 0x00
LCD_ENTRYLEFT = 0x02
LCD_ENTRYSHIFTINCREMENT = 0x01
LCD_ENTRYSHIFTDECREMENT = 0x00

# flags for display on/off control
LCD_DISPLAYON = 0x04
LCD_DISPLAYOFF = 0x00
LCD_CURSORON = 0x02
LCD_CURSOROFF = 0x00
LCD_BLINKON = 0x01
LCD_BLINKOFF = 0x00

# flags for display/cursor shift
LCD_DISPLAYMOVE = 0x08
LCD_CURSORMOVE = 0x00
LCD_MOVERIGHT = 0x04
LCD_MOVELEFT = 0x00

# flags for function set
LCD_8BITMODE = 0x10
LCD_4BITMODE = 0x00
LCD_2LINE = 0x08
LCD_1LINE = 0x00
LCD_5x10DOTS = 0x04
LCD_5x8DOTS = 0x00

# flags for backlight control
LCD_BACKLIGHT = 0x08
LCD_NOBACKLIGHT = 0x00

En = 0b00000100 # Enable bit
Rw = 0b00000010 # Read/Write bit
Rs = 0b00000001 # Register select bit

class lcd:
   #initializes objects and lcd
   def init(self):
      self.lcd_device = i2c_lib.i2c_device(ADDRESS)

      self.lcd_write(0x03)
      self.lcd_write(0x03)
      self.lcd_write(0x03)
      self.lcd_write(0x02)

      self.lcd_write(LCD_FUNCTIONSET | LCD_2LINE | LCD_5x8DOTS | LCD_4BITMODE)
      self.lcd_write(LCD_DISPLAYCONTROL | LCD_DISPLAYON)
      self.lcd_write(LCD_CLEARDISPLAY)
      self.lcd_write(LCD_ENTRYMODESET | LCD_ENTRYLEFT)
      sleep(0.2)

   # clocks EN to latch command
   def lcd_strobe(self, data):
      self.lcd_device.write_cmd(data | En | LCD_BACKLIGHT)
      sleep(.0005)
      self.lcd_device.write_cmd(((data & ~En) | LCD_BACKLIGHT))
      sleep(.0001)

   def lcd_write_four_bits(self, data):
      self.lcd_device.write_cmd(data | LCD_BACKLIGHT)
      self.lcd_strobe(data)

   # write a command to lcd
   def lcd_write(self, cmd, mode=0):
      self.lcd_write_four_bits(mode | (cmd & 0xF0))
      self.lcd_write_four_bits(mode | ((cmd << 4) & 0xF0))
      
   #turn on/off the lcd backlight
   def lcd_backlight(self, state):
      if state in ("on","On","ON"):
         self.lcd_device.write_cmd(LCD_BACKLIGHT)
      elif state in ("off","Off","OFF"):
         self.lcd_device.write_cmd(LCD_NOBACKLIGHT)
      else:
         print("Unknown State!")

   # put string function
   def lcd_display_string(self, string, line):
      if line == 1:
         self.lcd_write(0x80)
      if line == 2:
         self.lcd_write(0xC0)
      if line == 3:
         self.lcd_write(0x94)
      if line == 4:
         self.lcd_write(0xD4)

      for char in string:
         self.lcd_write(ord(char), Rs)

   # clear lcd and set to home
   def lcd_clear(self):
      self.lcd_write(LCD_CLEARDISPLAY)
      self.lcd_write(LCD_RETURNHOME)

#- motor.py

from time import sleep
import RPi.GPIO as GPIO
import os
import random

IN1=6 # IN1
IN2=13 # IN2
IN3=19 # IN3
IN4=26 # IN4
time = 0.001

def init():

    GPIO.setmode(GPIO.BCM) 
    GPIO.setup(IN1,GPIO.OUT)
    GPIO.setup(IN2,GPIO.OUT)
    GPIO.setup(IN3,GPIO.OUT)
    GPIO.setup(IN4,GPIO.OUT)
    GPIO.output(IN1, False)
    GPIO.output(IN2, False)
    GPIO.output(IN3, False)
    GPIO.output(IN4, False)
    
def cleanup():
    GPIO.cleanup()

def Step1():
    GPIO.output(IN4, True)
    sleep (time)
    GPIO.output(IN4, False)

def Step2():
    GPIO.output(IN4, True)
    GPIO.output(IN3, True)
    sleep (time)
    GPIO.output(IN4, False)
    GPIO.output(IN3, False)

def Step3():
    GPIO.output(IN3, True)
    sleep (time)
    GPIO.output(IN3, False)

def Step4():
    GPIO.output(IN2, True)
    GPIO.output(IN3, True)
    sleep (time)
    GPIO.output(IN2, False)
    GPIO.output(IN3, False)

def Step5():
    GPIO.output(IN2, True)
    sleep (time)
    GPIO.output(IN2, False)

def Step6():
    GPIO.output(IN1, True)
    GPIO.output(IN2, True)
    sleep (time)
    GPIO.output(IN1, False)
    GPIO.output(IN2, False)

def Step7():
    GPIO.output(IN1, True)
    sleep (time)
    GPIO.output(IN1, False)

def Step8():
    GPIO.output(IN4, True)
    GPIO.output(IN1, True)
    sleep (time)
    GPIO.output(IN4, False)
    GPIO.output(IN1, False)

def left(step): 
    for i in range (step):   
        Step1()
        Step2()
        Step3()
        Step4()
        Step5()
        Step6()
        Step7()
        Step8()  
        print ("Step left: ",i)

def right(step):
    for i in range (step):
        Step8()
        Step7()
        Step6()
        Step5()
        Step4()
        Step3()
        Step2()
        Step1()  
        print ("Step right: ",i)

#- ssc3.py

import lcddriver
import motor
import hashlib
import gsm
from pyfingerprint.pyfingerprint import PyFingerprint
from smartcard.Exceptions import CardConnectionException, NoCardException
from smartcard.System import *
from smartcard import util
from cardstate import *
from time import *
import RPi.GPIO as GPIO

COUNTER_FOR_SMS = 3

def init():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(17, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) #Black
    GPIO.setup(27, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) #Red
    lcd = lcddriver.lcd()
    return(lcd)
    
def welcome_msg(lcd):
    lcd.lcd_clear()
    lcd.lcd_display_string("Welcome to Demo", 1)
    
def warning_msg(lcd, e):
    lcd.lcd_clear()
    lcd.lcd_display_string("Welcome to Demo", 1)
    lcd.lcd_display_string(str(e), 2)
    lcd.lcd_display_string("Wait: Retrying", 3)
    
def error_msg(lcd, e):
    print('Operation failed!')
    print(str)
    lcd.lcd_clear()
    lcd.lcd_display_string("Welcome to Demo", 1)
    lcd.lcd_display_string(str(e), 2)
    lcd.lcd_display_string("Error:Reset System", 3)
    
def init_smart_card_reader(lcd):
    try:
        ret, context = get_reader_context()
        ret, readers = get_readers(context)
        while (ret == 0):
            welcome_msg(lcd)
            lcd.lcd_display_string("CardReader NotFound", 2)
            sleep(1)
            ret, readers = get_readers(context)
            if (ret == 1):
                lcd.lcd_clear()
                lcd.lcd_display_string("Welcome to Demo", 1)
                lcd.lcd_display_string("CardReader Found", 2)
                break;
        return(context, readers)
    except Exception as e:
        error_msg(lcd, e)
    exit(1)
    
def init_smart_card(lcd, context, readers):
    try:
        ret, state = get_card_state(context, readers)
        while True:
            if(ret == 5):
                welcome_msg(lcd)
                lcd.lcd_display_string("CardReader Found", 2)
                lcd.lcd_display_string("Insert your DL", 3)
                ret, state = wait_card_state_change(context, readers, state)
            elif(ret == 6):
                welcome_msg(lcd)
                lcd.lcd_display_string("CardReader Found", 2)
                lcd.lcd_display_string("DL Found", 3)
                sleep(3)
                break
        return(state)
    except Exception as e:
        error_msg(lcd, e)
        pass
def wait_new_smart_card(lcd, context, readers, state):
    try:
        ret, state = wait_card_state_change(context, readers, state)
        while True:
            if(ret == 5):
                welcome_msg(lcd)
                lcd.lcd_display_string("CardReader Found", 2)
                lcd.lcd_display_string("Insert your DL", 3)
                ret, state = wait_card_state_change(context, readers, state)
            elif(ret == 6):
                welcome_msg(lcd)
                lcd.lcd_display_string("CardReader Found", 2)
                lcd.lcd_display_string("DL Found", 3)
                sleep(2)
                break
        return(state)
    except Exception as e:
        error_msg(lcd, e)
        pass

def init_fp(lcd):
    while True:
        try:
            f = PyFingerprint('/dev/ttyUSB0', 57600, 0xFFFFFFFF, 0x00000000)
            if ( f.verifyPassword() == False ):
                print('Currently used templates: ' + str(f.getTemplateCount()) +'/'+ str(f.getStorageCapacity()))
                raise Exception('FP password wrong!')
                break
            else:
                break
        except Exception as e:
            print("Some issue with FP sendor, trying again")
            warning_msg(lcd, e)
            pass
    return(f)

def read_fp_sensor(lcd, f):
    while ( f.readImage() == False ):
        pass
    f.convertImage(0x01)
    ## Searchs template
    result = f.searchTemplate()

positionNumber = result[0]
    accuracyScore = result[1]
    return(positionNumber, accuracyScore)
        
def verify_fp_from_sensor(lcd, f):
    counter = 0
    while True:
        positionNumber, accuracyScore = read_fp_sensor(lcd, f)
        if ( positionNumber == -1 ):
                counter = counter + 1
                print('fp fail count is:' + str(counter))
                welcome_msg(lcd)
                lcd.lcd_display_string("Pls dont remove DL", 2)
                lcd.lcd_display_string('No match ' + str(counter), 3)
                lcd.lcd_display_string('Try again',4)
                sleep(3)
                global COUNTER_FOR_SMS
                if (counter > COUNTER_FOR_SMS):
                    print("sending sms")
                    gsm.sendsms()
                    counter = 0
                #for i in range(1,5):
                 #   sleep (1)
                  #  welcome_msg(lcd)
                   # lcd.lcd_display_string("Pls dont remove DL", 2)
                    #lcd.lcd_display_string('No match ' + str(counter), 3)
                    #lcd.lcd_display_string('Try after 5 secs' + str(i+1), 4)
        else:
            break
    return(positionNumber, accuracyScore)

def read_verify_dl(lcd, f, positionNumber):
    while True:
        try:
            fp_card = read_fp_from_card()
        except Exception as e:
            lcd.lcd_clear()
            lcd.lcd_display_string("Welcome to Demo", 1)
            lcd.lcd_display_string("FP Matched-1", 2)
            lcd.lcd_display_string('DL Not found', 3)
            lcd.lcd_display_string('Pls insert DL', 4)
            pass            
                #f.uploadCharacteristics(0x01, fp_card)
        f.loadTemplate(positionNumber, 0x01)
        characterics = f.downloadCharacteristics(0x01)
        print(positionNumber)
        print(characterics)
        print('--------')
        print(fp_card)
        f.uploadCharacteristics(0x02, fp_card)
        result = f.compareCharacteristics()
        break
    return(result)

def drive(lcd):
    try:
        context, readers = init_smart_card_reader(lcd)
        state = init_smart_card(lcd, context, readers)
        f = init_fp(lcd)
        welcome_msg(lcd)
        lcd.lcd_display_string("Pls dont remove DL", 2)
        lcd.lcd_display_string('Place your finger..', 3)
        positionNumber, accuracyScore = verify_fp_from_sensor(lcd, f)
        welcome_msg(lcd)
        lcd.lcd_display_string("Pls dont remove DL", 2)
        lcd.lcd_display_string('FingerPrint Matched-1', 3)
        lcd.lcd_display_string('Verifying DL', 4)
        sleep(3)
        result = read_verify_dl(lcd, f, positionNumber)
        if ( result == 0 ):
            welcome_msg(lcd)
            lcd.lcd_display_string("FP Matched-1", 2)
            lcd.lcd_display_string('DL check Fail', 3)
            lcd.lcd_display_string('Pls insert valid DL', 4)
            print("No match for DL")
            state = wait_new_smart_card(lcd, context, readers, state)
            #sleep(5)
            execfile("ssc3.py")
        else:
            print('Found template at position #' + str(positionNumber))
            print('The accuracy score is: ' + str(accuracyScore))
            welcome_msg(lcd)
            lcd.lcd_display_string("Wishing Safe Driving", 2)
            motor.init()
            motor.right(250)
            motor.cleanup()
            exit(1)
    except Exception as e:
            print(e)
            GPIO.cleanup()
            error_msg(lcd, e)
def enroll_car(lcd):
    try:
        counter = 0
        f = init_fp(lcd)
        while True:
            welcome_msg(lcd)
            lcd.lcd_display_string("Owner verification", 2)
            lcd.lcd_display_string("Place Finger", 3)
            positionNumber, accuracyScore = read_fp_sensor(lcd, f)
            if(positionNumber == -1):
                counter = counter + 1
                lcd.lcd_display_string("Verification fail", 4)
                sleep(4)
                global COUNTER_FOR_SMS
                if(counter > COUNTER_FOR_SMS):
                    gsm.sendsms();

return
            else:
                break
        welcome_msg(lcd)
        lcd.lcd_display_string("Owner verification", 2)
        lcd.lcd_display_string("Verify Success", 3)
        sleep(4)
        while True:
            welcome_msg(lcd)
            lcd.lcd_display_string("Place FP to enroll", 2)
            positionNumber, accuracyScore = read_fp_sensor(lcd, f)
            if ( positionNumber >= 0 ):
                print('Template already exists at position #' + str(positionNumber))
                welcome_msg(lcd)
                lcd.lcd_display_string("Already Enrolled ", 2)
                sleep(3)
                welcome_msg(lcd)
                lcd.lcd_display_string("Enroll DL:Push Black", 2)
                lcd.lcd_display_string("Main Menu: Push Red", 3)
                sleep(5)
                while True:    
                    button_state_dl_enroll = GPIO.input(17) #car
                    button_state_menu = GPIO.input(27) #dl
                    if button_state_dl_enroll == GPIO.HIGH:
                        enroll_dl(lcd, f, positionNumber)
                        break
                    elif button_state_menu == GPIO.HIGH:
                        break
                break
            else:
                welcome_msg(lcd)
                lcd.lcd_display_string("Remove Finger", 2)
                sleep(4)
                welcome_msg(lcd)
                lcd.lcd_display_string("Waiting same finger", 2)
                print('Waiting for same finger again...')
                ## Wait that finger is read again
                while ( f.readImage() == False ):
                    pass
                ## Converts read image to characteristics and stores it in charbuffer 2
                f.convertImage(0x02)
                sleep(1)
                ## Compares the charbuffers
                if ( f.compareCharacteristics() == 0 ):
                    lcd.lcd_display_string("Mismatch", 3)
                    lcd.lcd_display_string("Try Again", 4)
                    sleep(4)
                else:
                    ## Creates a template
                    f.createTemplate()
                    ## Saves template at new position number
                    positionNumber = f.storeTemplate()
                    print('Finger enrolled successfully!')
                    lcd.lcd_display_string("Enrolled", 3)
                    print('New template position #' + str(positionNumber))
                    sleep(5)
                    welcome_msg(lcd)
                    lcd.lcd_display_string("Enroll DL:Push Black", 2)
                    lcd.lcd_display_string("Main Menu: Push Red", 3)
                    while True:    
                        button_state_dl_enroll = GPIO.input(17) #car
                        button_state_menu = GPIO.input(27) #dl
                        if button_state_dl_enroll == GPIO.HIGH:
                            enroll_dl(lcd, f, positionNumber)
                            break
                        elif button_state_menu == GPIO.HIGH:
                            break
                    break
    except Exception as e:
        print('Operation failed!')
        print('Exception message: ' + str(e))
        pass
    
def enroll_dl(lcd, f, positionNumber):
    try:
        welcome_msg(lcd)
        lcd.lcd_display_string("Wait, Enrolling", 2)
        f.loadTemplate(positionNumber, 0x01)
        #characterics = str(f.downloadCharacteristics(0x01)).encode('utf-8')
        characterics = f.downloadCharacteristics(0x01)
        print(characterics)
        write_fp_to_card(characterics)
        welcome_msg(lcd)
        lcd.lcd_display_string("Enrolled", 2)
        sleep(3)
    except Exception as e:
        print('Operation failed!')
        print('Exception message: ' + str(e))
        pass

def main():
    try:
        lcd = init()
        while True:
            welcome_msg(lcd)
            lcd.lcd_display_string("Enroll: Push Black", 2)
            lcd.lcd_display_string("Drive: Push Red", 3)
            while True:
                button_state_enroll = GPIO.input(17)
                button_state_drive = GPIO.input(27)
                if button_state_drive == GPIO.HIGH:
                    drive(lcd)
                    break
                elif button_state_enroll == GPIO.HIGH:
                    enroll_car(lcd)
                    sleep(1)
                    break
                    
    except Exception as e:
            print(e)
            GPIO.cleanup()
            error_msg(lcd, e)
    
if name== "main":
  main()