# File Encryptor

A small command-line utility that encrypts and decrypts files using Python's Fernet authenticated-encryption implementation.

## What it demonstrates

- Binary file handling
- Command-line argument parsing
- Symmetric authenticated encryption
- Key lifecycle and error handling
- Clear separation between encryption and decryption operations

## Security model

The program creates a Fernet key the first time encryption is requested and reuses that key for later operations. The key is never committed to Git.

> Losing the key makes encrypted files unrecoverable. Anyone who obtains both the encrypted file and its key can decrypt the data.

This is an educational utility, not an audited production security product.

## Setup

```bash
git clone https://github.com/sshailaja03/file-encryptor.git
cd file-encryptor
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

On Windows, activate the environment with `.venv\Scripts\activate`.

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

## Important limitations

- The whole file is read into memory.
- Key storage and backup remain the user's responsibility.
- The utility does not derive keys from passwords.
- Do not overwrite or publish `secret.key`.

## Future improvements

- Streaming encryption for large files
- Password-based key derivation with a salt
- Automated round-trip tests
- Safer overwrite confirmation
