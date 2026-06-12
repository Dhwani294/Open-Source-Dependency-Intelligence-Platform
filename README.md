# VulnGraph 🛡️
### Open-Source Dependency Intelligence Platform

> A production-style data engineering platform that analyzes software supply chain risk by ingesting vulnerability data from multiple sources, modeling dependency relationships, and exposing actionable security insights through analytics APIs.

![Python](https://img.shields.io/badge/Python-3.11-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-Backend-green)
![Airflow](https://img.shields.io/badge/Airflow-Orchestration-red)
![dbt](https://img.shields.io/badge/dbt-Transformations-orange)
![Docker](https://img.shields.io/badge/Docker-Containerized-blue)
![BigQuery](https://img.shields.io/badge/BigQuery-Warehouse-yellow)
![Status](https://img.shields.io/badge/Status-Portfolio_Project-success)

---



Modern software depends heavily on open-source packages.

A single vulnerability in a widely used dependency can affect thousands of downstream applications.

The challenge is not finding vulnerabilities.

The challenge is understanding:

- Which packages are affected?
- How quickly ecosystems patch security issues?
- Which maintainers represent the highest risk?
- What is the true blast radius of a CVE through dependency chains?

VulnGraph was built to answer those questions using a modern data engineering stack.

---

# Architecture

```text
                    ┌────────────────────┐
                    │ External Sources   │
                    │────────────────────│
                    │ NVD                │
                    │ PyPI               │
                    │ GitHub Advisory DB │
                    │ OSV.dev            │
                    │ Libraries.io       │
                    └──────────┬─────────┘
                               │
                               ▼
                    ┌────────────────────┐
                    │ Ingestion Layer    │
                    │ Python ETL Jobs    │
                    └──────────┬─────────┘
                               │
                               ▼
                    ┌────────────────────┐
                    │ Raw Storage        │
                    │ GCS / Local Mock   │
                    └──────────┬─────────┘
                               │
                               ▼
                    ┌────────────────────┐
                    │ BigQuery Warehouse │
                    │ Star Schema Model  │
                    └──────────┬─────────┘
                               │
                               ▼
                    ┌────────────────────┐
                    │ dbt Transformations│
                    │ + Data Quality     │
                    └──────────┬─────────┘
                               │
                               ▼
                    ┌────────────────────┐
                    │ Apache Airflow     │
                    │ Orchestration      │
                    └──────────┬─────────┘
                               │
                               ▼
                    ┌────────────────────┐
                    │ FastAPI Service    │
                    │ Analytics API      │
                    └────────────────────┘
```

---

# Tech Stack

| Layer | Technology |
|---------|-----------|
| Language | Python |
| API | FastAPI |
| Orchestration | Apache Airflow |
| Transformation | dbt |
| Data Warehouse | BigQuery |
| Storage | Google Cloud Storage |
| Containerization | Docker |
| Testing | Pytest |
| Data Modeling | Star Schema |
| Security Analytics | CVE Intelligence |

---

# Data Sources

The platform integrates five public security and package ecosystems:

| Source | Purpose |
|----------|---------|
| NVD (NIST) | CVE vulnerability records |
| PyPI API | Package metadata and release history |
| GitHub Advisory Database | Security advisories |
| OSV.dev | Cross-ecosystem vulnerabilities |
| Libraries.io | Dependency graph relationships |

---

# Data Warehouse Design

## Dimension Tables

### dim_packages
Tracks package metadata using SCD Type 2 history.

```sql
package_id
name
ecosystem
latest_version
maintainer_id
is_deprecated
effective_from
effective_to
is_current
```

### dim_maintainers

```sql
maintainer_id
handle
org
verified
```

### dim_versions

```sql
version_id
package_id
semver
release_date
yanked_flag
```

### dim_time

```sql
date_id
date
week
month
quarter
year
```

---

## Fact Tables

### fact_vulnerability_exposure

Stores package-level vulnerability impact.

```sql
vuln_id
package_id
version_id
severity_score
cvss_vector
patch_version
days_to_patch
affected_download_count
```

### fact_dependency_graph

Stores package dependency relationships.

```sql
dependent_package_id
dependency_id
version_constraint
ecosystem
depth_level
```

---

# Analytics Marts

The warehouse exposes four business-facing analytical models.

---

## mart_blast_radius

Answers:

> If a CVE affects Package A, which packages are impacted directly and transitively?

Features:

- Recursive CTE
- Multi-level graph traversal
- Dependency impact analysis
- Supply-chain risk visibility

---

## mart_patch_velocity

Measures:

- Average time-to-patch
- Ecosystem responsiveness
- Security remediation trends

Uses:

- Window functions
- Time-series analysis

---

## mart_maintainer_risk

Identifies:

- Single-maintainer packages
- High download count dependencies
- Critical unpatched vulnerabilities

Useful for:

- Risk scoring
- Third-party dependency reviews

---

## mart_ecosystem_health

Measures:

- Package abandonment rates
- Vulnerability density
- Rolling 90-day patch velocity

Provides ecosystem-level health metrics.

---

# Airflow Pipelines

## Daily Pipeline

Runs every day at 2 AM UTC.

```text
Ingest Sources
      ↓
Load Staging
      ↓
Run dbt Models
      ↓
Execute dbt Tests
      ↓
Publish Analytics
```

---

## Emergency Rescan Pipeline

Triggered automatically when:

```text
Severity = CRITICAL
```

Purpose:

- Immediate dependency graph recalculation
- Faster risk visibility
- Reduced response latency

---

# API Endpoints

## Blast Radius

```http
GET /api/v1/vulnerabilities/{cve_id}/blast-radius
```

Returns all affected packages across dependency chains.

---

## Package Risk Score

```http
GET /api/v1/packages/{package_name}/risk-score
```

Returns package-level security risk assessment.

---

## Patch Velocity

```http
GET /api/v1/ecosystems/{ecosystem}/patch-velocity
```

Measures remediation speed.

---

## Maintainer Exposure

```http
GET /api/v1/maintainers/{handle}/exposure
```

Returns vulnerability exposure metrics.

---

## Platform Health

```http
GET /api/v1/health
```

Returns system status and freshness metadata.

---

# Local Development

## Clone Repository

```bash
git clone https://github.com/Dhwani294/Dhwani294/Open-Source-Dependency-Intelligence-Platform.git
cd vulngraph
```

---

## Create Virtual Environment

```bash
python -m venv .venv
```

### Windows

```bash
.venv\Scripts\activate
```

### Linux / Mac

```bash
source .venv/bin/activate
```

---

## Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Start Full Platform

```bash
docker compose up --build
```

---

## FastAPI

```text
http://localhost:8000/docs
```

---

## Airflow

```text
http://localhost:8080
```

---

# Testing

Run all tests:

```bash
pytest -v
```

---

# Engineering Challenges

This project was intentionally designed to simulate real-world data engineering problems.

### Challenge 1
Flattening deeply nested NVD vulnerability records.

### Challenge 2
Handling multiple vulnerability schemas across ecosystems.

### Challenge 3
Building recursive dependency graph traversal.

### Challenge 4
Implementing SCD Type 2 package history tracking.

### Challenge 5
Orchestrating ingestion, transformation, and validation in a single workflow.

---

# Key Learnings

Building VulnGraph reinforced several important engineering lessons:

- Data quality is more important than data volume.
- Dependency graphs behave more like networks than tables.
- Analytics engineering benefits greatly from dbt model lineage.
- Orchestration should coordinate work, not perform it.
- Security intelligence becomes exponentially more valuable when historical context is preserved.

---

# Future Improvements

Planned enhancements include:

- Real-time streaming ingestion with Pub/Sub
- OpenTelemetry observability
- Kubernetes deployment
- CI/CD with GitHub Actions
- Graph database integration for dependency traversal
- Machine-learning based vulnerability risk prediction

---

# Project Highlights

✔ Multi-source ingestion pipeline

✔ Star-schema warehouse design

✔ SCD Type 2 dimensional modeling

✔ Recursive graph analytics

✔ Airflow orchestration

✔ dbt transformation layer

✔ FastAPI analytics service

✔ Dockerized local deployment

✔ End-to-end testing

---

# About This Project

This project was built as a portfolio-grade data engineering system to demonstrate practical experience with modern analytics engineering, data warehousing, orchestration, and security intelligence workflows.

It reflects the type of architecture commonly found in vulnerability management, software supply chain security, and enterprise analytics platforms.
