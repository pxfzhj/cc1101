"""
Copyright (c) 2022
"""

import ctypes
import math

from enum import IntEnum
from typing import Dict, Tuple, Type, Optional

from cc1101.errors import ConfigError, ConfigException

# Crystal frequency of 26 Mhz
XTAL_FREQ = 26

class Registers(IntEnum):
    """Mapping of register name to address
    Extracted from SmartRF studio using @RN@@<<@= 0x@AH@ config string
    """

    IOCFG2 = 0x00  # GDO2 Output Pin Configuration
    IOCFG1 = 0x01  # GDO1 Output Pin Configuration
    IOCFG0 = 0x02  # GDO0 Output Pin Configuration
    FIFOTHR = 0x03  # RX FIFO and TX FIFO Thresholds
    SYNC1 = 0x04  # Sync Word, High Byte
    SYNC0 = 0x05  # Sync Word, Low Byte
    PKTLEN = 0x06  # Packet Length
    PKTCTRL1 = 0x07  # Packet Automation Control
    PKTCTRL0 = 0x08  # Packet Automation Control
    ADDR = 0x09  # Device Address
    CHANNR = 0x0A  # Channel Number
    FSCTRL1 = 0x0B  # Frequency Synthesizer Control
    FSCTRL0 = 0x0C  # Frequency Synthesizer Control
    FREQ2 = 0x0D  # Frequency Control Word, High Byte
    FREQ1 = 0x0E  # Frequency Control Word, Middle Byte
    FREQ0 = 0x0F  # Frequency Control Word, Low Byte
    MDMCFG4 = 0x10  # Modem Configuration
    MDMCFG3 = 0x11  # Modem Configuration
    MDMCFG2 = 0x12  # Modem Configuration
    MDMCFG1 = 0x13  # Modem Configuration
    MDMCFG0 = 0x14  # Modem Configuration
    DEVIATN = 0x15  # Modem Deviation Setting
    MCSM2 = 0x16  # Main Radio Control State Machine Configuration
    MCSM1 = 0x17  # Main Radio Control State Machine Configuration
    MCSM0 = 0x18  # Main Radio Control State Machine Configuration
    FOCCFG = 0x19  # Frequency Offset Compensation Configuration
    BSCFG = 0x1A  # Bit Synchronization Configuration
    AGCCTRL2 = 0x1B  # AGC Control
    AGCCTRL1 = 0x1C  # AGC Control
    AGCCTRL0 = 0x1D  # AGC Control
    WOREVT1 = 0x1E  # High Byte Event0 Timeout
    WOREVT0 = 0x1F  # Low Byte Event0 Timeout
    WORCTRL = 0x20  # Wake On Radio Control
    FREND1 = 0x21  # Front End RX Configuration
    FREND0 = 0x22  # Front End TX Configuration
    FSCAL3 = 0x23  # Frequency Synthesizer Calibration
    FSCAL2 = 0x24  # Frequency Synthesizer Calibration
    FSCAL1 = 0x25  # Frequency Synthesizer Calibration
    FSCAL0 = 0x26  # Frequency Synthesizer Calibration
    RCCTRL1 = 0x27  # RC Oscillator Configuration
    RCCTRL0 = 0x28  # RC Oscillator Configuration
    FSTEST = 0x29  # Frequency Synthesizer Calibration Control
    PTEST = 0x2A  # Production Test
    AGCTEST = 0x2B  # AGC Test
    TEST2 = 0x2C  # Various Test Settings
    TEST1 = 0x2D  # Various Test Settings
    TEST0 = 0x2E  # Various Test Settings


CONFIG_SIZE = 0x2F

class StatusRegisters(IntEnum):
    PARTNUM = 0x30
    VERSION = 0x31
    FREQEST = 0x32
    LQI = 0x33
    RSSI = 0x34
    MARCSTATE = 0x35
    WORTIME1 = 0x36
    WORTIME0 = 0x37
    PKTSTATUS = 0x38
    VCO_VC_DAC = 0x39
    TXBYTES = 0x3A
    RXBYTES = 0x3B
    RCCTRL1_STATUS = 0x3C
    RCCTRL0_STATUS = 0x3D

STATUS_SIZE = 0x0E

class cc1101_config_t(ctypes.Structure):
    """C struct definition for cc1101_rx_config from cc1101.h"""

    _fields_ = [
        ("frequency", ctypes.c_uint32),
        ("addr", ctypes.c_uint8),
        ("channel", ctypes.c_uint8),
        ("pa_gain", ctypes.c_uint8)
    ]

