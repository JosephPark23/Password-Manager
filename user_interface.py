# dependencies
from access_vault import authenticate
from vault_setup import Vault


# getting the salt, hash, and vault path
def get_information():
    # get the vault ID
    vault_id = input("Enter the unique vault ID: ")
    storage_path = f"{vault_id}.csv"

    try:
        # get the other vault information
        with open(storage_path, "r") as storagefile:
            contents = storagefile.read()
    except Exception as e:
        print(f"Something went wrong. Check your information: {e}")

    contents = contents.split(",")

    return contents[:3]
# sets up new vault
def create_vault_():
    v = Vault()
    v.execute_setup()

# access and gets contents of the vault
def access_vault_():
    salt, checksum, vault_path = get_information()
    authenticate(vault_path, salt, checksum)

# main menu
def menu():

    actions = {
        "1": create_vault_,
        "2": access_vault_,
        "0": exit
    }

    while True:
        choice = input("Would you like to:\n"
                       "1) Create a new vault\n"
                       "2) Access an existing vault\n"
                       "Select a number that corresponds to your preferred choice: ").strip()

        if choice in actions:
            actions[choice]()
        else:
            print("Invalid input, please try again.")


if __name__ == "__main__":
    menu()

