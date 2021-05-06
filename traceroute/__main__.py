from argparse import ArgumentParser
from traceroute import Tracer
import socket


def parse_args():
    parser = ArgumentParser(description='Traceroute')
    parser.add_argument('host', help='Host you want to trace')
    return parser.parse_args()


if __name__ == '__main__':
    args = parse_args()
    destination = args.host
    try:
        tracer = Tracer(destination)
        for result in tracer.trace():
            print(f'{result}\r\n')
    except socket.gaierror:
        print(f'Address {destination} is invalid')
        exit(1)
    except PermissionError:
        print('Not enough rights')
        exit(1)
    except KeyboardInterrupt:
        print('Terminated.')
