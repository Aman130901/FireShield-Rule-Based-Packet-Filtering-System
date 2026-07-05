import csv
import json
import os


class Exporter:

    def __init__(self):
        os.makedirs("reports", exist_ok=True)

    def export_csv(self, packets):

        filename = "reports/firewall_results.csv"

        with open(filename, "w", newline="") as file:

            writer = csv.writer(file)

            writer.writerow([
                "Source IP",
                "Destination IP",
                "Protocol",
                "Port",
                "Decision"
            ])

            for packet in packets:
                writer.writerow([
                    packet["source"],
                    packet["destination"],
                    packet["protocol"],
                    packet["port"],
                    packet["decision"]
                ])

        return filename

    def export_json(self, packets):

        filename = "reports/firewall_results.json"

        with open(filename, "w") as file:
            json.dump(packets, file, indent=4)

        return filename