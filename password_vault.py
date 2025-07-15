# password_vault.py
# └── Handles:
#     ├── Master password check
#     ├── Add new credentials
#     ├── Retrieve credentials
#     └── Encrypt/Decrypt data

from cryptography.fernet import Fernet

# function to create a master key
# This key is used to encrypt and decrypt the credentials
# It generates a new key and saves it to a file named "key.key"


def write_key():
    key = Fernet.generate_key()  # Generate a new key
    # Save the key to a file
    with open("key.key", "wb") as key_file:
        key_file.write(key)

# ----- RUN THIS ONLY ONCE -----
# write_key()

# Function to load the key from the file
# This key is used for encryption and decryption of credentials


def load_key():
    return open("key.key", "rb").read()


key = load_key()
fer = Fernet(key)

# Function to add a new credential to the vault
# It encrypts the password before saving it


def add():
    name = input("Account Name: ")
    user = input("Username: ")
    pwd = input("Password: ")

    with open("vault.txt", "a") as f:
        encrypted_pwd = fer.encrypt(pwd.encode()).decode()
        f.write(f"{name}|{user}|{encrypted_pwd}\n")


# Function to view credentials from the vault
# It decrypts the password before displaying it
def view():
    try:
        with open("vault.txt", "r") as f:
            for line in f:
                name, user, encrypted_pwd = line.strip().split("|")
                decrypted_pwd = fer.decrypt(encrypted_pwd.encode()).decode()
                print(f"{name} | {user} | {decrypted_pwd}")
    except FileNotFoundError:
        print("No passwords saved yet.")


# Main loop to interact with the user
# It allows the user to add new credentials or view existing ones
while True:
    mode = input(
        "\nWould you like to add a new password or view existing ones (add/view)? Press 'q' to quit: ").lower()

    if mode == "q":
        break
    elif mode == "add":
        add()
    elif mode == "view":
        view()
    else:
        print("Invalid choice.")
