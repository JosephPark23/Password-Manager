import hashlib
from base64 import urlsafe_b64encode

import pbkdf2 as pb
from cryptography.fernet import Fernet


# get the credentials from the user
def get_credentials():
    submitted_password = input("Enter the master password: ")

    with open("salt.txt", "r") as saltfile:
        salt = saltfile.read().strip()

    # convert to proper format
    b_submitted_password = bytes(submitted_password, "utf-8")
    b_submitted_salt = bytes.fromhex(salt)

    return b_submitted_password, b_submitted_salt

# derive the key using the credentials
def derive_key():
    # pbkdf2 to derive key
    master_password, salt = get_credentials()
    derived_key = urlsafe_b64encode(pb.pbkdf2(hashlib.sha256, master_password, salt, 20000, 32))

    return derived_key, salt

# get the checksum of the decrypted file
def confirm_checksums(data):
    # generate hash from data
    checksum = hashlib.sha256(data).hexdigest()

    return checksum

# confirm password is correct
def authenticate():
    # decrypt the contents using the key
    derived_key, salt = derive_key()
    fernet = Fernet(derived_key)

    # decrypt the contents using the derived key
    with open("insert_vault_path_here", "rb") as vaultfile: # when the user interface is implemented the string will be replaced
        contents = vaultfile.read()
    decrypted_contents = fernet.decrypt(contents)

    # get the original hash
    with open("insert_hash_path_here", "rb") as hashfile:
        original_hash = hashfile.read()

    # authenticate
    if original_hash == confirm_checksums(decrypted_contents):
        return True


