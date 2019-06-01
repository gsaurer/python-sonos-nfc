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
import math
import SonosController
import NFCHelper

continue_reading = True

## Capture SIGINT for cleanup when the script is aborted
def end_read(signal,frame):
    global continue_reading
    print("Ctrl+C captured, ending read.")
    continue_reading = False
    GPIO.cleanup()
# Hook the SIGINT
signal.signal(signal.SIGINT, end_read)

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
        
        dataSize = NFCHelper.read_Metadata(MIFAREReader, uid, NFCHelper.AUTH_KEY_DEFAULT)

        #Startsector
        sectorCount = NFCHelper.SECTOR_DATA_START
        #number of sectors
        numberOfSectorsToRead = math.ceil(dataSize / 16)

        print("Sector [%s-%s] need to be read." % (sectorCount, sectorCount + numberOfSectorsToRead))

        # read the data
        nfcData = ""
        numberOfSectorsReadCount = 0
        while numberOfSectorsReadCount < numberOfSectorsToRead and continue_reading:
            nfcData = nfcData + NFCHelper.read_Sector(MIFAREReader, uid, NFCHelper.AUTH_KEY_DEFAULT, sectorCount)
            sectorCount = sectorCount + 1 
            if(sectorCount % 4 == 3):
                sectorCount = sectorCount + 1 
            numberOfSectorsReadCount = numberOfSectorsReadCount + 1

        nfcData = nfcData[:dataSize]

        print("NFC Data: '%s'" % nfcData)

        # Stop
        MIFAREReader.MFRC522_StopCrypto1()
        
        #send command to server
        SonosController.play(nfcData)

        time.sleep(3)