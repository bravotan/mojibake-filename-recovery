"""Shift-JIS 誤解釈によるファイル名の文字化けを検出・復旧するコアロジック。

典型的なパターン: Windows で Shift-JIS (cp932) エンコードされたファイル名が、
Mac 側のツールでバイト単位に latin-1 相当として文字列化されてしまい、
日本語部分が文字化けする。逆変換 (str -> latin-1 bytes -> cp932 str) を
試みることで元のファイル名を復元できる。
"""

from __future__ import annotations


def recover_name(name: str, include_ascii: bool = False) -> str | None:
    """文字化けしたファイル名の復旧を試みる。

    Args:
        name: 復旧を試みるファイル名(パスの最終要素)。
        include_ascii: True の場合、ASCII のみからなる名前にも復旧処理を試みる。

    Returns:
        復旧に成功し、かつ元の名前と異なる場合は復旧後の名前。
        文字化けと判定できない場合、または復旧結果が元の名前と同じ場合は None。
    """
    if not include_ascii and name.isascii():
        return None

    try:
        raw = name.encode("latin-1")
    except UnicodeEncodeError:
        return None

    try:
        recovered = raw.decode("cp932")
    except UnicodeDecodeError:
        return None

    if recovered == name:
        return None

    return recovered
