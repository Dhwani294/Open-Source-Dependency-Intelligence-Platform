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
    "ghsa_id",
    "cve_id",
    "package_name",
    "ecosystem",
    "severity",
    "cvss_score",
    "published_date",
    "patched_version",
]


class GitHubAdvisoryError(Exception):
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
        raise GitHubAdvisoryError(
            f"Failed reading file: {exc}"
        ) from exc


def validate(df: pd.DataFrame) -> None:

    missing = (
        set(REQUIRED_COLUMNS)
        - set(df.columns)
    )

    if missing:
        raise GitHubAdvisoryError(
            f"Missing columns: {sorted(missing)}"
        )

    if df.empty:
        raise GitHubAdvisoryError(
            "CSV contains zero rows."
        )


def normalize(df: pd.DataFrame) -> pd.DataFrame:

    df = df.copy()

    df["published_date"] = pd.to_datetime(
        df["published_date"],
        utc=True,
        errors="coerce",
    )

    df["cvss_score"] = pd.to_numeric(
        df["cvss_score"],
        errors="coerce",
    )

    before = len(df)

    df = df.drop_duplicates(
        subset=[
            "ghsa_id",
            "package_name",
        ]
    )

    logger.info(
        "Removed %s duplicate advisory rows",
        before - len(df),
    )

    return df


def build_records(
    df: pd.DataFrame,
) -> list[dict[str, Any]]:

    records = []

    for _, row in df.iterrows():

        records.append(
            {
                "ghsa_id": row["ghsa_id"],
                "cve_id": row["cve_id"],
                "package_name": row[
                    "package_name"
                ],
                "ecosystem": row[
                    "ecosystem"
                ],
                "severity": row[
                    "severity"
                ],
                "cvss_score": (
                    None
                    if pd.isna(
                        row["cvss_score"]
                    )
                    else float(
                        row["cvss_score"]
                    )
                ),
                "patched_version": row[
                    "patched_version"
                ],
                "published_date": row[
                    "published_date"
                ].isoformat(),
            }
        )

    return records


def advisory_summary(
    df: pd.DataFrame,
) -> list[dict[str, Any]]:

    result = []

    grouped = (
        df.groupby("severity")
        .size()
        .reset_index(name="count")
    )

    for _, row in grouped.iterrows():

        result.append(
            {
                "severity": row[
                    "severity"
                ],
                "count": int(
                    row["count"]
                ),
            }
        )

    return result


def write_output(
    output_path: str,
    payload: dict[str, Any],
) -> None:

    try:

        with open(
            output_path,
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
        raise GitHubAdvisoryError(
            f"Unable to write output: {exc}"
        ) from exc


def run(
    input_file: str,
    output_file: str,
) -> None:

    logger.info(
        "Starting GitHub Advisory ingestion..."
    )

    df = load_csv(input_file)

    validate(df)

    df = normalize(df)

    payload = {
        "batch_id": generate_batch_id(
            input_file
        ),
        "ingested_at": datetime.now(
            timezone.utc
        ).isoformat(),
        "record_count": len(df),
        "severity_summary": advisory_summary(
            df
        ),
        "records": build_records(df),
    }

    write_output(
        output_file,
        payload,
    )

    logger.info(
        "GitHub Advisory ingestion complete."
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
            "GitHub Advisory ingestion failed."
        )

        raise SystemExit(1)


if __name__ == "__main__":
    main()