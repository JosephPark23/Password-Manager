# dependencies
import csv
import getpass

from cryptography.fernet import Fernet
import pbkdf2 as pb
import hashlib
import os, subprocess
from base64 import urlsafe_b64encode


# getting the salt, hash, and vault path
def get_information():
    # get the vault ID
    vault_id = input("Enter the unique vault ID: ")
    storage_path = f"{vault_id}.csv"

    # get the other vault information
    with open(storage_path, "r") as storagefile:
        contents = storagefile.read()

    return contents.split("\n")



def


def get_choice()