import argparse
from time import sleep

from rich.console import Console
from rich.live import Live
from rich.table import Table

from core.dashboard import Dashboard
from core.exporter import Exporter
from core.firewall import Firewall
from core.logger import FirewallLogger
from core.parser import RuleParser
from core.report import HTMLReport
from core.simulator import PacketSimulator

console = Console()


def main():

    # ---------------- CLI Arguments ---------------- #

    parser = argparse.ArgumentParser(
        description="FireShield - Rule-Based Packet Filtering System"
    )

    parser.add_argument(
        "--packets",
        type=int,
        default=20,
        help="Number of packets to simulate",
    )

    parser.add_argument(
        "--rules",
        type=str,
        default="config/rules.json",
        help="Path to firewall rules JSON file",
    )

    parser.add_argument(
        "--delay",
        type=float,
        default=0.25,
        help="Delay between packet processing",
    )

    args = parser.parse_args()

    console.print(
        "\n[bold red]🔥 FireShield - Rule-Based Packet Filtering System[/bold red]\n"
    )

    # ---------------- Load Rules ---------------- #

    rule_parser = RuleParser(args.rules)
    rules = rule_parser.load_rules()

    firewall = Firewall(rules)
    simulator = PacketSimulator()
    logger = FirewallLogger()
    report = HTMLReport()
    exporter = Exporter()

    packets = simulator.generate_packets(args.packets)

    allowed = 0
    blocked = 0

    report_packets = []

    # ---------------- Packet Table ---------------- #

    packet_table = Table(title="Firewall Packet Inspection")

    packet_table.add_column("#", style="cyan", justify="center")
    packet_table.add_column("Source IP", style="green")
    packet_table.add_column("Destination IP", style="yellow")
    packet_table.add_column("Protocol", style="magenta")
    packet_table.add_column("Port", justify="center")
    packet_table.add_column("Decision", justify="center")

    console.print("[bold cyan]Starting Live Firewall Inspection...[/bold cyan]\n")

    # ---------------- Live Dashboard ---------------- #

    with Live(
        Dashboard.create(0, len(packets), 0, 0),
        refresh_per_second=10,
        console=console,
    ) as live:

        for index, packet in enumerate(packets, start=1):

            decision = firewall.check_packet(packet)

            logger.log(packet, decision)

            if decision == "ALLOW":
                allowed += 1
                decision_color = "[bold green]ALLOW[/bold green]"
            else:
                blocked += 1
                decision_color = "[bold red]BLOCK[/bold red]"

            packet_table.add_row(
                str(index),
                packet.source_ip,
                packet.destination_ip,
                packet.protocol,
                str(packet.port),
                decision_color,
            )

            report_packets.append(
                {
                    "source": packet.source_ip,
                    "destination": packet.destination_ip,
                    "protocol": packet.protocol,
                    "port": packet.port,
                    "decision": decision,
                }
            )

            live.update(
                Dashboard.create(
                    index,
                    len(packets),
                    allowed,
                    blocked,
                    packet,
                )
            )

            sleep(args.delay)

    # ---------------- Results ---------------- #

    console.print()
    console.print(packet_table)

    summary = Table(title="Firewall Summary")

    summary.add_column("Metric", style="cyan")
    summary.add_column("Value", style="green")

    summary.add_row("Packets Processed", str(len(packets)))
    summary.add_row("Allowed", str(allowed))
    summary.add_row("Blocked", str(blocked))
    summary.add_row("Firewall Rules", str(len(rules)))
    summary.add_row("Log File", "logs/firewall.log")

    console.print(summary)

    # ---------------- Reports ---------------- #

    html_report = report.generate(
        report_packets,
        allowed,
        blocked,
    )

    csv_report = exporter.export_csv(report_packets)
    json_report = exporter.export_json(report_packets)

    console.print()

    console.print(
        f"[bold green]✔ HTML Report Generated:[/bold green] {html_report}"
    )

    console.print(
        f"[bold green]✔ CSV Report Generated:[/bold green] {csv_report}"
    )

    console.print(
        f"[bold green]✔ JSON Report Generated:[/bold green] {json_report}"
    )

    console.print(
        "[bold green]✔ Firewall Log Saved:[/bold green] logs/firewall.log"
    )

    console.print(
        "[bold green]✔ Packet Filtering Completed Successfully![/bold green]\n"
    )


if __name__ == "__main__":
    main()