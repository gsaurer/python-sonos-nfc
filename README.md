SONOS NFC tooling
=================

This library can be leveraged in combination with [node-sonos-http-api](https://github.com/gsaurer/node-sonos-http-api) to controll the sonos service over RFID cards. This allows you to build a very flexible service for you children or to digitalize your libary by still looking at CD's. 

The library itself can write and read NFRC tags. I am leveraging an old [Raspberry Pi](http://raspberrypi.org) with an MFRC522 RFID Reader [Tutorial how to connect](https://www.youtube.com/watch?v=IeuQNXSNzxA) but you can also leverage an Arduio or other equipment if you want. 


Supported Services
------------------
* Local Sonos playlist
* Spotify 
* Apple Music
* Amazon Music
* Tunein

Requirements
------------
This code requires you to have 
* SPI-Py installed from the following [repository:](https://github.com/lthiery/SPI-Py)
* node-sonos-http-api installed from the following [repository:](https://github.com/gsaurer/node-sonos-http-api)
MFRC522.py from the [repository:](https://github.com/mxgxw/MFRC522-python) is included in this project and adapted to support python3 

How to use the lirbary
======================

Test Cards
----------

`python sonos-nfc-dump.py` 
Will let you read the content of the card. If this is successful you can start creating a card that can be leveraged to play content


Write Cards
----------

`python sonos-nfc-write.py -uri [URI]` 

will write a card with an URI that the sonos controller can play. Supported formats are: 
* Local Playlist: Format: playlist:[Playlist Name] e.g. playlist:Test 1
* Spotify: Format: [Spotify URI] e.g. spotify:album:12gOUR61KU69vYMaKZOPHV
* Apple Music: Format: applemusic:[song|album]:[id] e.g. applemusic:song:55364259 or applemusic:album:355363490
* Amazon Music: Format: amazonmusic:[song|album]:[id] e.g. amazonmusic:song:B009C7ZG38 or amazonmusic:album:B00720Z8PS
* TuneIn: Format: tunein:[id] e.g. tunein:8007

The card programm will write the uri to the card including some meta information to get the content right 


Read Cards
----------

`python sonos-nfc-read.py -sonosURI [URI of the node-sonos-http-api endpoint] -sonosRoom [Room the music should play in]` 

The programm will wait until you represent a card that was written with the service before. It will take the URI and send it to the sonos controller that can run on the same machine or on a server if you you like to leverage a central endpoint for other actions as well. 


Install on Raspberry Pi
----------

The read programm needs to be started when the raspberry pi starts thefore I added it to the rc.local file 

`sudo nano /etc/rc.local`
`sudo python3 /home/pi/python-sonos-nfc/sonos-nfc-read.py -sonosUri http://localhost:5005 -sonosRoom Office > /home/pi/python-sonos-nfc/log.txt &`

