from binascii import unhexlify

# from cc1101.config import TXConfig, Modulation
from cc1101.config import CC1101Config
from cc1101 import CC1101

# tx_config = TXConfig.new(frequency=434, modulation=Modulation.OOK, baud_rate=1, tx_power=0.1)
tx_config = CC1101Config(frequency=434, addr=1, channel=1, pa_gain=1)
radio = CC1101("/dev/cc1101.1.0")

radio.transmit(tx_config, unhexlify("0f0f0f0f0f0f0f0f0f0f0f"))