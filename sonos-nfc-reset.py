#!/usr/bin/env python
# -*- coding: utf8 -*-
#
#    Copyright 2014,2018 Gerd Saurer <gerd.saurer@gmail.com>
#
#    You should have received a copy of the GNU Lesser General Public License
#    along with sonos-nfc-read.  If not, see <http://www.gnu.org/licenses/>.
#

import RPi.GPIO as GPIO
import MFRC522
import signal
import time
import textwrap
import sys
import NFCHelper
import argparse

continue_reading = True
is_Test = False

# Capture SIGINT for cleanup when the script is aborted
def end_read(signal,frame):
    global continue_reading
    print("Ctrl+C captured, ending read.")
    continue_reading = False
    GPIO.cleanup()
# Hook the SIGINT
signal.signal(signal.SIGINT, end_read)

parser = argparse.ArgumentParser(description='Write NFC tags for sonos.')
parser.add_argument('-test', type=bool, default=False, help='Just test the reset, but dont perform the action on the card')
#parser.add_argument('-nfcKey', type=str, default='FF:FF:FF:FF:FF:FF', help='The hex code of the nfc key to writ the content default: FF:FF:FF:FF:FF:FF')
args = parser.parse_args()

is_test = args.test

# Create an object of the class MFRC522
MIFAREReader = MFRC522.MFRC522()

print("Add NFC Tag ...")

# Program start
# This loop keeps checking for chips. If one is near it will get the UID and authenticate
while continue_reading:

    # Scan for cards    
    (status,TagType) = MIFAREReader.MFRC522_Request(MIFAREReader.PICC_REQIDL)

    # If a card is found
    if status == MIFAREReader.MI_OK:
        print("Card detected")
    
    # Get the UID of the card
    (status,uid) = MIFAREReader.MFRC522_Anticoll()

    # If we have the UID, continue
    if status == MIFAREReader.MI_OK:

        # Print UID
        print("Card UID: %s:%s:%s:%s" % (uid[0], uid[1], uid[2], uid[3]))
        
        # Select the scanned tag
        MIFAREReader.MFRC522_SelectTag(uid)

        # Write the data
        sectorCount = 1
        print("cleaning Sector [%s-%s] need to be written with data." % (sectorCount, 64))
 
        while sectorCount < 64:
            if(sectorCount != 0 and sectorCount % 4 != 3 ):
                if(not is_test):
                    NFCHelper.clear_Sector(MIFAREReader, uid, NFCHelper.AUTH_KEY_DEFAULT, sectorCount)
                NFCHelper.read_Sector(MIFAREReader, uid, NFCHelper.AUTH_KEY_DEFAULT, sectorCount) 
            sectorCount = sectorCount + 1 
        
        if(not is_test):
            NFCHelper.clear_Metadata(MIFAREReader, uid, NFCHelper.AUTH_KEY_DEFAULT)
        nfcDataSize = NFCHelper.read_Metadata(MIFAREReader, uid, NFCHelper.AUTH_KEY_DEFAULT)
        
        # Stop
        MIFAREReader.MFRC522_StopCrypto1()
        print("Card UID: %s:%s:%s:%s reset." % (uid[0], uid[1], uid[2], uid[3]))
        time.sleep(3)
