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
    "dependency_name",
    "version_constraint",
    "depth_level",
    "maintainer_handle",
    "deprecated_flag",
    "snapshot_date",
]


class LibrariesIOIngestionError(Exception):
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


def package_id(name: str) -> str:
    return hashlib.md5(
        name.encode()
    ).hexdigest()


def maintainer_id(handle: str) -> str:
    return hashlib.md5(
        handle.encode()
    ).hexdigest()


def load_csv(
    file_path: str,
) -> pd.DataFrame:

    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(
            f"File not found: {file_path}"
        )

    try:
        return pd.read_csv(path)

    except Exception as exc:
        raise LibrariesIOIngestionError(
            f"Unable to load file: {exc}"
        ) from exc


def validate(
    df: pd.DataFrame,
) -> None:

    missing = (
        set(REQUIRED_COLUMNS)
        - set(df.columns)
    )

    if missing:
        raise LibrariesIOIngestionError(
            f"Missing columns: {sorted(missing)}"
        )

    if df.empty:
        raise LibrariesIOIngestionError(
            "Input contains zero rows."
        )


def normalize(
    df: pd.DataFrame,
) -> pd.DataFrame:

    df = df.copy()

    df["snapshot_date"] = pd.to_datetime(
        df["snapshot_date"],
        utc=True,
        errors="coerce",
    )

    df["depth_level"] = pd.to_numeric(
        df["depth_level"],
        errors="coerce",
    )

    df["deprecated_flag"] = (
        df["deprecated_flag"]
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
            "dependency_name",
            "version_constraint",
        ]
    )

    logger.info(
        "Removed %s duplicate dependency rows",
        before - len(df),
    )

    return df


def build_packages(
    df: pd.DataFrame,
) -> list[dict[str, Any]]:

    latest = (
        df.sort_values(
            "snapshot_date",
            ascending=False,
        )
        .groupby("package_name")
        .first()
        .reset_index()
    )

    rows = []

    for _, row in latest.iterrows():

        rows.append(
            {
                "package_id": package_id(
                    row["package_name"]
                ),
                "package_name": row[
                    "package_name"
                ],
                "ecosystem": row[
                    "ecosystem"
                ],
                "maintainer_id": maintainer_id(
                    row["maintainer_handle"]
                ),
                "is_deprecated": bool(
                    row["deprecated_flag"]
                ),
            }
        )

    return rows


def build_dependency_graph(
    df: pd.DataFrame,
) -> list[dict[str, Any]]:

    rows = []

    for _, row in df.iterrows():

        rows.append(
            {
                "dependent_package_id":
                    package_id(
                        row["package_name"]
                    ),
                "dependency_id":
                    package_id(
                        row["dependency_name"]
                    ),
                "version_constraint":
                    row[
                        "version_constraint"
                    ],
                "ecosystem":
                    row["ecosystem"],
                "depth_level":
                    int(
                        row["depth_level"]
                    ),
            }
        )

    return rows


def build_package_history(
    df: pd.DataFrame,
) -> list[dict[str, Any]]:

    rows = []

    ordered = df.sort_values(
        [
            "package_name",
            "snapshot_date",
        ]
    )

    for _, row in ordered.iterrows():

        rows.append(
            {
                "package_id":
                    package_id(
                        row["package_name"]
                    ),
                "maintainer_id":
                    maintainer_id(
                        row[
                            "maintainer_handle"
                        ]
                    ),
                "is_deprecated":
                    bool(
                        row[
                            "deprecated_flag"
                        ]
                    ),
                "effective_from":
                    row[
                        "snapshot_date"
                    ].isoformat(),
            }
        )

    return rows


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
        raise LibrariesIOIngestionError(
            f"Failed writing output: {exc}"
        ) from exc


def run(
    input_file: str,
    output_file: str,
) -> None:

    logger.info(
        "Starting Libraries.io ingestion..."
    )

    df = load_csv(
        input_file
    )

    validate(df)

    df = normalize(df)

    payload = {
        "batch_id":
            generate_batch_id(
                input_file
            ),
        "ingested_at":
            datetime.now(
                timezone.utc
            ).isoformat(),
        "package_count":
            len(
                df[
                    "package_name"
                ].unique()
            ),
        "dependency_count":
            len(df),
        "packages":
            build_packages(df),
        "dependencies":
            build_dependency_graph(df),
        "package_history":
            build_package_history(df),
    }

    write_output(
        output_file,
        payload,
    )

    logger.info(
        "Libraries.io ingestion complete."
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
            "Libraries.io ingestion failed."
        )

        raise SystemExit(1)


if __name__ == "__main__":
    main()