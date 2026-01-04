from __future__ import annotations

import argparse


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="postshift")
    parser.add_argument("--version", action="store_true")
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    if args.version:
        print("postshift 0.0.0")
        return 0
    parser.print_help()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
