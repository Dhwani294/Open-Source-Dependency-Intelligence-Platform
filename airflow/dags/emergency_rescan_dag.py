from __future__ import annotations

from datetime import datetime

from airflow import DAG
from airflow.operators.bash import BashOperator


default_args = {
    "owner": "vulngraph",
}


with DAG(
    dag_id="emergency_rescan",
    default_args=default_args,
    start_date=datetime(2025, 1, 1),
    schedule=None,
    catchup=False,
    tags=["vulngraph", "emergency"],
) as dag:

    rescan_graph = BashOperator(
        task_id="rescan_dependency_graph",
        bash_command="cd dbt && dbt run --select fact_dependency_graph",
    )