import hashlib
from base64 import urlsafe_b64encode

import pbkdf2 as pb
from cryptography.fernet import Fernet
import csv
from os import system, name

# clear the screen
def clear():
    # windows
    if name == 'nt':
        _ = system('cls')
    # mac
    else:
        _ = system('clear')

# get the credentials from the user
def get_credentials(salt):
    submitted_password = input("Enter the master password: ")

    # convert to proper format
    b_submitted_password = bytes(submitted_password, "utf-8")
    b_submitted_salt = bytes(salt)

    return b_submitted_password, b_submitted_salt

# derive the key using the credentials
def derive_key(salt):
    # pbkdf2 to derive key
    master_password, salt = get_credentials(salt)
    derived_key = urlsafe_b64encode(pb.pbkdf2(hashlib.sha256, master_password, salt, 20000, 32))

    return derived_key, salt

# decrypt using file:
def authenticate(vault_path, salt, stored_checksum):
    derived_key, salt = derive_key(salt)

    with open(vault_path, "rb") as encrypted_file:
        encrypted_contents = encrypted_file.read()

    fernet = Fernet(derived_key)
    decrypted_contents = fernet.decrypt(encrypted_contents)
    calculated_checksum = hashlib.sha256(decrypted_contents).hexdigest()

    if calculated_checksum == stored_checksum:
        print_contents(decrypted_contents)
    else:
        print("Incorrect password. Please try again.")


# print the decrypted contents
def print_contents(decrypted_contents):
    print("\nVault Contents:\n================")
    reader = csv.reader(decrypted_contents.decode().splitlines())
    headers = next(reader)  # Skip headers
    print(f"{headers[0]:<20} {headers[1]:<30} {headers[2]:<15} {headers[3]:<20}")
    print("-" * 90)
    for row in reader:
        print(f"{row[0]:<20} {row[1]:<30} {row[2]:<15} {row[3]:<20}")


