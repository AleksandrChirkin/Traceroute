import struct
import random


class IcmpPacket:
    def __init__(self, packet_type: int, code: int):
        self.packet_type = packet_type
        self.code = code

    def get_checksum(self) -> int:
        packet_octets = struct.pack('!2BH', self.packet_type, self.code, 0)
        acc = 0
        for i in range(0, len(packet_octets), 2):
            acc += (packet_octets[i] << 8) + packet_octets[i + 1]
        checksum = (acc >> 16) + (acc & 0xffff)
        return checksum & 0xffff

    def pack(self) -> bytes:
        checksum = self.get_checksum()
        return struct.pack('!2B3H', self.packet_type, self.code, checksum, 1,
                           random.randint(256, 3000))

    @staticmethod
    def from_bytes(data: bytes) -> 'IcmpPacket':
        return IcmpPacket(*struct.unpack('!BB', data[:2]))

    def __repr__(self) -> str:
        return f'Type: {self.packet_type}; Code: {self.code}'
