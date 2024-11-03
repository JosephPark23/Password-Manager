# dependencies
import csv
from cryptography.fernet import Fernet
import pbkdf2 as pb
import hashlib
import os, subprocess
from base64 import urlsafe_b64encode


class Vault:

    def __init__(self, vault_path, salt_path):
        self.master_password = ""
        self.derived_key = b''
        self.salt = b''
        self.vault_path = vault_path
        self.salt_path = salt_path

    def create_data_file(self):
        # create a data template
        with open(self.vault_path, 'x', newline='') as csvfile:
            vault_writer = csv.writer(csvfile, delimiter=" ", quotechar="|", )
            vault_writer.writerow(['The Vault'])
            vault_writer.writerow(['Username', 'URL', 'Salt', 'Password'])

        # hide the file
        if os.name == 'nt':
            subprocess.call(["attrib", "+H", self.vault_path])

    # set the master password and derive a key from it
    def set_master_password(self):
        # get master password from user
        self.master_password = input("Enter your master password: ")
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

    # encrypt the vault's contents using pbkdf2
    def encrypt_vault_file(self):
        # read plaintext contents and encrypt using Fernet
        fernet = Fernet(self.derived_key)

        # get and encrypt the contents
        with open(self.vault_path, "rb") as csvfile:
            contents = csvfile.read()
        encrypted_contents = fernet.encrypt(contents)

        # write the encrypted contents back into the file
        with open(self.vault_path, "wb") as csvfile:
            csvfile.write(encrypted_contents)

    # get the checksum and store it
    def calculate_checksum(self):
        hasher = hashlib.sha256()
        with open(self.vault_path, 'rb') as file:
            while True:
                chunk = file.read(4096)
                if not chunk:
                    break
                hasher.update(chunk)
