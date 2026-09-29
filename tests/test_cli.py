from mojibake_filename_recovery.cli import process_path


def _mangle(name: str) -> str:
    return name.encode("cp932").decode("latin-1")


def test_process_path_renames_file(tmp_path):
    original = "新しいファイル.txt"
    file_path = tmp_path / _mangle(original)
    file_path.write_text("data", encoding="utf-8")

    process_path(file_path, recursive=False, dry_run=False, verbose=False, include_ascii=False)

    assert not file_path.exists()
    assert (tmp_path / original).exists()


def test_process_path_dry_run_does_not_rename(tmp_path):
    original = "新しいファイル.txt"
    file_path = tmp_path / _mangle(original)
    file_path.write_text("data", encoding="utf-8")

    process_path(file_path, recursive=False, dry_run=True, verbose=False, include_ascii=False)

    assert file_path.exists()
    assert not (tmp_path / original).exists()


def test_process_path_recurses_into_directories_when_recursive(tmp_path):
    original_dir = "新しいフォルダー"
    original_file = "資料.txt"

    nested_dir = tmp_path / _mangle(original_dir)
    nested_dir.mkdir()
    (nested_dir / _mangle(original_file)).write_text("data", encoding="utf-8")

    process_path(tmp_path, recursive=True, dry_run=False, verbose=False, include_ascii=False)

    recovered_dir = tmp_path / original_dir
    assert recovered_dir.is_dir()
    assert (recovered_dir / original_file).exists()


def test_process_path_without_recursive_only_renames_directory_itself(tmp_path):
    original_dir = "新しいフォルダー"
    original_file = "資料.txt"
    mangled_file = _mangle(original_file)

    nested_dir = tmp_path / _mangle(original_dir)
    nested_dir.mkdir()
    (nested_dir / mangled_file).write_text("data", encoding="utf-8")

    process_path(nested_dir, recursive=False, dry_run=False, verbose=False, include_ascii=False)

    recovered_dir = tmp_path / original_dir
    assert recovered_dir.is_dir()
    # 中身は再帰処理していないため文字化けしたままのはず
    assert (recovered_dir / mangled_file).exists()
    assert not (recovered_dir / original_file).exists()
