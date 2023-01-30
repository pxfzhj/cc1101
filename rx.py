
from time import sleep
from binascii import hexlify

from cc1101.config import RXConfig, Modulation
from cc1101 import CC1101

rx_config = RXConfig.new(frequency=434, modulation=Modulation.OOK, baud_rate=1, sync_word=0x0000, packet_length=64)
radio = CC1101("/dev/cc1101.1.0", rx_config, blocking=True)

while True:
    packets = radio.receive()

    for packet in packets:
        print(f"Received - {hexlify(packet)}")
    
    sleep(0.1)
