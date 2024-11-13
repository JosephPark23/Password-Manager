# dependencies
import csv
import getpass

from cryptography.fernet import Fernet
import random
import pbkdf2 as pb
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
        self.vault_ID = random.randint(1000, 9999)
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
        self.vault_path = input("Enter the name of the vault file: ") + ".csv"
        self.clear()

        # create a data template
        with open(self.vault_path, 'x', newline='') as csvfile:
            vault_writer = csv.writer(csvfile, delimiter=",", quotechar="|", )
            vault_writer.writerow(['The Vault'])
            vault_writer.writerow(['Username', 'URL', 'Salt', 'Password'])

        # hide the file
        if os.name == 'nt':
            subprocess.call(["attrib", "+H", self.vault_path])

    # set the master password and derive a key from it
    def set_master_password(self):
        # get master password from user
        while True:
            self.master_password = getpass.getpass("Enter your master password: ")
            confirmation = getpass.getpass("Confirm your master password: ")
            self.clear()
            if self.master_password == confirmation:
                break

        self.master_password = bytes(self.master_password, "utf-8")

        # derive key from password using pbkdf2
        self.salt = os.urandom(32)
        self.derived_key = urlsafe_b64encode(pb.pbkdf2(hashlib.sha256, self.master_password, self.salt, 20000, 32))

        # Store the salt
        with open(self.vault_path, 'a', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["Salt", "None", self.salt.hex(), ""])

    # get the checksum and salt and store it
    def calculate_checksum(self, data):
        # generate hash from data
        checksum = hashlib.sha256(data).hexdigest()

        with open(self.storage_path, "x") as storagefile:
            storagefile.write(self.salt.hex() + "\n")
            storagefile.write(checksum + "\n")
            storagefile.write(self.vault_path)

    # encrypt the vault's contents using pbkdf2
    def encrypt_vault_file(self):
        # read plaintext contents and en    crypt using Fernet
        fernet = Fernet(self.derived_key)

        # get and encrypt the contents
        with open(self.vault_path, "rb") as csvfile:
            contents = csvfile.read()
            self.calculate_checksum(contents)
        encrypted_contents = fernet.encrypt(contents)

        # write the encrypted contents back into the file
        with open(self.vault_path, "wb") as csvfile:
            csvfile.write(encrypted_contents)

    def inform_user(self):
        print("The vault setup has been completed.\n"
              "===================================\n"
              "Important details to remember:\n"
              f"Master Password: {self.master_password}"
              f"Unique Vault ID: {self.vault_ID}\n"
              "===================================")




