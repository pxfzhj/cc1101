"""
Copyright (c) 2022
"""

import argparse
import sys
import time

from binascii import hexlify, unhexlify

from . import config, CC1101


def tx(args: argparse.Namespace) -> None:
    """Handle the tx subcommand"""

    cc1101 = CC1101(args.device, None)
    cc1101.transmit(unhexlify(args.packet))



def rx(args: argparse.Namespace) -> None:
    """Handle the rx subcommand"""

    cc1101 = CC1101(args.device, None)

    count = 1
    min_rssi = None
    max_rssi = None

    print("Receiving Packets", file=sys.stderr)
    while True:
        if args.out_format == "rssi":
            rssi = cc1101.get_rssi()

            if min_rssi is None or rssi < min_rssi:
                min_rssi = rssi

            if max_rssi is None or rssi > max_rssi:
                max_rssi = rssi

            output = (
                f"\rCurrent: {rssi} dB / Min: {min_rssi} dB / Max: {max_rssi} dB"
            )
            sys.stdout.write("\r" + " " * count)
            sys.stdout.write("\r" + output)
            count = len(output)
        else:
            for packet in cc1101.receive():
                if args.out_format in ["hex", "info"]:
                    packet_hex = hexlify(packet).decode("ascii")

                        if args.out_format == "info":
                            print(f"[{count} - {cc1101.get_rssi()} dB] {packet_hex}")
                        else:
                            print(packet_hex)
                else:
                    sys.stdout.buffer.write(packet)

                count += 1
            time.sleep(0.1)


def conf(args: argparse.Namespace) -> None:
    """Handle the conf subcommand"""

    cc1101 = CC1101(args.device, None)

    if args.conf_type == "config_set":
        cc1101.set_config(args)

    elif args.conf_type == "config_raw":
        config.print_config(cc1101.get_config())

    elif args.conf_type == "dev_raw":
        config.print_raw_config(cc1101.get_device_config())

    elif args.conf_type == "dev_status":
        config.print_raw_status(cc1101.get_device_status())

    print(f"Max Packet Size: {cc1101.get_max_packet_size()}")


def reset(args: argparse.Namespace) -> None:
    """Handle the reset subcommand"""

    cc1101 = CC1101(args.device, None)
    cc1101.reset()


def main() -> None:
    parser = argparse.ArgumentParser(prog="cc1101")
    subparsers = parser.add_subparsers()

    tx_parser = subparsers.add_parser("tx", help="Transmit a Packet")
    tx_parser.add_argument("device", help="CC1101 Device")
    tx_parser.add_argument("packet", help="packet to transmit (hexadecimal string)")

    tx_parser.set_defaults(func=tx)

    rx_parser = subparsers.add_parser("rx", help="Receive Packets")
    rx_parser.add_argument("device", help="CC1101 Device")
    rx_parser.add_argument("packet_size", help="receive packet size (bytes)")
    rx_parser.add_argument(
        "--block", action="store_true", help="obtain an exclusive lock on the device"
    )
    rx_parser.add_argument(
        "--out-format",
        choices=["hex", "bin", "info", "rssi"],
        default="hex",
        help="output format",
    )

    rx_parser.set_defaults(func=rx)

    conf_parser = subparsers.add_parser("config", help="Get Device Configs")
    conf_parser.add_argument("device", help="CC1101 Device")
    conf_parser.add_argument(
        "conf_type",
        help="Config to get",
        choices=["config_set", "config_raw", "dev_raw", "dev_status"],
    )
    conf_parser.set_defaults(func=conf)

    reset_parser = subparsers.add_parser("reset", help="Reset Device")
    reset_parser.add_argument("device", help="CC1101 Device")
    reset_parser.set_defaults(func=reset)

    args = parser.parse_args()

    if "func" in args:
        args.func(args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
