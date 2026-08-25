# SonarQube Python Demo

A minimal setup to scan a Python project with SonarQube locally using Docker Compose, and generate a self-contained local HTML report of the results.

## Contents

- `app.py` — simple demo Python app (a calculator) that gets scanned.
- `buggy_code.py` — intentionally messy code (bare `except`, mutable default
  argument, unused variable, weak hashing, empty method) so the scan has
  something to flag.
- `sonar-project.properties` — SonarQube scanner configuration.
- `docker-compose.yml` — spins up a local SonarQube server and a scanner container.
- `generate_report.py` — pulls issues/measures from the SonarQube API and writes a local `report.html`.
- `.github/workflows/sonarqube.yml` — GitHub Actions workflow that runs the
  scan automatically on every push/PR to `master`.

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

## CI: run the scan on every push (SonarCloud)

`.github/workflows/sonarqube.yml` runs the scan automatically via GitHub
Actions, against [SonarCloud](https://sonarcloud.io) (free for public repos).
A local `docker compose` SonarQube instance is NOT reachable from GitHub's
runners, so CI targets SonarCloud instead of your local server.

Setup (one-time, done via the SonarCloud website):

1. Log in to [sonarcloud.io](https://sonarcloud.io) with your GitHub account
   and authorize it.
2. **+ → Analyze new project** → pick `rameshwar-dudhe/sonarqube-python-demo`.
3. Note the **Organization Key** and **Project Key** it assigns (update
   `sonar.organization` / `sonar.projectKey` in `sonar-project.properties` to
   match if they differ from the defaults already set there).
4. **My Account → Security → Generate Token**, then add it as a repo secret:
   `Settings → Secrets and variables → Actions → New repository secret`,
   name it `SONAR_TOKEN`.

Once the secret is set, every push/PR to `master` triggers the scan and
results show up on your SonarCloud project dashboard.

## Notes

- `SONAR_TOKEN` must be set for both the scanner and the report generator.
- `report.html` requires the SonarQube server to be reachable while it's
  being generated (it queries the API), but the resulting file is fully
  offline afterwards.
