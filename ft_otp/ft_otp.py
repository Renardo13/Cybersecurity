import argparse
import hmac
import hashlib
import sys
import os
from cryptography.fernet import Fernet

KEY_FILE = "ft_otp.key"
FERNET_FILE = "ft_otp.fernet"
COUNTER_FILE = "counter.txt"


#------------------------------------------- Counter update --------------------------------

def read_counter():
    if not os.path.exists(COUNTER_FILE):
        return 0 
    with open(COUNTER_FILE, "r") as f:
        return int(f.read().strip())
    
def write_counter(counter):
    with open(COUNTER_FILE, "w") as f:
        f.write(str(counter))


#------------------------------------------- Secret key manipulation --------------------------
def save_key(hex_key):
    
    # Cipher the key with a fernet key
    fernet_key = Fernet.generate_key()
    cipher = Fernet(fernet_key)
    encrypted = cipher.encrypt(hex_key.encode())
    # store also the cipher key for future encryption
    with open(KEY_FILE, "wb") as file:
        file.write(fernet_key + b"\n" + encrypted)
    print(f"Key saved successfully into {KEY_FILE}.")
    write_counter(0)
    
# Read cipher key and the secret key in ft_hotp.key
def load_key(file_path):
    with open(file_path, "rb") as f:
        lines = f.readlines()
        fernet_key = lines[0].strip()        # Fernet key
        encrypted_key = lines[1].strip()     # Cipher key
        cipher = Fernet(fernet_key)
        hex_key = cipher.decrypt(encrypted_key).decode()  # str key hex
        key_bytes = bytes.fromhex(hex_key)                # convert str key hex -> bytes to specifie the base from which has to be interpreted
        return key_bytes


#------------------------------------------- hotp algorithm --------------------------

def generate_hotp(key):
    counter = read_counter()

    counter_bytes = counter.to_bytes(8, byteorder="big")
    hmac_hash = hmac.new(key, counter_bytes, hashlib.sha1).digest()

    offset = hmac_hash[19] & 0x0F
    selected = hmac_hash[offset:offset+4]

    # 31 bits
    code_int = ((selected[0] & 0x7F) << 24) | (selected[1] << 16) | (selected[2] << 8) | selected[3]
    otp = code_int % 10**6
    
    write_counter(counter + 1)
    return otp

def parse():
    parser = argparse.ArgumentParser(description="HOTP Generator")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("-g", type=str)
    group.add_argument("-k", type=str)
    return parser.parse_args()

def main():
    args = parse()

    if args.g:
        key = args.g.strip()
        if not all(c in "0123456789abcdefABCDEF" for c in key):
            print("Error: key must be a hexadecimal string.")
            sys.exit(1)
        if len(key) != 32:
            print("Error: key must be exactly 32 hexadecimal characters (128 bits).")
            sys.exit(1)
        save_key(key)

    if args.k:
        if not os.path.exists(args.k):
            print(f"Error: {args.k} not found. Please generate a secret key first with -g.")
            sys.exit(1)

        key = load_key(args.k)
        otp = generate_hotp(key)
        print("Your HOTP is:", otp)

if __name__ == "__main__":
    main()