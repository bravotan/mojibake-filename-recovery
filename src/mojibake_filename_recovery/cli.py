"""mojibake-filename-recovery の CLI エントリポイント。"""

from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path

from .core import recover_name


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="mojibake-filename-recovery",
        description=(
            "Windows -> Mac 転送で Shift-JIS が誤解釈され文字化けした"
            "ファイル名を検出・復旧する CLI ツール"
        ),
    )
    parser.add_argument(
        "paths",
        nargs="+",
        help="復旧対象のファイルまたはディレクトリのパス(ディレクトリは再帰処理される)",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="実際にはリネームせず、変更内容のみ表示する",
    )
    parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        help="変更されない項目も含めて詳細なログを出力する",
    )
    parser.add_argument(
        "--include-ascii",
        action="store_true",
        help="ASCII のみからなるファイル名も復旧対象に含める(通常は文字化けしないため対象外)",
    )
    return parser


def _maybe_rename(path: Path, *, include_ascii: bool, dry_run: bool, verbose: bool) -> bool:
    recovered = recover_name(path.name, include_ascii=include_ascii)
    if recovered is None:
        if verbose:
            print(f"SKIP  {path}")
        return False

    new_path = path.with_name(recovered)
    if new_path.exists():
        print(
            f"WARN  復旧後の名前が既に存在するためスキップします: {path} -> {new_path}",
            file=sys.stderr,
        )
        return False

    if dry_run:
        print(f"[dry-run] {path} -> {new_path}")
    else:
        path.rename(new_path)
        print(f"{path} -> {new_path}")
    return True


def process_path(path: Path, *, dry_run: bool, verbose: bool, include_ascii: bool) -> None:
    if path.is_dir():
        for dirpath, dirnames, filenames in os.walk(path, topdown=False):
            base = Path(dirpath)
            for name in filenames:
                _maybe_rename(
                    base / name, include_ascii=include_ascii, dry_run=dry_run, verbose=verbose
                )
            for name in dirnames:
                _maybe_rename(
                    base / name, include_ascii=include_ascii, dry_run=dry_run, verbose=verbose
                )

    _maybe_rename(path, include_ascii=include_ascii, dry_run=dry_run, verbose=verbose)


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)

    exit_code = 0
    for raw_path in args.paths:
        path = Path(raw_path)
        if not path.exists():
            print(f"ERROR: パスが見つかりません: {raw_path}", file=sys.stderr)
            exit_code = 1
            continue
        process_path(
            path,
            dry_run=args.dry_run,
            verbose=args.verbose,
            include_ascii=args.include_ascii,
        )

    return exit_code


if __name__ == "__main__":
    raise SystemExit(main())
