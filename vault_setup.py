# dependencies
import csv
from cryptography.fernet import Fernet
import pbkdf2 as pb
import hashlib
import os


class Vault:

    def __init__(self):
        self.master_password = ""
        self.salt = b''

    def create_data_file(self):
        # create a data template
        with open('.chase/.csv', 'x', newline='') as csvfile:
            vault_writer = csv.writer(csvfile, delimiter=" ", quotechar="|", )
            vault_writer.writerow(['Username', 'URL', 'Salt', 'Password'])

    def set_master_password(self):
        # get master password from user
        self.master_password = input("Enter your master password: ")
        self.master_password = bytes(self.master_password, "utf-8")

        # derive key from password using pbkdf2
        self.salt = os.urandom(32)

        with open('.chase/.csv', 'a', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["Master Password", "None", self.salt, self.master_password])


    def encrypt_vault_file(self):
        # read plaintext contents and encrypt using Fernet
        fernet = Fernet(self.derived_key)

        with open(".chase/.csv", "rb") as csvfile:
            contents = csvfile.read()
        encrypted_contents = fernet.encrypt(contents)

        # write the encrypted contents back into the file
        with open(".chase/.csv", "wb") as csvfile:
            csvfile.write(encrypted_contents)

        # save the key in a different file
        with open("way.key", "wb") as keyfile:
            keyfile.write(self.derived_key)





