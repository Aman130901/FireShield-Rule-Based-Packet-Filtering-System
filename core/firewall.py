class Firewall:

    def __init__(self, rules):
        self.rules = rules

    def check_packet(self, packet):
        """
        Returns:
            ALLOW
            BLOCK
            DEFAULT BLOCK
        """

        for rule in self.rules:

            protocol_match = (
                rule["protocol"].upper() == packet.protocol.upper()
            )

            port_match = (
                rule["port"] == -1 or
                rule["port"] == packet.port
            )

            if protocol_match and port_match:
                return rule["action"]

        return "BLOCK"