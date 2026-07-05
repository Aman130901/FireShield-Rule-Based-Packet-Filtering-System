import random

from core.packet import Packet


class PacketSimulator:

    PROTOCOLS = ["TCP", "UDP", "ICMP"]

    PORTS = [
        22,
        23,
        53,
        69,
        80,
        110,
        143,
        443,
        3306,
        8080
    ]

    def random_ip(self):
        return f"192.168.0.{random.randint(2,254)}"

    def generate_packet(self):

        protocol = random.choice(self.PROTOCOLS)

        if protocol == "ICMP":
            port = -1
        else:
            port = random.choice(self.PORTS)

        return Packet(
            source_ip=self.random_ip(),
            destination_ip="192.168.0.1",
            protocol=protocol,
            port=port
        )

    def generate_packets(self, count=20):

        packets = []

        for _ in range(count):
            packets.append(self.generate_packet())

        return packets