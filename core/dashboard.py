from rich.table import Table
from rich.panel import Panel


class Dashboard:

    @staticmethod
    def create(processed, total, allowed, blocked, packet=None):

        table = Table(show_header=False)

        table.add_row("📦 Packets Processed", f"{processed}/{total}")
        table.add_row("✅ Allowed", str(allowed))
        table.add_row("❌ Blocked", str(blocked))

        if packet:

            table.add_row("🌐 Source", packet.source_ip)
            table.add_row("🎯 Destination", packet.destination_ip)
            table.add_row("📡 Protocol", packet.protocol)
            table.add_row("🔌 Port", str(packet.port))

        return Panel(
            table,
            title="🔥 FireShield Live Dashboard",
            border_style="red"
        )