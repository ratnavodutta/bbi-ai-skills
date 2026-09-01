from __future__ import annotations

import argparse
import json
from pathlib import Path

from .diagnostics import run_diagnostics


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="client-network-agent",
        description="Collect network and compute evidence for client connectivity issues.",
    )
    parser.add_argument(
        "--target",
        required=True,
        help="Server, IP, hostname, URL, or API endpoint to test.",
    )
    parser.add_argument(
        "--output-dir",
        default="logs",
        help="Directory where evidence files will be written. Default: logs",
    )
    parser.add_argument(
        "--timeout",
        type=int,
        default=20,
        help="Per-command timeout in seconds. Default: 20",
    )
    parser.add_argument(
        "--deep",
        action="store_true",
        help="Run slower optional checks such as extended route/path diagnostics when available.",
    )
    parser.add_argument(
        "--no-http-body",
        action="store_true",
        help="Only collect HTTP headers and timing for URL/API targets.",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    result = run_diagnostics(
        target=args.target,
        output_dir=Path(args.output_dir),
        timeout_seconds=args.timeout,
        deep=args.deep,
        include_http_body=not args.no_http_body,
    )

    print(json.dumps(result["summary"], indent=2))
    print(f"Evidence JSON: {result['files']['json']}")
    print(f"Evidence TXT:  {result['files']['text']}")
    return 0
