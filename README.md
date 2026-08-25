# SonarQube Python Demo

A minimal setup to scan a Python project with SonarQube locally using Docker Compose, and generate a self-contained local HTML report of the results.

## Contents

- `app.py` — simple demo Python app (a calculator) that gets scanned.
- `sonar-project.properties` — SonarQube scanner configuration.
- `docker-compose.yml` — spins up a local SonarQube server and a scanner container.
- `generate_report.py` — pulls issues/measures from the SonarQube API and writes a local `report.html`.

## Usage

### 1. Start SonarQube server

```bash
docker compose up -d sonarqube
```

Wait until it's healthy (~1-2 min on first run):

```bash
docker compose ps
```

### 2. Create an access token

Open `http://localhost:9000`, log in (default `admin` / `admin`), then go to
**My Account → Security → Generate Token**.

```bash
export SONAR_TOKEN=your_token_here
```

### 3. Run the scan

```bash
docker compose --profile scan run --rm sonar-scanner
```

Results are pushed to the local SonarQube server and viewable at
`http://localhost:9000/dashboard?id=demo-python-project`.

### 4. Generate a local HTML report

```bash
pip install requests
python generate_report.py
```

This writes `report.html` — a standalone file with a summary (bugs,
vulnerabilities, code smells, coverage, duplication) and a full issue
table, viewable in any browser without SonarQube running.

## Notes

- `SONAR_TOKEN` must be set for both the scanner and the report generator.
- `report.html` requires the SonarQube server to be reachable while it's
  being generated (it queries the API), but the resulting file is fully
  offline afterwards.
