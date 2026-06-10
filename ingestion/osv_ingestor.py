from __future__ import annotations

import argparse
import hashlib
import json
import logging
import os
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import pandas as pd


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
)

logger = logging.getLogger(__name__)


REQUIRED_COLUMNS = [
    "osv_id",
    "ecosystem",
    "package_name",
    "severity_score",
    "affected_version",
    "fixed_version",
    "published_date",
]


class OSVIngestionError(Exception):
    pass


def generate_batch_id(file_path: str) -> str:
    stat = os.stat(file_path)

    seed = (
        f"{file_path}|"
        f"{stat.st_size}|"
        f"{stat.st_mtime}"
    )

    return hashlib.sha256(
        seed.encode()
    ).hexdigest()


def load_csv(file_path: str) -> pd.DataFrame:

    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(
            f"File not found: {file_path}"
        )

    try:
        return pd.read_csv(path)

    except Exception as exc:
        raise OSVIngestionError(
            f"Unable to read CSV: {exc}"
        ) from exc


def validate(df: pd.DataFrame) -> None:

    missing = (
        set(REQUIRED_COLUMNS)
        - set(df.columns)
    )

    if missing:
        raise OSVIngestionError(
            f"Missing columns: {sorted(missing)}"
        )

    if df.empty:
        raise OSVIngestionError(
            "CSV contains zero rows."
        )


def normalize(df: pd.DataFrame) -> pd.DataFrame:

    df = df.copy()

    df["severity_score"] = pd.to_numeric(
        df["severity_score"],
        errors="coerce",
    )

    df["published_date"] = pd.to_datetime(
        df["published_date"],
        utc=True,
        errors="coerce",
    )

    before = len(df)

    df = df.drop_duplicates(
        subset=[
            "osv_id",
            "package_name",
            "affected_version",
        ]
    )

    removed = before - len(df)

    logger.info(
        "Removed %s duplicate OSV rows",
        removed,
    )

    return df


def severity_bucket(
    score: float,
) -> str:

    if pd.isna(score):
        return "UNKNOWN"

    if score >= 9.0:
        return "CRITICAL"

    if score >= 7.0:
        return "HIGH"

    if score >= 4.0:
        return "MEDIUM"

    return "LOW"


def build_records(
    df: pd.DataFrame,
) -> list[dict[str, Any]]:

    rows = []

    for _, row in df.iterrows():

        rows.append(
            {
                "vuln_id": row["osv_id"],
                "ecosystem": row["ecosystem"],
                "package_name": row["package_name"],
                "severity_score": (
                    None
                    if pd.isna(
                        row["severity_score"]
                    )
                    else float(
                        row["severity_score"]
                    )
                ),
                "severity_bucket": severity_bucket(
                    row["severity_score"]
                ),
                "affected_version": row[
                    "affected_version"
                ],
                "fixed_version": row[
                    "fixed_version"
                ],
                "published_date": row[
                    "published_date"
                ].isoformat(),
            }
        )

    return rows


def ecosystem_summary(
    df: pd.DataFrame,
) -> list[dict[str, Any]]:

    summary = []

    grouped = (
        df.groupby("ecosystem")
        .size()
        .reset_index(name="count")
    )

    for _, row in grouped.iterrows():

        summary.append(
            {
                "ecosystem": row[
                    "ecosystem"
                ],
                "vulnerability_count": int(
                    row["count"]
                ),
            }
        )

    return summary


def write_output(
    output_file: str,
    payload: dict[str, Any],
) -> None:

    try:

        with open(
            output_file,
            "w",
            encoding="utf-8",
        ) as fp:

            json.dump(
                payload,
                fp,
                indent=2,
                default=str,
            )

    except Exception as exc:
        raise OSVIngestionError(
            f"Failed writing output: {exc}"
        ) from exc


def run(
    input_file: str,
    output_file: str,
) -> None:

    logger.info(
        "Starting OSV ingestion..."
    )

    df = load_csv(input_file)

    validate(df)

    df = normalize(df)

    batch_id = generate_batch_id(
        input_file
    )

    payload = {
        "batch_id": batch_id,
        "ingested_at": datetime.now(
            timezone.utc
        ).isoformat(),
        "record_count": len(df),
        "ecosystem_count": len(
            df["ecosystem"].unique()
        ),
        "ecosystem_summary": ecosystem_summary(
            df
        ),
        "records": build_records(df),
    }

    write_output(
        output_file,
        payload,
    )

    logger.info(
        "OSV ingestion complete."
    )


def main() -> None:

    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--input",
        required=True,
    )

    parser.add_argument(
        "--output",
        required=True,
    )

    args = parser.parse_args()

    try:

        run(
            args.input,
            args.output,
        )

    except Exception:

        logger.exception(
            "OSV ingestion failed."
        )

        raise SystemExit(1)


if __name__ == "__main__":
    main()