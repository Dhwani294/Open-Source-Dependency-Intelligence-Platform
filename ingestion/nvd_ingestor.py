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
    "cve_id",
    "published_date",
    "last_modified_date",
    "severity_score",
    "cvss_vector",
    "description",
]


class NVDIngestionError(Exception):
    """Custom exception for NVD ingestion failures."""


def generate_batch_id(file_path: str) -> str:
    """
    Create deterministic batch id from file metadata.
    """

    stat = os.stat(file_path)

    raw = (
        f"{file_path}|"
        f"{stat.st_size}|"
        f"{stat.st_mtime}"
    )

    return hashlib.sha256(raw.encode()).hexdigest()


def validate_dataframe(df: pd.DataFrame) -> None:
    """
    Validate required schema.
    """

    missing = set(REQUIRED_COLUMNS) - set(df.columns)

    if missing:
        raise NVDIngestionError(
            f"Missing required columns: {sorted(missing)}"
        )

    if df.empty:
        raise NVDIngestionError(
            "Input file contains zero rows."
        )


def normalize_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    """
    Normalize datatypes and deduplicate.
    """

    df = df.copy()

    df["published_date"] = pd.to_datetime(
        df["published_date"],
        errors="coerce",
        utc=True,
    )

    df["last_modified_date"] = pd.to_datetime(
        df["last_modified_date"],
        errors="coerce",
        utc=True,
    )

    df["severity_score"] = pd.to_numeric(
        df["severity_score"],
        errors="coerce",
    )

    before_count = len(df)

    df = df.drop_duplicates(
        subset=["cve_id"],
        keep="latest" if False else "first"
    )

    after_count = len(df)

    logger.info(
        "Removed %s duplicate CVEs",
        before_count - after_count,
    )

    return df


def load_sample_csv(file_path: str) -> pd.DataFrame:
    """
    Load local sample data.
    """

    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(
            f"Sample file not found: {file_path}"
        )

    try:
        df = pd.read_csv(path)
        return df

    except Exception as exc:
        raise NVDIngestionError(
            f"Failed reading CSV: {exc}"
        ) from exc


def build_output_payload(
    df: pd.DataFrame,
    batch_id: str,
) -> dict[str, Any]:
    """
    Build ingestion artifact.
    """

    return {
        "batch_id": batch_id,
        "ingested_at": datetime.now(
            timezone.utc
        ).isoformat(),
        "row_count": int(len(df)),
        "records": df.to_dict(
            orient="records"
        ),
    }


def write_json_output(
    payload: dict[str, Any],
    output_path: str,
) -> None:
    """
    Persist normalized artifact.
    """

    try:
        with open(
            output_path,
            "w",
            encoding="utf-8",
        ) as f:
            json.dump(
                payload,
                f,
                indent=2,
                default=str,
            )

    except Exception as exc:
        raise NVDIngestionError(
            f"Failed writing output: {exc}"
        ) from exc


def run(
    input_file: str,
    output_file: str,
) -> None:

    logger.info(
        "Starting NVD ingestion from %s",
        input_file,
    )

    df = load_sample_csv(input_file)

    validate_dataframe(df)

    df = normalize_dataframe(df)

    batch_id = generate_batch_id(
        input_file
    )

    payload = build_output_payload(
        df,
        batch_id,
    )

    write_json_output(
        payload,
        output_file,
    )

    logger.info(
        "NVD ingestion completed. Rows=%s",
        len(df),
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
            input_file=args.input,
            output_file=args.output,
        )

    except Exception as exc:
        logger.exception(
            "NVD ingestion failed"
        )
        raise SystemExit(1) from exc


if __name__ == "__main__":
    main()