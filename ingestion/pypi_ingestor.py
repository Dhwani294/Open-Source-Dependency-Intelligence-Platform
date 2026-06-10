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
    "package_name",
    "ecosystem",
    "version",
    "release_date",
    "maintainer_handle",
    "maintainer_org",
    "verified",
    "yanked_flag",
]


class PyPIIngestionError(Exception):
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
        raise PyPIIngestionError(
            f"Unable to load CSV: {exc}"
        ) from exc


def validate(df: pd.DataFrame) -> None:

    missing = (
        set(REQUIRED_COLUMNS)
        - set(df.columns)
    )

    if missing:
        raise PyPIIngestionError(
            f"Missing columns: {sorted(missing)}"
        )

    if df.empty:
        raise PyPIIngestionError(
            "CSV contains zero rows."
        )


def normalize(df: pd.DataFrame) -> pd.DataFrame:

    df = df.copy()

    df["release_date"] = pd.to_datetime(
        df["release_date"],
        errors="coerce",
        utc=True,
    )

    df["verified"] = (
        df["verified"]
        .astype(str)
        .str.lower()
        .map(
            {
                "true": True,
                "false": False,
            }
        )
    )

    df["yanked_flag"] = (
        df["yanked_flag"]
        .astype(str)
        .str.lower()
        .map(
            {
                "true": True,
                "false": False,
            }
        )
    )

    before = len(df)

    df = df.drop_duplicates(
        subset=[
            "package_name",
            "version",
        ]
    )

    removed = before - len(df)

    logger.info(
        "Removed %s duplicate package/version rows",
        removed,
    )

    return df


def build_packages(df: pd.DataFrame) -> list[dict[str, Any]]:

    latest_release = (
        df.sort_values(
            "release_date",
            ascending=False,
        )
        .groupby("package_name")
        .first()
        .reset_index()
    )

    packages = []

    for _, row in latest_release.iterrows():

        package_id = hashlib.md5(
            row["package_name"].encode()
        ).hexdigest()

        maintainer_id = hashlib.md5(
            row["maintainer_handle"].encode()
        ).hexdigest()

        packages.append(
            {
                "package_id": package_id,
                "name": row["package_name"],
                "ecosystem": row["ecosystem"],
                "latest_version": row["version"],
                "maintainer_id": maintainer_id,
                "is_deprecated": False,
            }
        )

    return packages


def build_versions(
    df: pd.DataFrame,
) -> list[dict[str, Any]]:

    versions = []

    for _, row in df.iterrows():

        package_id = hashlib.md5(
            row["package_name"].encode()
        ).hexdigest()

        version_id = hashlib.md5(
            (
                row["package_name"]
                + row["version"]
            ).encode()
        ).hexdigest()

        versions.append(
            {
                "version_id": version_id,
                "package_id": package_id,
                "semver": row["version"],
                "release_date": row[
                    "release_date"
                ].isoformat(),
                "yanked_flag": bool(
                    row["yanked_flag"]
                ),
            }
        )

    return versions


def build_maintainers(
    df: pd.DataFrame,
) -> list[dict[str, Any]]:

    maintainers = []

    unique = (
        df[
            [
                "maintainer_handle",
                "maintainer_org",
                "verified",
            ]
        ]
        .drop_duplicates()
        .reset_index(drop=True)
    )

    for _, row in unique.iterrows():

        maintainer_id = hashlib.md5(
            row[
                "maintainer_handle"
            ].encode()
        ).hexdigest()

        maintainers.append(
            {
                "maintainer_id": maintainer_id,
                "handle": row[
                    "maintainer_handle"
                ],
                "org": row[
                    "maintainer_org"
                ],
                "verified": bool(
                    row["verified"]
                ),
            }
        )

    return maintainers


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
        raise PyPIIngestionError(
            f"Failed writing output: {exc}"
        ) from exc


def run(
    input_file: str,
    output_file: str,
) -> None:

    logger.info(
        "Starting PyPI ingestion..."
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
        "package_count": len(
            df["package_name"]
            .unique()
        ),
        "version_count": len(df),
        "maintainer_count": len(
            df["maintainer_handle"]
            .unique()
        ),
        "packages": build_packages(
            df
        ),
        "versions": build_versions(
            df
        ),
        "maintainers": build_maintainers(
            df
        ),
    }

    write_output(
        output_file,
        payload,
    )

    logger.info(
        "PyPI ingestion complete."
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
            "PyPI ingestion failed."
        )
        raise SystemExit(1)


if __name__ == "__main__":
    main()