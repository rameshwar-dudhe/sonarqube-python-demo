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
    rows = "\n".join(
        f"<tr><td>{i['severity']}</td><td>{i['type']}</td>"
        f"<td>{i['component'].split(':')[-1]}</td>"
        f"<td>{i.get('line', '-')}</td><td>{i['message']}</td></tr>"
        for i in issues
    )
    summary = "".join(
        f"<li><b>{k}</b>: {v}</li>" for k, v in measures.items()
    )
    return f"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<title>SonarQube Report - {PROJECT_KEY}</title>
<style>
body {{ font-family: Arial, sans-serif; margin: 2rem; }}
table {{ border-collapse: collapse; width: 100%; }}
th, td {{ border: 1px solid #ccc; padding: 6px 10px; text-align: left; font-size: 14px; }}
th {{ background: #eee; }}
</style>
</head>
<body>
<h1>SonarQube Report: {PROJECT_KEY}</h1>
<p>Generated: {datetime.now().isoformat(timespec='seconds')}</p>
<h2>Summary</h2>
<ul>{summary}</ul>
<h2>Issues ({len(issues)})</h2>
<table>
<tr><th>Severity</th><th>Type</th><th>File</th><th>Line</th><th>Message</th></tr>
{rows}
</table>
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
