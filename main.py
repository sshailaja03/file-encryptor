from cryptography.fernet import Fernet, InvalidToken
import argparse
from pathlib import Path

DEFAULT_KEY_FILE = Path("secret.key")


def get_or_create_key(key_file: Path) -> bytes:
    """Load an existing Fernet key or create it once."""
    if key_file.exists():
        return load_key(key_file)

    key_file.parent.mkdir(parents=True, exist_ok=True)
    key = Fernet.generate_key()
    key_file.write_bytes(key)
    return key


def load_key(key_file: Path) -> bytes:
    """Load and validate the Fernet key required for encryption/decryption."""
    if not key_file.is_file():
        raise FileNotFoundError(
            f"Key file '{key_file}' was not found. The original key is required."
        )

    key = key_file.read_bytes()
    try:
        Fernet(key)
    except (ValueError, TypeError) as exc:
        raise ValueError(f"Key file '{key_file}' is not a valid Fernet key.") from exc

    return key


def validate_paths(input_file: Path, output_file: Path) -> None:
    """Prevent accidental in-place encryption/decryption."""
    if input_file.resolve() == output_file.resolve():
        raise ValueError("Input and output files must be different.")


def encrypt_file(input_file: Path, output_file: Path, key_file: Path) -> None:
    if not input_file.is_file():
        raise FileNotFoundError(f"Input file '{input_file}' was not found.")

    validate_paths(input_file, output_file)
    key = get_or_create_key(key_file)
    output_file.parent.mkdir(parents=True, exist_ok=True)
    output_file.write_bytes(Fernet(key).encrypt(input_file.read_bytes()))
    print(f"Encrypted: {input_file} -> {output_file}")
    print(f"Key file: {key_file} (keep it private and backed up)")


def decrypt_file(input_file: Path, output_file: Path, key_file: Path) -> None:
    if not input_file.is_file():
        raise FileNotFoundError(f"Encrypted file '{input_file}' was not found.")

    validate_paths(input_file, output_file)
    key = load_key(key_file)

    try:
        decrypted = Fernet(key).decrypt(input_file.read_bytes())
    except InvalidToken as exc:
        raise ValueError("Decryption failed: wrong key or corrupted input.") from exc

    output_file.parent.mkdir(parents=True, exist_ok=True)
    output_file.write_bytes(decrypted)
    print(f"Decrypted: {input_file} -> {output_file}")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Encrypt or decrypt files with authenticated Fernet encryption."
    )
    parser.add_argument("mode", choices=("encrypt", "decrypt"))
    parser.add_argument("input", type=Path, help="Input file path")
    parser.add_argument("output", type=Path, help="Output file path")
    parser.add_argument(
        "--key-file",
        type=Path,
        default=DEFAULT_KEY_FILE,
        help="Key path (default: secret.key)",
    )
    args = parser.parse_args()

    try:
        if args.mode == "encrypt":
            encrypt_file(args.input, args.output, args.key_file)
        else:
            decrypt_file(args.input, args.output, args.key_file)
    except (FileNotFoundError, OSError, ValueError) as exc:
        parser.exit(1, f"error: {exc}\n")


if __name__ == "__main__":
    main()
