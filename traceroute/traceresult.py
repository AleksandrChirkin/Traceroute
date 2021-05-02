from dataclasses import dataclass
from typing import Dict


@dataclass
class TraceResult:
    route: str
    dst: str
    n: int
    net_name: str
    as_zone: str
    country: str
    is_local: bool

    @staticmethod
    def from_whois_data(dst: str, n: int, data: Dict) -> 'TraceResult':
        is_local = data is None
        route = data.get('route', '') if not is_local else ''
        country = data.get('country', '') if not is_local else ''
        as_zone = data.get('origin', '') if not is_local else ''
        net_name = data.get('netname', '') if not is_local else ''
        return TraceResult(route, dst, n, net_name, country, as_zone, is_local)

    def __str__(self) -> str:
        str_trace_res = f'{self.n}. {self.route} (Destination: {self.dst})\r\n'
        if self.is_local:
            return str_trace_res + 'local\r\n'
        info = []
        if self.net_name:
            info.append(self.net_name)
        if self.as_zone:
            info.append(self.as_zone)
        if self.country:
            info.append(self.country)
        return str_trace_res + ', '.join(info) + '\r\n'
