import getpass
import hashlib
from base64 import urlsafe_b64encode

from cryptography.fernet import Fernet
from colors import bcolors as cr
import csv
from os import system, name
from time import sleep

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
    clear()
    print(f"{cr.HEADER}{cr.CYAN}JIP Password Manager Access Portal{cr.END}\n")
    print("==================================\n")
    submitted_password = getpass.getpass("Enter the master password: ")

    if isinstance(salt, str):
        salt = bytes.fromhex(salt)

    return submitted_password, salt

# derive the key using the credentials
def derive_key(salt): 
    # pbkdf2 to derive key
    master_password, salt = get_credentials(salt)

    derived_key = urlsafe_b64encode(hashlib.pbkdf2_hmac('sha256', master_password.encode('utf-8'), salt, 100, 32))

    return derived_key, salt

# decrypt using the information processed
def authenticate(vault_path, salt, stored_checksum):
    while True:
        derived_key, salt = derive_key(salt)

        try:
            with open(vault_path, "rb") as encrypted_file:
                encrypted_contents = encrypted_file.read()

        except Exception as e:
            print(f"Something went wrong. Check your information: {e}")
            sleep(2)
            clear()
            continue

        fernet = Fernet(derived_key)

        try:
            decrypted_contents = fernet.decrypt(encrypted_contents)

        except Exception as e:
            print(f"Decryption went wrong. Check your information: {e}")
            sleep(2)
            clear()
            continue

        calculated_checksum = hashlib.sha256(decrypted_contents).hexdigest()

        if calculated_checksum == stored_checksum:
            print_contents(decrypted_contents)
            break
        else:
            print("Incorrect password. Please try again.")
            sleep(2)
            clear()


# print the decrypted contents
def print_contents(decrypted_contents):
    clear()
    print(f"\n{cr.CYAN}============================================JIP PASSWORD MANAGER==========================================={cr.END}\n\n")
    reader = csv.reader(decrypted_contents.decode().splitlines())
    headers = next(reader)  # skip headers hehe

    print(f"{headers[0]:<20} {headers[1]:<30} {headers[2]:<15}")
    print("-" * 70)
    for row in reader:
        print(f"{row[0]:<20} {row[1]:<30} {row[2]:<15}")

    input("\n\nPress the ENTER key to leave: ")
    clear()