class CC1101Config:
    """Class for common configuration properties shared by TX and RX"""

    _frequency: int
    _addr: int
    _channel: int
    _pa_gain: int

    def __init__(
        self,
        frequency: float,
        addr:int,
        channel:int,
        pa_gain:int,

    ):
        self.set_frequency(frequency)
        self._addr = addr
        self._channel = channel
        self._pa_gain = pa_gain

    @staticmethod
    def frequency_to_config(frequency: float) -> int:
        """Convert a frequency in MHz to a configuration value

        Uses the formula from section 21 of the CC1101 datasheet
        """

        if not (
            (frequency >= 299.999756 and frequency <= 347.999939)
            or (frequency >= 386.999939 and frequency <= 463.999786)
            or (frequency >= 778.999878 and frequency <= 928.000000)
        ):
            raise ConfigException(ConfigError.INVALID_FREQUENCY)
        multiplier = (frequency * 2**16) / XTAL_FREQ
        return int(multiplier)

    @staticmethod
    def config_to_frequency(config: int) -> float:
        """Convert a configuration value to a frequency in MHz

        Uses the formula from section 21 of the CC1101 datasheet
        """
        return round((XTAL_FREQ / 2**16) * config, 6)

    def get_frequency(self) -> float:
        """Get the configured frequency"""
        return self.config_to_frequency(self._frequency)

    def set_frequency(self, frequency: float) -> None:
        """Set the frequency"""
        self._frequency = self.frequency_to_config(frequency)
    
    def get_addr(self) -> int:
        """Get the configured addr"""
        self._addr

    def set_addr(self, addr: int) -> None:
        """Set the addr"""
        self._addr = addr

    def get_channel(self) -> int:
        """Get the configured channel"""
        self._channel

    def set_channel(self, channel: int) -> None:
        """Set the channel"""
        self._channel = channel

    def get_pa_gain(self) -> int:
        """Get the configured size_t len,"""
        self._channel

    def set_channel(self, pa_gain: int) -> None:
        """Set the size_t len,"""
        self._channel = pa_gain

    @classmethod
    def size(cls: Type["CC1101Config"]) -> int:
        """Get the size in bytes of the configuration struct"""
        return ctypes.sizeof(cc1101_config_t)

    @classmethod
    def from_struct(
        cls: Type["CC1101Config"], config: cc1101_config_t
    ) -> "CC1101Config":
        """Construct a CC1101Config from a cc1101_config_t struct"""

        frequency = cls.config_to_frequency(config.frequency)

        return cls(frequency)

    def to_struct(self) -> cc1101_config_t:
        """Serialize a CommonConfig to a cc1101_common_config struct"""

        return cc1101_config_t(
            self._frequency,
            self._addr,
            self._channel,
            self._pa_gain
        )

    @classmethod
    def from_bytes(
        cls: Type["CC1101Config"], config_bytes: bytes
    ) -> Optional["CC1101Config"]:
        """Convert struct bytes from the CC1101 driver to a CC1101Config"""

        print(config_bytes)

        # Check for all zeroes in the config (not configured)
        if sum(config_bytes) == 0:
            return None

        config = cc1101_config_t.from_buffer_copy(config_bytes)
        return cls.from_struct(config)

    def to_bytes(self) -> bytearray:
        """Convert configuration to struct bytes to send to the CC1101 driver"""
        return bytearray(self.to_struct())

    def __repr__(self) -> str:
        ret = f"Frequency: {self.get_frequency()} MHz\n"
        ret += f"address: 0x{self.get_addr():08X}\n"
        ret += f"channel: 0x{self.get_channel():08X}\n"
        ret += f"pa_gain: 0x{self.get_pa_gain():08X}\n"
        return ret

def print_raw_config(config_bytes: bytes) -> None:
    """Print an array of CC1101 config bytes as register key/values"""
    config = {}

    for r in Registers:
        config[r.name] = config_bytes[r.value]

    for k in config.keys():
        print(f"{k}: {config[k]:02x}")

def print_raw_status(config_bytes: bytes) -> None:
    """Print an array of CC1101 status bytes as register key/values"""
    config = {}

    for r in StatusRegisters:
        config[r.name] = config_bytes[r.value]

    for k in config.keys():
        print(f"{k}: {config[k]:02x}")

def print_config(config_bytes: bytes):
    cf = CC1101Config.from_bytes(config_bytes)
    print(cf)
