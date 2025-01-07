import hashlib
import getpass
import csv
import os

from cryptography.fernet import Fernet
from base64 import urlsafe_b64encode
from os import system, name
from colors import bcolors as cr
from time import sleep
from tempfile import NamedTemporaryFile

# clear the screen
def clear():
    # windows
    if name == 'nt':
        _ = system('cls')
    # mac
    else:
        _ = system('clear')


# get the credentials from the user
def get_credentials():
    print(f"{cr.HEADER}{cr.CYAN}JIP Password Manager Access Portal{cr.END}\n")
    print("==================================\n")
    submitted_password = getpass.getpass("Enter the master password: ")

    return submitted_password

# derive the key using the credentials
def derive_key(salt):
    # pbkdf2 to derive key
    master_password = get_credentials()

    if isinstance(salt, str):
        salt = bytes.fromhex(salt)

    derived_key = urlsafe_b64encode(hashlib.pbkdf2_hmac('sha256', master_password.encode('utf-8'), salt, 100, 32))

    return derived_key, salt

# confirm the user's credentials are valid
def unlock_vault(actual_salt, actual_checksum, vault_path):
    # derive the key and decrypt contents
    while True:
        derived_key, salt = derive_key(actual_salt)

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

        # confirm the key's contents are valid
        calculated_checksum = hashlib.sha256(decrypted_contents).hexdigest()

        if calculated_checksum == actual_checksum:
            return derived_key, True
        else:
            print("Incorrect password. Please try again.")

# get the information for the new password
def create_new_entry():
    print(f"{cr.HEADER}{cr.CYAN}============New Password Entry============\n{cr.END}")
    account = input("What is the new password for? (e.g. Instagram, Amazon, etc.): ")
    username = input("\nWhat is the username?: ")

    # confirm the password
    while True:
        password = getpass.getpass("\nEnter the new password you want to store: ")
        confirmation = getpass.getpass("Confirm the new password: ")

        if password == confirmation:
            print(f"\n{cr.GREEN}{cr.BOLD}Password successfully stored!{cr.END}")
            sleep(3)
            break

    return username, password, account

# store the new password
def add_entry(vault_path, derived_key):
    username, password, account = create_new_entry()
    new_entry = f"{account},{username},{password}\n"

    fernet = Fernet(derived_key)

    # decrypt whole file (try to fix) (what the hell is a redundancy anyway)
    try:
        with open(vault_path, "rb") as file:
            encrypted_contents = file.read()

        decrypted_contents = fernet.decrypt(encrypted_contents).decode("utf-8")

    except Exception as e:
        print(f"Error occurred during decryption: {e}")
        return

    # update the plaintext (yay)
    updated_contents = decrypted_contents + new_entry

    # encrypt AGAIN
    try:
        encrypted_updated_contents = fernet.encrypt(updated_contents.encode("utf-8"))

        with open(vault_path, "wb") as file:
            file.write(encrypted_updated_contents)

        print(f"New entry added: {username}")

    except Exception as e:
        sleep(2)
        clear()
        print(f"Exception occurred: {e}")

# get the new checksum
def get_new_checksum(vault_path, derived_key):

    while True:
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
            break

        except Exception as e:
            print(f"Decryption went wrong. Check your information: {e}")
            exit()

    # get the new checksum
    calculated_checksum = hashlib.sha256(decrypted_contents).hexdigest()

    return calculated_checksum

# temp file again
def create_temp_file(vault_id, new_contents):
    # create temporary file
    with NamedTemporaryFile(mode="wb", delete=False) as workspace:
        workspace.write(new_contents)
        temp_file_path = workspace.name

    # atomic replacement while preserving file location
    os.replace(temp_file_path, vault_id)


# updates checksum in the vault_ID file for further use.
def update_checksum(vault_id, vault_path, derived_key):
    try:
        with open(vault_id, 'r', newline='') as file:
            reader = csv.reader(file)
            rows = list(reader)

        # update checksum
        new_checksum = get_new_checksum(vault_path, derived_key)
        if len(rows) > 0:
            rows[0][1] = new_checksum
        else:
            print("Checksum update failed.")
            return

        # convert rows back to csv format
        updated_content = "\n".join([",".join(row) for row in rows]).encode()

        # write updated content back to the file
        create_temp_file(vault_id, updated_content)

    except Exception as e:
        print(f"Error while updating checksum: {e}")

# main workflow
def main(actual_salt, actual_checksum, vault_path, vault_id):
    clear()
    derived_key, authenticated = unlock_vault(actual_salt, actual_checksum, vault_path)
    if authenticated:
        clear()
        add_entry(vault_path, derived_key)
    clear()
    update_checksum(vault_id, vault_path, derived_key)
