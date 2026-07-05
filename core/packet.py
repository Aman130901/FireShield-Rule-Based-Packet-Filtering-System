from dataclasses import dataclass


@dataclass
class Packet:
    source_ip: str
    destination_ip: str
    protocol: str
    port: int