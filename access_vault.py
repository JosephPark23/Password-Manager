from vault_setup import Vault
import csv
from cryptography.fernet import Fernet
import pbkdf2 as pb
import hashlib
import os, subprocess
from base64 import urlsafe_b64encode

# get the credentials from the user
def get_credentials():
    submitted_password = input("Enter the master password: ")
    with open("salt.txt", "r") as saltfile:
        salt = saltfile.read().strip()

    # convert to proper format
    b_submitted_password = bytes(submitted_password, "utf-8")
    b_submitted_salt = bytes.fromhex(salt)

    return b_submitted_password, b_submitted_salt

# derive the key using the credentials
def derive_key():
    # pbkdf2 to derive key
    master_password, salt = get_credentials()
    derived_key = urlsafe_b64encode(pb.pbkdf2(hashlib.sha256, master_password, salt, 20000, 32))

    return derived_key, salt

# confirm password is correct
def authenticate():
    # decrypt the contents using the key
    derived_key, salt = derive_key()
    fernet = Fernet(derived_key)

    with open("chase.csv", "rb") as vaultfile:
        contents = vaultfile.read()
    decrypted_contents = (fernet.decrypt(contents)).decode("utf-8")

    if decrypted_contents.find(salt.hex()):
        return True

def main():
    if authenticate():
        return True
