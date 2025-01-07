# dependencies
import csv
import getpass

from cryptography.fernet import Fernet
import random
import hashlib
import os, subprocess
from os import system, name
from base64 import urlsafe_b64encode
from tempfile import NamedTemporaryFile
from time import sleep
from colors import bcolors as cr
from pathlib import Path

# clear the screen
def clear():
    # windows
    if name == 'nt':
        _ = system('cls')
    # mac
    else:
        _ = system('clear')


# creating the vault
class Vault:

    # initializing necessary variables
    def __init__(self):
        self.master_password = ""
        self.derived_key = b''
        self.salt = b''
        self.vault_path = ""

        # initialize unique Vault ID
        while True:
            self.vault_ID = random.randint(1000, 9999)
            if not os.path.exists(f"{self.vault_ID}.csv"):
                break

        home_dir = Path.home()
        self.storage_path = home_dir / f"{self.vault_ID}.csv"

    # create the vault file
    def create_data_file(self):
        print("=============Vault Setup=============\n")

        # name the vault filepath with user's choice
        while True:
            vault_name = input("Enter the name of the new vault file: ")
            home_dir = Path.home()
            self.vault_path = home_dir / f"{vault_name}.csv"

            if os.path.exists(self.vault_path):
                print("Error: File already exists. Choose a different name.")
                sleep(2)
                clear()
            else:
                break

        # initialize the user's vault filepath and create the template
        try:
            with open(self.vault_path, 'x', newline='') as csvfile:
                vault_writer = csv.writer(csvfile, delimiter=",", quotechar="|", )
                vault_writer.writerow(['Website/Account', 'Username', 'Password'])

        except Exception as e:
            print(f"An error occurred while creating the vault file: {e}")

        # hide the vault filepath
        if os.name == 'nt':
            subprocess.call(["attrib", "+H", self.vault_path])

    # set the master password and derive a key from it
    def set_master_password(self):
        # user creates and confirms their vault password
        while True:
            print("=======Create a Password=======\n")
            self.master_password = getpass.getpass("Enter your new master password: ")
            confirmation = getpass.getpass("Confirm your new master password: ")

            if self.master_password == confirmation:
                print(f"\n{cr.GREEN}{cr.BOLD}Password confirmed!{cr.END}")
                sleep(2)
                break

        # derive the key from password using pbkdf2 and generate a random salt
        self.salt = os.urandom(32)
        self.derived_key = urlsafe_b64encode(hashlib.pbkdf2_hmac('sha256', self.master_password.encode('utf-8'), self.salt, 100, 32))

    # get the checksum and salt and store it
    def calculate_checksum(self, data):
        # generate hash from data
        checksum = hashlib.sha256(data).hexdigest()

        try:
            with open(self.storage_path, "x") as storage_file:
                writer = csv.writer(storage_file)
                writer.writerow([self.salt.hex(), checksum, self.vault_path, ""])

            if os.name == 'nt':
                subprocess.call(["attrib", "+H", self.storage_path])

        except Exception as e:
            print(f"An error occurred while creating the storage file: {e}")

    # write encrypted contents using a temporary file
    def create_temp_file(self, encrypted_contents):
        # create temporary file
        with NamedTemporaryFile(mode="wb", delete=False) as workspace:
            workspace.write(encrypted_contents)
            temp_file_path = workspace.name

        # atomic replacement while preserving file location
        os.replace(temp_file_path, self.vault_path)

    # encrypt the vault's contents using pbkdf2
    def encrypt_vault_file(self):
        # read plaintext contents and encrypt using Fernet
        fernet = Fernet(self.derived_key)

        # get and encrypt the contents using Fernet
        try:
            with open(self.vault_path, "rb") as csvfile:
                contents = csvfile.read()
                self.calculate_checksum(contents)

            encrypted_contents = fernet.encrypt(contents)

            # write the encrypted contents back into the file
            self.create_temp_file(encrypted_contents)

        except Exception as e:
            print(f"An exception occurred while writing the encrypted contents: {e}")

    # ending message
    def inform_user(self):
        input(f"{cr.BOLD}The vault setup has been completed!{cr.END}\n\n"
              "===================================\n"
              f"{cr.CYAN}Unique Vault ID: {self.vault_ID}{cr.END}\n"
              f"{cr.CYAN}Vault Filepath: {self.vault_path}{cr.END}\n"
              "==================================="
              "\n\nPress the ENTER key to leave: ")
        clear()

    # execute all the commands in sequence
    def execute_setup(self):
        clear()
        self.create_data_file()
        clear()
        self.set_master_password()
        clear()
        self.encrypt_vault_file()
        self.inform_user()




