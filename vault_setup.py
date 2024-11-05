# dependencies
import csv
import getpass

from cryptography.fernet import Fernet
import pbkdf2 as pb
import hashlib
import os, subprocess
from os import system, name
from base64 import urlsafe_b64encode


class Vault:

    def __init__(self, vault_path, salt_path, hash_path):
        self.master_password = ""
        self.derived_key = b''
        self.salt = b''
        self.vault_path = vault_path
        self.salt_path = salt_path
        self.hash_path = hash_path

    def clear(self):
        # windows
        if name == 'nt':
            _ = system('cls')
        # mac
        else:
            _ = system('clear')

    # create the vault file
    def create_data_file(self):
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
            if self.master_password == confirmation:
                self.clear()
                break

        self.master_password = bytes(self.master_password, "utf-8")

        # derive key from password using pbkdf2
        self.salt = os.urandom(32)
        self.derived_key = urlsafe_b64encode(pb.pbkdf2(hashlib.sha256, self.master_password, self.salt, 20000, 32))

        # Store the salt
        with open(self.vault_path, 'a', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["Salt", "None", self.salt.hex(), ""])

        with open(self.salt_path, 'x', newline='') as saltfile:
            saltfile.write(self.salt.hex())

        if os.name == 'nt':
            subprocess.call(["attrib", "+H", self.salt_path])

    # get the checksum and store it
    def calculate_checksum(self, data):
        # generate hash from data
        checksum = hashlib.sha256(data).hexdigest()

        with open(self.hash_path, "x") as hashfile:
            hashfile.write(checksum)

        if os.name == 'nt':
            subprocess.call(["attrib", "+H", self.hash_path])

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



