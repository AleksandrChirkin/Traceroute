from argparse import ArgumentParser
from traceroute import Tracer
from typing import Dict
import socket


def parse_args() -> Dict:
    parser = ArgumentParser(description='Traceroute')
    parser.add_argument('host', help='Host you want to trace')
    return parser.parse_args().__dict__


if __name__ == '__main__':
    args = parse_args()
    destination = args['host']
    try:
        tracer = Tracer(destination)
        for result in tracer.trace():
            print(f'{result}\r\n')
    except socket.gaierror:
        print(f'Address {destination} is invalid')
        exit(1)
    except PermissionError:
        print(f'Not enough rights. Try sudo or run as admin')
        exit(1)
