#!/usr/bin/env python
# -*- coding: utf8 -*-
#
#    Copyright 2014,2018 Gerd Saurer <gerd.saurer@gmail.com>
#
#    You should have received a copy of the GNU Lesser General Public License
#    along with sonos-nfc-read.  If not, see <http://www.gnu.org/licenses/>.

import MFRC522

# This is the default key for authentication
AUTH_KEY_DEFAULT = [0xFF,0xFF,0xFF,0xFF,0xFF,0xFF]
#metainfoSector
SECTOR_META_INFO = 1
# StartSector
SECTOR_DATA_START = 4

def isInt(v):
    try:     i = int(v)
    except:  return False
    return True

# Method to read a sector content
def read_Sector(MIFAREReader, uid, key, sector):
    retVal = ""

     # Authenticate the sector
    status = MIFAREReader.MFRC522_Auth(MIFAREReader.PICC_AUTHENT1A, sector, key, uid)

    # Check if authenticated
    if status == MIFAREReader.MI_OK:
         #Read the data
         data = MIFAREReader.MFRC522_Read(sector)
         for i in data:
            if(i != 0):
                retVal = retVal + chr(i)            
            else:
                break
    else:
          print("Authentication error sector %s" % sector)

    return retVal

def read_Metadata(MIFAREReader, uid, key):
    dataSize = 0
    data = read_Sector(MIFAREReader, uid, key, SECTOR_META_INFO)
    print("Metadata is '%s'" % data)
    if(isInt(data)):
        dataSize = int(data)
    return dataSize
    

def write_Metadata(MIFAREReader, uid, key,  data):
    dataSize = str(len(data))
    write_Sector(MIFAREReader, uid, key, SECTOR_META_INFO, dataSize)

def clear_Metadata(MIFAREReader, uid, key):
    write_Sector(MIFAREReader, uid, key, SECTOR_META_INFO, "")

def clear_Sector(MIFAREReader, uid, key, sector):
    write_Sector(MIFAREReader, uid, key, sector, "")

# Method to write a sector content
def write_Sector(MIFAREReader, uid, key, sector, data):
    if sector == 0 or sector % 4 == 3:
        print("Sector %s can't be written" % sector)
        
    # Variable for the data to write
    byteData = bytearray()
    byteData.extend(data.encode('latin-1')) 

    #Fill rest of the array with 0x00
    while len(byteData) < 16:
        byteData.append(0x00)
    
    if(len(byteData) == 16):         
        write_SectorBytes(MIFAREReader, uid, key, sector, byteData)
    else:
        print("Data is too long %s bytes" % (len(data), data))


# Method to write a sector content
def write_SectorBytes(MIFAREReader, uid, key, sector, byteData):

    # Authenticat the sector
    status = MIFAREReader.MFRC522_Auth(MIFAREReader.PICC_AUTHENT1A, sector, key, uid)

    if status == MIFAREReader.MI_OK:
        if(len(byteData) == 16):         
            print("Sector %s will now be filled with '%s'" % (sector, str(byteData)))
            # Write the data
            MIFAREReader.MFRC522_Write(sector, byteData)
        else:
            print("Data is too long %s bytes" % (len(byteData), str(byteData)))
    else:
        print("Authentication error sector %s" % sector)