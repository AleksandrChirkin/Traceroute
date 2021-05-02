from dataclasses import dataclass


@dataclass
class TraceResult:
    route: str
    n: int
    net_name: str
    as_zone: str
    country: str
    is_local: bool

    def __str__(self) -> str:
        result = f'{self.n}. {self.route}\r\n'
        if self.is_local:
            return f'{result}local\r\n'
        info = []
        if self.net_name:
            info.append(self.net_name)
        if self.as_zone:
            info.append(self.as_zone[2:])
        if self.country:
            info.append(self.country)
        return result +\
               (', '.join(info) + '\r\n' if len(info) > 0 else '*\r\n')
