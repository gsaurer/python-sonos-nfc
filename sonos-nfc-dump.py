#!/usr/bin/env python
# -*- coding: utf8 -*-
#
#    Copyright 2014,2018 Gerd Saurer <gerd.saurer@gmail.com>
#
#    You should have received a copy of the GNU Lesser General Public License
#    along with sonos-nfc-read.  If not, see <http://www.gnu.org/licenses/>.


import RPi.GPIO as GPIO
import MFRC522
import signal
import NFCHelper
import argparse

continue_reading = True

# Capture SIGINT for cleanup when the script is aborted
def end_read(signal,frame):
    global continue_reading
    print("Ctrl+C captured, ending read.")
    continue_reading = False
    GPIO.cleanup()

# Hook the SIGINT
signal.signal(signal.SIGINT, end_read)

parser = argparse.ArgumentParser(description='Write NFC tags for sonos.')
#parser.add_argument('-nfcKey', type=str, default='FF:FF:FF:FF:FF:FF', help='The hex code of the nfc key to writ the content default: FF:FF:FF:FF:FF:FF')
args = parser.parse_args()



# Create an object of the class MFRC522
MIFAREReader = MFRC522.MFRC522()

print("Add NFC Tag ...")

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
        print("Card read UID: %s:%s:%s:%s" % (uid[0], uid[1], uid[2], uid[3]))
    
        
        # Select the scanned tag
        MIFAREReader.MFRC522_SelectTag(uid)

        # Dump the data
        MIFAREReader.MFRC522_DumpClassic1K(NFCHelper.AUTH_KEY_DEFAULT, uid)

        # Stop
        MIFAREReader.MFRC522_StopCrypto1()

