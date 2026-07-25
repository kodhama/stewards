#!/usr/bin/env python3
"""Emit one closed marketplace observation from GitHub Actions runtime data."""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
import json
import os
from pathlib import Path
import tempfile

from validate_kodhama_plugin import Invalid, validate_observation


def required_environment(name: str) -> str:
    value = os.environ.get(name)
    if not value:
        raise SystemExit(f"missing required environment variable: {name}")
    return value


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--host", choices=("claude", "codex"), required=True)
    parser.add_argument("--surface-id", required=True)
    parser.add_argument("--marketplace-name", required=True)
    parser.add_argument("--marketplace-repository", required=True)
    parser.add_argument("--marketplace-revision", required=True)
    parser.add_argument("--workflow", required=True)
    parser.add_argument("--job", required=True)
    parser.add_argument("--setup-step-id", required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    if args.output.exists() or args.output.is_symlink():
        if args.output.is_dir() and not args.output.is_symlink():
            raise SystemExit("refusing observation output path that is a directory")
        args.output.unlink()

    observation = {
        "schema_version": 1,
        "host": args.host,
        "surface_id": args.surface_id,
        "marketplace": {
            "name": args.marketplace_name,
            "repository": args.marketplace_repository,
            "revision": args.marketplace_revision,
        },
        "execution": {
            "repository": required_environment("GITHUB_REPOSITORY"),
            "commit": required_environment("GITHUB_SHA"),
            "workflow": args.workflow,
            "job": args.job,
            "run_id": int(required_environment("GITHUB_RUN_ID")),
            "run_attempt": int(required_environment("GITHUB_RUN_ATTEMPT")),
            "setup_step_id": args.setup_step_id,
        },
        "observed_at": datetime.now(timezone.utc)
        .isoformat(timespec="milliseconds")
        .replace("+00:00", "Z"),
    }

    try:
        validate_observation(observation, "marketplace observation")
    except Invalid as error:
        raise SystemExit(f"refusing to emit invalid observation: {error}") from error

    args.output.parent.mkdir(parents=True, exist_ok=True)
    payload = json.dumps(observation, indent=2) + "\n"
    temporary_path = None
    try:
        with tempfile.NamedTemporaryFile(
            "w",
            encoding="utf-8",
            dir=args.output.parent,
            prefix=f".{args.output.name}.",
            delete=False,
        ) as temporary:
            temporary.write(payload)
            temporary_path = Path(temporary.name)
        validate_observation(
            json.loads(temporary_path.read_text(encoding="utf-8")),
            "serialized marketplace observation",
        )
        os.replace(temporary_path, args.output)
    finally:
        if temporary_path is not None:
            temporary_path.unlink(missing_ok=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
