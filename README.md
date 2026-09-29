# mojibake-filename-recovery

Windows → Mac のファイル転送で、Shift-JIS のファイル名が UTF-8 として誤解釈され文字化けしてしまった場合に、元の日本語ファイル名を自動復旧する CLI ツールです。

## 背景

Windows で作成した ZIP アーカイブなどを Mac 側で展開すると、ファイル名のエンコーディングの扱いの違いから、日本語ファイル名が文字化けすることがあります。本ツールは、この文字化けパターンを検出し、元のファイル名に復旧します。

## 機能

- Shift-JIS 誤解釈の検出・復旧
- ディレクトリの再帰処理
- `argparse` ベースの CLI
- `--dry-run` / `--verbose` オプション

## 動作環境

- Python 3.x

## 使い方

```bash
python -m mojibake_filename_recovery <path> [--dry-run] [--verbose]
```

（インターフェースは開発が進むにつれて変更される可能性があります）

## 開発ロードマップ

1. CLI 実装
2. zip ファイル対応
3. PyPI パッケージ化

## ライセンス

未定
