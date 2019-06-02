#!/usr/bin/env python
# -*- coding: utf8 -*-
#
#    Copyright 2014,2018 Gerd Saurer <gerd.saurer@gmail.com>
#
#    You should have received a copy of the GNU Lesser General Public License
#    along with sonos-nfc-read.  If not, see <http://www.gnu.org/licenses/>.

import requests
import json
import configparser

SONOS_BASE_URI = ""
SONOS_ROOM = ""

config = configparser.ConfigParser()
config.read('settings.ini')
SONOS_BASE_URI = config.get('Sonos', 'Server', fallback='http://192.168.10.2:5005')
SONOS_ROOM = config.get('Sonos', 'Room', fallback='Office')

def play(command):
    return playRoom(SONOS_ROOM, command)

def playRoom(room, command):
    sonosUri = SONOS_BASE_URI + "/%s/nfc/%s" % (room, command)
    executeSonosCommand(sonosUri)


def playPause(room):
    sonosUri = SONOS_BASE_URI + "/%s/playpause" % (room)
    executeSonosCommand(sonosUri)


def executeSonosCommand(sonosUri):
    print("Calling '%s'" % sonosUri)

    # Send command
    response = requests.get(sonosUri)
    print(response.json())

    if(response.status_code == 200):
        return True
    else:
        return False

