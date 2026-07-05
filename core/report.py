from datetime import datetime
from jinja2 import Template
import os


class HTMLReport:

    def generate(self, packets, allowed, blocked):

        html = """
<!DOCTYPE html>
<html>

<head>

<title>FireShield Report</title>

<style>

body{
font-family:Arial;
background:#f5f5f5;
margin:40px;
}

h1{
color:#c92a2a;
}

.summary{
background:white;
padding:20px;
border-radius:10px;
margin-bottom:30px;
}

table{
width:100%;
border-collapse:collapse;
background:white;
}

th,td{
border:1px solid #ddd;
padding:10px;
text-align:left;
}

th{
background:#212529;
color:white;
}

.allow{
color:green;
font-weight:bold;
}

.block{
color:red;
font-weight:bold;
}

</style>

</head>

<body>

<h1>FireShield Packet Filtering Report</h1>

<div class="summary">

<p><b>Date:</b> {{date}}</p>
<p><b>Total Packets:</b> {{total}}</p>
<p><b>Allowed:</b> {{allowed}}</p>
<p><b>Blocked:</b> {{blocked}}</p>

</div>

<table>

<tr>

<th>#</th>
<th>Source</th>
<th>Destination</th>
<th>Protocol</th>
<th>Port</th>
<th>Decision</th>

</tr>

{% for p in packets %}

<tr>

<td>{{loop.index}}</td>
<td>{{p.source}}</td>
<td>{{p.destination}}</td>
<td>{{p.protocol}}</td>
<td>{{p.port}}</td>

{% if p.decision=="ALLOW" %}
<td class="allow">{{p.decision}}</td>
{% else %}
<td class="block">{{p.decision}}</td>
{% endif %}

</tr>

{% endfor %}

</table>

</body>

</html>

"""

        template = Template(html)

        output = template.render(
            date=datetime.now().strftime("%d-%m-%Y %H:%M:%S"),
            total=len(packets),
            allowed=allowed,
            blocked=blocked,
            packets=packets
        )

        os.makedirs("reports", exist_ok=True)

        path = "reports/firewall_report.html"

        with open(path, "w") as file:
            file.write(output)

        return path