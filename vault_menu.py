# dependencies
from view_vault import authenticate
from create_vault import Vault
from add_password import main
from os import system, name
from colors import bcolors as cr
from time import sleep
from pathlib import Path

# clear the screen
def clear():
    # windows
    if name == 'nt':
        _ = system('cls')
    # mac
    else:
        _ = system('clear')

# getting the salt, hash, and vault path
def get_information():
    # get the vault ID
    while True:
        try:
            vault_id = input("Enter the unique vault ID: ")
            home_dir = Path.home()
            storage_path = home_dir / f"{vault_id}.csv"

            # get the other vault information
            with open(storage_path, "r") as storage_file:
                contents = storage_file.read()

            break

        except Exception as e:
            print(f"Something went wrong. Check your information: {e}")
            sleep(3)
            clear()
            continue

    print(f"\n{cr.GREEN}{cr.BOLD}Vault found! Accessing...{cr.END}")
    sleep(2)
    contents = contents.split(",")

    return contents[:3] + [storage_path]

# sets up new vault
def create_vault_():
    clear()
    v = Vault()
    v.execute_setup()

# access and gets contents of the vault
def access_vault_():
    salt, checksum, vault_path, storage_path = get_information()
    authenticate(vault_path, salt, checksum)

# add a password
def add_password_():
    salt, checksum, vault_path, storage_path = get_information()
    main(salt, checksum, vault_path, storage_path)

# main menu
def menu():

    actions = {
        "1": create_vault_,
        "2": access_vault_,
        "3": add_password_,
        "4": exit
    }

    # Options
    while True:
        choice = input("Would you like to:\n"
                       "1) Create a new vault\n"
                       "2) Access an existing vault\n"
                       "3) Add a password\n"
                       "4) Exit the program\n\n"
                       "Enter the number that corresponds to your choice: ").strip()

        if choice in actions:
            actions[choice]()
        else:
            print("Invalid input, please try again.")
            sleep(2)
            clear()


if __name__ == "__main__":
    clear()
    print(f"{cr.BOLD}{cr.CYAN}Welcome to the JIP Secure Password Manager!{cr.END}\n")
    print("===========================================\n")
    menu()

