from datetime import datetime
import os


class FirewallLogger:

    def __init__(self):

        os.makedirs("logs", exist_ok=True)

        self.logfile = "logs/firewall.log"

    def log(self, packet, decision):

        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        line = (
            f"[{timestamp}] "
            f"{decision:<5} | "
            f"{packet.protocol:<4} | "
            f"{packet.source_ip:<15} -> "
            f"{packet.destination_ip:<15} | "
            f"Port {packet.port}\n"
        )

        with open(self.logfile, "a") as file:
            file.write(line)