# dependencies
import cryptography
from cryptography.fernet import Fernet
import csv
import pbkdf2
import hashlib
import os

class Vault:

    def __init__(self):
        self.master_password = ""

    def create_data_file(self):
        with open('chase.csv', 'x', newline='') as csvfile:
            vault_writer = csv.writer(csvfile, delimiter=" ", quotechar="|", )
            vault_writer.writerow(['Username', 'URL', 'Salt', 'Password'])
        csvfile.close()

    def set_master_password(self):
        self.master_password = input("Enter your master password: ")


    def encrypt_vault_file(self):
        # generate a key
        key = Fernet.generate_key()
        fernet = Fernet(key)

        # read plaintext contents and encrypt using Fernet
        with open("chase.csv", "rb") as csvfile:
            contents = csvfile.read()
        encrypted_contents = fernet.encrypt(contents)

        # write the encrypted contents back into the file
        with open("chase.csv", "wb") as csvfile:
            csvfile.write(encrypted_contents)

        # save the key in a different file
        with open("way.key", "wb") as keyfile:
            keyfile.write(key)



