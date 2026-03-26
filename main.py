from cryptography.fernet import Fernet
import argparse
import os

# to decrypt a file this file is needed
KEY_FILE = "secret.key"


def generate_key():
    """Generate and save a Fernet key"""
    key = Fernet.generate_key()
    with open(KEY_FILE, "wb") as key_file:
        key_file.write(key)
    return key


def load_key():
    """Load the Fernet key from file"""
    if not os.path.exists(KEY_FILE):
        raise FileNotFoundError("Key file not found. Generate a key first.")
    return open(KEY_FILE, "rb").read()


def encrypt_file(input_file, output_file):
    key = generate_key()
    fernet = Fernet(key)

    with open(input_file, "rb") as file:
        data = file.read()

    encrypted = fernet.encrypt(data)

    with open(output_file, "wb") as file:
        file.write(encrypted)

    print(f"✅ File encrypted successfully")
    print(f"🔑 Key saved in {KEY_FILE}")


def decrypt_file(input_file, output_file):
    key = load_key()
    fernet = Fernet(key)

    with open(input_file, "rb") as file:
        encrypted_data = file.read()

    decrypted = fernet.decrypt(encrypted_data)

    with open(output_file, "wb") as file:
        file.write(decrypted)

    print("✅ File decrypted successfully")


def main():
    parser = argparse.ArgumentParser(description="Encrypt or decrypt a file using Fernet")
    parser.add_argument("mode", choices=["encrypt", "decrypt"], help="Mode: encrypt or decrypt")
    parser.add_argument("input", help="Input file path")
    parser.add_argument("output", help="Output file path")

    args = parser.parse_args()

    if args.mode == "encrypt":
        encrypt_file(args.input, args.output)
    else:
        decrypt_file(args.input, args.output)


if __name__ == "__main__":
    main()


