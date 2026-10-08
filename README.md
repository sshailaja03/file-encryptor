# File Encryptor

A focused command-line utility for encrypting and decrypting files with Python's Fernet authenticated-encryption implementation.

## Why this project

This project demonstrates practical security-oriented programming rather than only calling an encryption API. It handles key lifecycle, binary file I/O, command-line interfaces, validation, failure cases, and automated round-trip testing.

## What it demonstrates

- Authenticated symmetric encryption with Fernet
- Binary file handling with `pathlib`
- CLI design with `argparse`
- Key creation, loading, and validation
- Input/output path validation
- Explicit error handling for missing keys and invalid/corrupted data
- Automated tests for core encryption workflows

## Security model

A Fernet key is generated on the first encryption operation and stored at the configured key path. The key is ignored by Git and must be backed up securely.

> Losing the key makes encrypted files unrecoverable. Anyone who obtains both the encrypted file and its key can decrypt the data.

This is an educational utility, not an audited production security product.

## Architecture

```text
CLI arguments
     │
     ▼
Path validation
     │
     ├── Encrypt ──► Load/create Fernet key ──► Encrypt bytes ──► Output
     │
     └── Decrypt ──► Validate key ─────────────► Decrypt bytes ──► Output
```

## Setup

```bash
git clone https://github.com/sshailaja03/file-encryptor.git
cd file-encryptor
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

On Windows:

```text
.venv\Scripts\activate
```

## Usage

Encrypt a file:

```bash
python main.py encrypt document.txt document.encrypted
```

Decrypt it:

```bash
python main.py decrypt document.encrypted restored.txt
```

Use a custom key location:

```bash
python main.py encrypt document.txt document.encrypted --key-file keys/document.key
```

## Testing

Run the automated test suite with:

```bash
pytest
```

The tests cover:
- Encrypt → decrypt round trip
- Protection against using the same input/output path
- Missing-key failure handling

## Engineering decisions

### Fernet instead of implementing cryptography manually

The project uses the well-established Fernet implementation from the `cryptography` library rather than attempting to implement cryptographic primitives from scratch.

### Key validation

Keys are validated when loaded so malformed key files fail before encryption or decryption begins.

### Path safety

Input and output paths are checked to prevent accidental in-place operations. Output directories are created when necessary.

## Limitations

- The entire file is currently loaded into memory.
- Keys are stored as files and remain the user's responsibility to protect.
- Password-based key derivation is not implemented.
- The project has not been security audited.

## Future improvements

- Streaming encryption for large files
- Password-based key derivation with a salt
- Safer overwrite confirmation
- CI-based automated testing

---

**Shailaja Singh · Software Engineering Student · Python · Security Fundamentals**