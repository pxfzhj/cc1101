
from time import sleep
from binascii import hexlify

from cc1101.config import RXConfig, Modulation
from cc1101 import CC1101

radio = CC1101("/dev/cc1101.1.0")

while True:
    packets = radio.receive()

    for packet in packets:
        print(f"Received - {hexlify(packet)}")
    
    sleep(0.1)
