"""Fetch scan results from a local SonarQube server and save an HTML report."""

import os
import sys
from datetime import datetime

import requests

SONAR_URL = os.environ.get("SONAR_HOST_URL", "http://localhost:9000")
PROJECT_KEY = os.environ.get("SONAR_PROJECT_KEY", "demo-python-project")
TOKEN = os.environ.get("SONAR_TOKEN")

if not TOKEN:
    sys.exit("Set the SONAR_TOKEN environment variable before running this script.")

AUTH = (TOKEN, "")


def fetch_issues():
    issues = []
    page = 1
    while True:
        resp = requests.get(
            f"{SONAR_URL}/api/issues/search",
            params={"componentKeys": PROJECT_KEY, "p": page, "ps": 100},
            auth=AUTH,
            timeout=30,
        )
        resp.raise_for_status()
        data = resp.json()
        issues.extend(data.get("issues", []))
        if page * 100 >= data.get("total", 0):
            break
        page += 1
    return issues


def fetch_measures():
    metrics = "bugs,vulnerabilities,code_smells,coverage,duplicated_lines_density"
    resp = requests.get(
        f"{SONAR_URL}/api/measures/component",
        params={"component": PROJECT_KEY, "metricKeys": metrics},
        auth=AUTH,
        timeout=30,
    )
    resp.raise_for_status()
    measures = resp.json().get("component", {}).get("measures", [])
    return {m["metric"]: m["value"] for m in measures}


def build_html(measures, issues):
    if issues:
        rows = "\n".join(
            f"<tr><td>{i['severity']}</td><td>{i['type']}</td>"
            f"<td>{i['component'].split(':')[-1]}</td>"
            f"<td>{i.get('line', '-')}</td><td>{i['message']}</td></tr>"
            for i in issues
        )
        issues_block = f"""<table>
<tr><th>Severity</th><th>Type</th><th>File</th><th>Line</th><th>Message</th></tr>
{rows}
</table>"""
    else:
        issues_block = '<p class="empty">No issues found. Code is clean.</p>'

    cards = "".join(
        f'<div class="card"><div class="value">{v}</div><div class="label">{k.replace("_", " ")}</div></div>'
        for k, v in measures.items()
    )

    return f"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<title>SonarQube Report - {PROJECT_KEY}</title>
<style>
body {{ font-family: Arial, sans-serif; margin: 2rem; color: #222; }}
h1 {{ margin-bottom: 0.2rem; }}
.timestamp {{ color: #666; margin-top: 0; }}
.cards {{ display: flex; gap: 1rem; flex-wrap: wrap; margin: 1.5rem 0; }}
.card {{ border: 1px solid #ddd; border-radius: 8px; padding: 1rem 1.5rem; min-width: 110px; text-align: center; background: #fafafa; }}
.card .value {{ font-size: 1.8rem; font-weight: bold; }}
.card .label {{ font-size: 0.8rem; color: #666; text-transform: uppercase; margin-top: 0.3rem; }}
table {{ border-collapse: collapse; width: 100%; margin-top: 1rem; }}
th, td {{ border: 1px solid #ccc; padding: 6px 10px; text-align: left; font-size: 14px; }}
th {{ background: #eee; }}
.empty {{ padding: 1.5rem; border: 1px dashed #9c9; background: #f2fbf2; color: #2a7a2a; border-radius: 6px; }}
</style>
</head>
<body>
<h1>SonarQube Report: {PROJECT_KEY}</h1>
<p class="timestamp">Generated: {datetime.now().isoformat(timespec='seconds')}</p>
<h2>Summary</h2>
<div class="cards">{cards}</div>
<h2>Issues ({len(issues)})</h2>
{issues_block}
</body>
</html>
"""


def main():
    measures = fetch_measures()
    issues = fetch_issues()
    html = build_html(measures, issues)
    out_path = "report.html"
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"Report written to {out_path} ({len(issues)} issues found)")


if __name__ == "__main__":
    main()
