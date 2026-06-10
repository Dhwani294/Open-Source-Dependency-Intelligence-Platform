from __future__ import annotations

import os
from datetime import datetime

from airflow import DAG
from airflow.operators.bash import BashOperator


INGESTION_PATH = "/opt/airflow/ingestion"


default_args = {
    "owner": "vulngraph",
    "retries": 1,
}


with DAG(
    dag_id="daily_pipeline",
    default_args=default_args,
    start_date=datetime(2025, 1, 1),
    schedule="0 2 * * *",
    catchup=False,
    tags=["vulngraph", "daily"],
) as dag:

    ingest_nvd = BashOperator(
        task_id="ingest_nvd",
        bash_command=f"python {INGESTION_PATH}/nvd_ingestor.py --input data/sample/nvd_sample.csv --output data/sample/nvd_output.json",
    )

    ingest_pypi = BashOperator(
        task_id="ingest_pypi",
        bash_command=f"python {INGESTION_PATH}/pypi_ingestor.py --input data/sample/pypi_sample.csv --output data/sample/pypi_output.json",
    )

    ingest_osv = BashOperator(
        task_id="ingest_osv",
        bash_command=f"python {INGESTION_PATH}/osv_ingestor.py --input data/sample/osv_sample.csv --output data/sample/osv_output.json",
    )

    ingest_github = BashOperator(
        task_id="ingest_github",
        bash_command=f"python {INGESTION_PATH}/github_advisory_ingestor.py --input data/sample/github_advisory_sample.csv --output data/sample/github_advisory_output.json",
    )

    ingest_libraries = BashOperator(
        task_id="ingest_libraries",
        bash_command=f"python {INGESTION_PATH}/libraries_io_ingestor.py --input data/sample/libraries_io_sample.csv --output data/sample/libraries_io_output.json",
    )

    run_dbt = BashOperator(
        task_id="run_dbt",
        bash_command="cd dbt && dbt run --project-dir . --profiles-dir .",
    )

    test_dbt = BashOperator(
        task_id="test_dbt",
        bash_command="cd dbt && dbt test --project-dir . --profiles-dir .",
    )

    [
        ingest_nvd,
        ingest_pypi,
        ingest_osv,
        ingest_github,
        ingest_libraries,
    ] >> run_dbt >> test_dbt