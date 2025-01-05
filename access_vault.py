import hashlib
from base64 import urlsafe_b64encode

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
    clear()
    print("JIP Password Manager Access Portal\n")
    print("==================================\n")
    submitted_password = input("Enter the master password: ")

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
            continue

        fernet = Fernet(derived_key)

        try:
            decrypted_contents = fernet.decrypt(encrypted_contents)

        except Exception as e:
            print(f"Decryption went wrong. Check your information: {e}")
            continue

        calculated_checksum = hashlib.sha256(decrypted_contents).hexdigest()

        if calculated_checksum == stored_checksum:
            print_contents(decrypted_contents)
            break
        else:
            print("Incorrect password. Please try again.")


# print the decrypted contents
def print_contents(decrypted_contents):
    clear()
    print("\n============================================JIP PASSWORD MANAGER===========================================\n\n")
    reader = csv.reader(decrypted_contents.decode().splitlines())
    headers = next(reader)  # Skip headers

    print(f"{headers[0]:<20} {headers[1]:<30} {headers[2]:<15} {headers[3]:<20}")
    print("-" * 90)
    for row in reader:
        print(f"{row[0]:<20} {row[1]:<30} {row[2]:<15} {row[3]:<20}")

    input("\n\nPress the ENTER key to leave: ")
    clear()

