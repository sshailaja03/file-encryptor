from pathlib import Path

import pytest

from main import decrypt_file, encrypt_file


def test_encrypt_and_decrypt_round_trip(tmp_path: Path):
    source = tmp_path / "source.txt"
    encrypted = tmp_path / "source.encrypted"
    restored = tmp_path / "restored.txt"
    key = tmp_path / "keys" / "test.key"

    original = b"recruiter-ready project test data"
    source.write_bytes(original)

    encrypt_file(source, encrypted, key)
    decrypt_file(encrypted, restored, key)

    assert encrypted.exists()
    assert restored.read_bytes() == original


def test_rejects_same_input_and_output(tmp_path: Path):
    source = tmp_path / "source.txt"
    source.write_text("hello")

    with pytest.raises(ValueError, match="must be different"):
        encrypt_file(source, source, tmp_path / "key")


def test_missing_key_fails_cleanly(tmp_path: Path):
    encrypted = tmp_path / "missing.encrypted"
    encrypted.write_bytes(b"not encrypted")

    with pytest.raises(FileNotFoundError):
        decrypt_file(encrypted, tmp_path / "restored.txt", tmp_path / "missing.key")
