import os
import hashlib
from cryptography.fernet import Fernet

# ---------- KEY FUNCTIONS (unchanged) ----------


def write_key():
    key = Fernet.generate_key()
    with open("key.key", "wb") as key_file:
        key_file.write(key)

# Run below only once before using the vault or master password functionality
# write_key()

def load_key():
    return open("key.key", "rb").read()


key = load_key()
fer = Fernet(key)

# master password functionality
# -------------------------------------------------
# This section allows the user to set and verify a master password.
# The master password is stored as a SHA‑256 hash in a file named "master.hash".
# The user must enter the correct master password to access the vault.
MASTER_FILE = "master.hash"


def set_master_password():
    """Run once: ask user for a master password and save its SHA‑256 hash."""
    master = input("Create a master password: ").strip()
    hash_ = hashlib.sha256(master.encode()).hexdigest()
    with open(MASTER_FILE, "w") as f:
        f.write(hash_)
    print("Master password set!  🔐")

# run below only once to set the master password before using the vault
# set_master_password()


def verify_master_password():
    """Prompt for master password and compare to stored hash."""
    if not os.path.exists(MASTER_FILE):
        set_master_password()

    stored_hash = open(MASTER_FILE).read().strip()
    attempt = input("Enter master password: ").strip()
    return hashlib.sha256(attempt.encode()).hexdigest() == stored_hash
# -------------------------------------------------


def add():
    name = input("Account Name: ")
    user = input("Username: ")
    pwd = input("Password: ")

    with open("vault.txt", "a") as f:
        encrypted_pwd = fer.encrypt(pwd.encode()).decode()
        f.write(f"{name}|{user}|{encrypted_pwd}\n")


def view():
    try:
        with open("vault.txt", "r") as f:
            for line in f:
                name, user, encrypted_pwd = line.strip().split("|")
                try:
                    decrypted_pwd = fer.decrypt(
                        encrypted_pwd.encode()).decode()
                    print(f"{name} | {user} | {decrypted_pwd}")
                except Exception:
                    print(f"{name} | {user} | [Could not decrypt]")
    except FileNotFoundError:
        print("No passwords saved yet.")


# ---------- MAIN ----------
if not verify_master_password():
    print("❌  Incorrect master password. Exiting.")
    exit()

while True:
    mode = input("\n(add/view) or 'q' to quit: ").lower()
    if mode == "q":
        break
    elif mode == "add":
        add()
    elif mode == "view":
        view()
    else:
        print("Invalid choice.")
