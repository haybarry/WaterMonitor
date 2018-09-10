# WaterMonitor Project
This project is a test of the US-100 Ultrasonic Distance sensor for measuring water depth for Aquaponics project

## Project Hardware
Project Uses:
* ESP12E on Yellow Dev Board from Ali Express
* LM2596 Stepdown converter board from Ali Express
* Breakout Board designed and built by BH
* US-100 Ultrasonic Distance Sensor from Ali Express.
* Housed in Bunnings sealed box.

## Preparation  
* Download latest Micropython image  esp8266-20180511-v1.9.4.bin
* Jumper in Flash Position
* Erase ESP12E  esptool.py --port com4 --baud 115200 erase_flash.  esptool.py.exe currently in C:\Python36-32\Scripts
* Reset Board
* Program Micropython with esptool.py.exe  esptool.py --port com4 --baud 115200 write_flash --flash_size 4MB 0 esp8266-20180511-v1.9.4.bin
* Remove Flashing jumper.  Reset.  Connect Serial at 115200
* Use Ampy to load files to ESP12
  * Make library directory ampy --port com4 --baud 115200 ls
  * ampy --port com4 --baud 115200 put myfont12.py lib/myfont12.py
  * ampy --port com4 --baud 115200 put myfont15.py lib/myfont15.py
  * ampy --port com4 --baud 115200 put sh1106.py lib/sh1106.py
  * ampy --port com4 --baud 115200 put writer.py lib/writer.py
  * ampy --port com4 --baud 115200 put vl53l0x.py vl53l0x.py
* Use PyCharm to load main.py to ESP12E
