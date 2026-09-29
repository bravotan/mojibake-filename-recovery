from mojibake_filename_recovery.core import recover_name


def _mangle(name: str) -> str:
    """テスト用: Shift-JIS 誤解釈による文字化けを再現する。"""
    return name.encode("cp932").decode("latin-1")


def test_recovers_known_example():
    original = "新しいフォルダー"
    mangled = _mangle(original)
    assert mangled != original
    assert recover_name(mangled) == original


def test_ascii_name_skipped_by_default():
    assert recover_name("readme.txt") is None


def test_ascii_name_still_unchanged_with_include_ascii():
    assert recover_name("readme.txt", include_ascii=True) is None


def test_already_correct_japanese_name_is_untouched():
    assert recover_name("新しいフォルダー") is None


def test_non_mojibake_latin1_name_is_untouched():
    # é (U+00E9) は latin-1 にはエンコードできるが、単独では
    # 有効な Shift-JIS バイト列にならないため復旧対象にならない。
    assert recover_name("café") is None
