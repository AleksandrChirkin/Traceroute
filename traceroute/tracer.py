from traceroute import IcmpPacket, TraceResult
from typing import Dict, Generator, Optional
import socket


class Tracer:
    def __init__(self, dst: str):
        self.ttl = 1
        self.max_hops = 30
        self.destination = socket.gethostbyname(dst)
        if self.destination == socket.gethostbyname('localhost'):
            self.max_hops = 1

    @staticmethod
    def get_whois_iana_data(addr) -> str:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as whois_sock:
            whois_sock.settimeout(1)
            whois_sock.connect((socket.gethostbyname('whois.iana.org'), 43))
            whois_sock.send(addr.encode(encoding='utf-8') + b'\r\n')
            try:
                iana_response = whois_sock.recv(1024).decode()
                whois_addr_start = iana_response.index('whois')
                whois_addr_end = iana_response.index('\n', whois_addr_start)
                whois_addr = iana_response[whois_addr_start:whois_addr_end].\
                    replace(' ', '').split(':')[0]
                return whois_addr
            except (socket.timeout, ValueError):
                pass
        return ''

    def get_whois_data(self, addr: str) -> Optional[Dict]:
        whois_addr = self.get_whois_iana_data(addr)
        whois_data = {}
        if not whois_addr:
            return
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as whois_sock:
            whois_sock.settimeout(2)
            whois_sock.connect((whois_addr, 43))
            whois_sock.send(addr.encode(encoding='utf-8') + b'\r\n')
            data = b''
            while True:
                temp_data = whois_sock.recv(1024)
                if not temp_data:
                    break
                data += temp_data
            data = data.decode()
            for field in ('netname', 'country', 'route', 'origin'):
                try:
                    field_start = data.rindex(field)
                    field_end = data.index('\n', field_start)
                    field_data = data[field_start:field_end].\
                        replace(' ', '').split(':')[1]
                    whois_data[field] = field_data
                except ValueError:
                    continue
        return whois_data

    def trace(self) -> Generator[TraceResult, None, None]:
        n = 1
        while self.ttl <= self.max_hops:
            with socket.socket(socket.AF_INET, socket.SOCK_DGRAM,
                               socket.IPPROTO_ICMP) as sender, \
                    socket.socket(socket.AF_INET, socket.SOCK_RAW,
                                  socket.IPPROTO_ICMP) as receiver:
                sender.setsockopt(socket.SOL_IP, socket.IP_TTL, self.ttl)
                receiver.settimeout(3)
                sender.sendto(IcmpPacket(8, 0).pack(), (self.destination, 80))
                try:
                    data, addr = receiver.recvfrom(1024)
                    whois_data = self.get_whois_data(addr[0])
                    icmp_response = IcmpPacket.from_bytes(data[20:])
                    trace_result = TraceResult.from_whois_data\
                        (self.destination, n, whois_data)
                    n += 1
                    yield trace_result
                    if icmp_response.code == icmp_response.packet_type == 0:
                        break
                except socket.timeout:
                    continue
                finally:
                    self.ttl += 1
