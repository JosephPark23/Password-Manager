# dependencies
import csv
import getpass

from cryptography.fernet import Fernet
import random
import hashlib
import os, subprocess
from os import system, name
from base64 import urlsafe_b64encode


class Vault:

    def __init__(self):
        self.master_password = ""
        self.derived_key = b''
        self.salt = b''
        self.vault_path = ""

        while True:
            self.vault_ID = random.randint(1000, 9999)
            if not os.path.exists(f"{self.vault_ID}.csv"):
                break
        self.storage_path = f"{self.vault_ID}.csv"

        if os.name == 'nt':
            subprocess.call(["attrib", "+H", self.storage_path])

    # clear the screen
    def clear(self):
        # windows
        if name == 'nt':
            _ = system('cls')
        # mac
        else:
            _ = system('clear')

    # create the vault file
    def create_data_file(self):
        # get vault path from user
        while True:
            self.vault_path = input("Enter the name of the new vault file: ") + ".csv"
            print(f"Vault file path: {self.vault_path}")
            if os.path.exists(self.vault_path):
                print("Error: File already exists. Choose a different name.")
            else:
                break

        # create a data template
        try:
            with open(self.vault_path, 'x', newline='') as csvfile:
                vault_writer = csv.writer(csvfile, delimiter=",", quotechar="|", )
                vault_writer.writerow(['Username', 'URL', 'Salt', 'Password'])
        except Exception as e:
            print(f"An error occurred while creating the vault file: {e}")

        # hide the file
        if os.name == 'nt':
            subprocess.call(["attrib", "+H", self.vault_path])

    # set the master password and derive a key from it
    def set_master_password(self):
        self.clear()
        # get master password from user
        while True:
            self.master_password = getpass.getpass("Enter your new master password: ")
            confirmation = getpass.getpass("Confirm your new master password: ")
            self.clear()
            if self.master_password == confirmation:
                break

        # derive key from password using pbkdf2
        self.salt = os.urandom(32)
        self.derived_key = urlsafe_b64encode(hashlib.pbkdf2_hmac('sha256', self.master_password.encode('utf-8'), self.salt, 100, 32))

        # Store the salt
        try:
            with open(self.vault_path, 'a', newline='') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(["Salt", "None", self.salt.hex(), ""])
        except Exception as e:
            print(f"An error occurred while storing the salt: {e}")

    # get the checksum and salt and store it
    def calculate_checksum(self, data):
        # generate hash from data
        checksum = hashlib.sha256(data).hexdigest()

        try:
            with open(self.storage_path, "x") as storagefile:
                writer = csv.writer(storagefile)
                writer.writerow([self.salt.hex(), checksum, self.vault_path, ""])
        except Exception as e:
            print(f"An error occurred while creating the storage file: {e}")

    # encrypt the vault's contents using pbkdf2
    def encrypt_vault_file(self):
        # read plaintext contents and encrypt using Fernet
        fernet = Fernet(self.derived_key)

        # get and encrypt the contents
        try:
            with open(self.vault_path, "rb") as csvfile:
                contents = csvfile.read()
                self.calculate_checksum(contents)

            encrypted_contents = fernet.encrypt(contents)

            # write the encrypted contents back into the file
            with open(self.vault_path, "wb") as csvfile:
                csvfile.write(encrypted_contents)
        except Exception as e:
            print(f"An exception occurred while writing the encrypted contents: {e}")

    def inform_user(self):
        print("The vault setup has been completed.\n"
              "===================================\n"
              f"Unique Vault ID: {self.vault_ID}\n"
              "===================================")

    # execute all the commands in sequence
    def execute_setup(self):
        self.create_data_file()
        self.set_master_password()
        self.encrypt_vault_file()
        self.inform_user()




