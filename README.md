# 🔥 FireShield — Rule-Based Packet Filtering System

**FireShield** is a terminal-based firewall simulator that evaluates simulated network packets against a configurable, JSON-defined rule set — allowing or blocking each one in real time, then producing a full audit trail in HTML, CSV, JSON, and log formats.

It's built to demonstrate how rule-based firewalls make ALLOW/BLOCK decisions, with a live Rich-powered dashboard that visualizes every packet as it's inspected, making the filtering logic transparent and easy to follow.

---

## ✨ Features

- **Rule-based packet filtering engine** — evaluates each packet against an ordered list of protocol/port rules
- **JSON-configurable firewall rules** — add, remove, or reorder ALLOW/BLOCK rules without touching code
- **Default-deny policy** — any packet that doesn't match a rule is blocked automatically
- **Built-in packet simulator** — generates randomized TCP/UDP/ICMP traffic for demonstration and testing, with no live capture or root privileges required
- **Live terminal dashboard** — real-time Rich-based panel showing packets processed, allow/block counts, and the current packet being inspected
- **Full audit trail** — every decision is written to a persistent log file, and a full session report is exported to HTML, CSV, and JSON
- **Configurable simulation** — control packet count and processing delay via CLI flags

---

## 📸 Screenshots

Screenshots of the live dashboard, packet inspection table, firewall summary, and generated reports are available in the [`screenshots/`](./screenshots) folder.

---

## 🏗️ Architecture

FireShield runs a simple linear pipeline: load rules, generate packets, evaluate each one, then log and report the results.

```
 config/rules.json
        │
        ▼
 ┌───────────────┐
 │ RuleParser    │  (core/parser.py)     – loads firewall rules from JSON
 └───────┬───────┘
         ▼
 ┌───────────────┐        ┌──────────────────┐
 │ Firewall      │◄───────┤ PacketSimulator   │  (core/simulator.py) – generates random packets
 │ (core/firewall.py)     │  (core/packet.py) │  – ALLOW/BLOCK decision per packet
 └───────┬───────┘        └──────────────────┘
         ▼
 ┌────────────────────────────┐
 │ Dashboard   │ FirewallLogger│  (core/dashboard.py, core/logger.py)
 │ (live UI)   │ (logs/firewall.log)│
 └────────────────────────────┘
         ▼
 ┌───────────────────────────┐
 │ HTMLReport   │  Exporter   │  (core/report.py, core/exporter.py)
 │ (styled report)│ (CSV/JSON) │
 └───────────────────────────┘
```

Each packet flows through the `Firewall` class exactly once: it's checked against every rule in order, and the first matching rule's action wins. If nothing matches, the packet is blocked by default — a standard "default-deny" firewall posture.

---

## 📁 Project Structure

```
FireShield-Rule-Based-Packet-Filtering-System/
├── main.py                  # Entry point — CLI args, simulation loop, live dashboard
├── requirements.txt         # Python dependencies
├── config/
│   └── rules.json           # Firewall rule set (protocol, port, action)
├── core/
│   ├── packet.py              # Packet dataclass (source/destination IP, protocol, port)
│   ├── parser.py               # Loads and parses rules.json
│   ├── firewall.py             # Rule-matching & ALLOW/BLOCK decision logic
│   ├── simulator.py             # Randomized packet generator
│   ├── dashboard.py             # Live Rich dashboard panel
│   ├── logger.py                # Persistent firewall.log writer
│   ├── report.py                 # Jinja2-based HTML report generation
│   └── exporter.py               # CSV / JSON export of session results
├── logs/                     # Generated at runtime (firewall.log)
├── reports/                  # Generated at runtime (firewall_report.html, .csv, .json)
└── screenshots/              # Sample output screenshots
```

---

## ⚙️ Requirements

- Python 3.9+

Dependencies (see `requirements.txt`):

- [`rich`](https://pypi.org/project/rich/) — live terminal dashboard and tables
- [`Jinja2`](https://pypi.org/project/Jinja2/) — HTML report templating

> No elevated privileges are required — FireShield works entirely on simulated packets and does not sniff live network traffic.

---

## 🚀 Installation

```bash
# Clone the repository
git clone https://github.com/<your-username>/FireShield-Rule-Based-Packet-Filtering-System.git
cd FireShield-Rule-Based-Packet-Filtering-System

# (Recommended) create a virtual environment
python3 -m venv venv
source venv/bin/activate      # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

---

## ▶️ Usage

Run FireShield with default settings (20 simulated packets, default rule set):

```bash
python3 main.py
```

Customize the simulation with CLI flags:

```bash
python3 main.py --packets 50 --delay 0.1 --rules config/rules.json
```

| Flag | Description | Default |
|---|---|---|
| `--packets` | Number of packets to simulate | `20` |
| `--rules` | Path to the firewall rules JSON file | `config/rules.json` |
| `--delay` | Delay (in seconds) between processing each packet | `0.25` |

While running, FireShield displays a live-updating dashboard showing packets processed, allow/block counts, and details of the packet currently being inspected. On completion, it prints a full packet inspection table and a summary, then generates the session reports.

---

## 🔐 Firewall Rules

Rules are defined in `config/rules.json` as an ordered list, each with a protocol, port, and action:

```json
[
    { "action": "ALLOW", "protocol": "TCP", "port": 80 },
    { "action": "ALLOW", "protocol": "TCP", "port": 443 },
    { "action": "ALLOW", "protocol": "ICMP", "port": -1 },
    { "action": "BLOCK", "protocol": "TCP", "port": 23 },
    { "action": "BLOCK", "protocol": "UDP", "port": 69 }
]
```

- Rules are evaluated **in order** — the first matching rule determines the packet's fate.
- A port value of **`-1`** matches any port for that protocol (used for ICMP, which has no ports).
- Any packet that matches **no rule** is **blocked by default**.

You can edit `rules.json` directly to add new ALLOW/BLOCK rules, or point `--rules` at an entirely different rule file to test alternate firewall policies.

---

## 🗂️ Logging & Reports

Every session produces a full audit trail:

| Output | Format | Description |
|---|---|---|
| `logs/firewall.log` | Plain text | Timestamped line-by-line decision log for every packet |
| `reports/firewall_report.html` | HTML | Styled summary report with the full packet decision table |
| `reports/firewall_results.csv` | CSV | Spreadsheet-friendly export of all packet decisions |
| `reports/firewall_results.json` | JSON | Structured export for programmatic use |

---

## 🗺️ Roadmap Ideas

- Support live packet capture (e.g. via Scapy) as an alternative to simulated traffic
- Add IP-based and CIDR-range rule matching, not just protocol/port
- Support rule priorities or explicit ordering weights
- Add a "dry run" mode that reports decisions without writing packets to logs
- Web-based dashboard as an alternative to the terminal UI

---

## ⚠️ Disclaimer

FireShield operates entirely on simulated, randomly generated traffic for educational and demonstration purposes. It does not capture or filter real network traffic and should not be used as a production firewall.

---

## 👤 Author

**Aman Sonkar**
