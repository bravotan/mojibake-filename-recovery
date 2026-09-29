# mojibake-filename-recovery

Windows → Mac のファイル転送で、Shift-JIS のファイル名が UTF-8 として誤解釈され文字化けしてしまった場合に、元の日本語ファイル名を自動復旧する CLI ツールです。

## 背景

Windows で作成した ZIP アーカイブなどを Mac 側で展開すると、ファイル名のエンコーディングの扱いの違いから、日本語ファイル名が文字化けすることがあります。本ツールは、この文字化けパターンを検出し、元のファイル名に復旧します。

## 機能

- Shift-JIS 誤解釈の検出・復旧
- `-r` / `--recursive` によるディレクトリの再帰処理
- `argparse` ベースの CLI
- `--dry-run` / `--verbose` / `--include-ascii` オプション

## 動作環境

- Python 3.9+
- [uv](https://docs.astral.sh/uv/)

## インストール

`uv tool install` でコマンドとしてグローバルにインストールできます(PyPI 未登録のため、現時点では GitHub リポジトリまたはローカルパスを指定します)。

```bash
# GitHub リポジトリから直接インストール
uv tool install git+https://github.com/bravotan/mojibake-filename-recovery

# ローカルにクローン済みの場合
uv tool install .
```

アンインストールする場合:

```bash
uv tool uninstall mojibake-filename-recovery
```

PyPI 公開後(ロードマップの Phase 3)は `uv tool install mojibake-filename-recovery` でインストールできるようになる予定です。

## 使い方

`uv tool install` 済みの場合:

```bash
mojibake-filename-recovery <path> [-r] [--dry-run] [--verbose] [--include-ascii]
```

開発中のソースをそのまま実行する場合:

```bash
uv sync
uv run mojibake-filename-recovery <path> [-r] [--dry-run] [--verbose] [--include-ascii]
```

`<path>` がディレクトリの場合、`-r`/`--recursive` を付けないとディレクトリ自体の名前のみ復旧し、
中身のファイル・サブディレクトリは処理しません。中身も含めて復旧するには `-r` を付けてください。

（インターフェースは開発が進むにつれて変更される可能性があります）

## 開発ロードマップ

1. CLI 実装
2. zip ファイル対応
3. PyPI パッケージ化

## ライセンス

未定
