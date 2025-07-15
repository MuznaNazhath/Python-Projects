import os
import hashlib
import tkinter as tk
from tkinter import messagebox, simpledialog, ttk
from cryptography.fernet import Fernet

# ---------- encryption helpers ----------
KEY_FILE = "key.key"
VAULT_FILE = "vault.txt"
MASTER_FILE = "master.hash"


def write_key():
    key = Fernet.generate_key()
    with open(KEY_FILE, "wb") as f:
        f.write(key)


def load_key():
    if not os.path.exists(KEY_FILE):
        write_key()
    return open(KEY_FILE, "rb").read()


fer = Fernet(load_key())

# ---------- master‑password helpers ----------


def set_master_password():
    while True:
        pw1 = simpledialog.askstring("Set Master Password",
                                     "Create a master password:",
                                     show="*")
        if not pw1:
            continue
        pw2 = simpledialog.askstring("Confirm Password",
                                     "Re‑enter password:",
                                     show="*")
        if pw1 == pw2:
            with open(MASTER_FILE, "w") as f:
                f.write(hashlib.sha256(pw1.encode()).hexdigest())
            messagebox.showinfo("Success", "Master password set!")
            return True
        else:
            messagebox.showerror("Mismatch", "Passwords do not match.")


def verify_master_password():
    if not os.path.exists(MASTER_FILE):
        return set_master_password()

    stored_hash = open(MASTER_FILE).read().strip()
    attempt = simpledialog.askstring("Login",
                                     "Enter master password:",
                                     show="*")
    if attempt and hashlib.sha256(attempt.encode()).hexdigest() == stored_hash:
        return True
    messagebox.showerror("Error", "Incorrect master password.")
    return False

# ---------- vault actions ----------


def add_password(name, user, pwd):
    enc = fer.encrypt(pwd.encode()).decode()
    with open(VAULT_FILE, "a") as f:
        f.write(f"{name}|{user}|{enc}\n")


def read_passwords():
    items = []
    if not os.path.exists(VAULT_FILE):
        return items
    with open(VAULT_FILE) as f:
        for line in f:
            name, user, enc = line.strip().split("|")
            try:
                dec = fer.decrypt(enc.encode()).decode()
            except Exception:
                dec = "[Decryption error]"
            items.append((name, user, dec))
    return items

# ---------- GUI ----------


class VaultApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Secure Password Vault")
        self.geometry("300x150")
        ttk.Style().theme_use("clam")

        ttk.Button(self, text="Add Password",
                   command=self.open_add_window).pack(pady=10)
        ttk.Button(self, text="View Passwords",
                   command=self.open_view_window).pack(pady=10)
        ttk.Button(self, text="Quit", command=self.destroy).pack(pady=10)

    # ----- add window -----
    def open_add_window(self):
        add_win = tk.Toplevel(self)
        add_win.title("Add Credential")
        add_win.geometry("300x200")

        ttk.Label(add_win, text="Service").pack()
        svc_entry = ttk.Entry(add_win)
        svc_entry.pack()
        ttk.Label(add_win, text="Username").pack()
        usr_entry = ttk.Entry(add_win)
        usr_entry.pack()
        ttk.Label(add_win, text="Password").pack()
        pwd_entry = ttk.Entry(add_win, show="*")
        pwd_entry.pack()

        def save():
            svc, usr, pwd = (svc_entry.get(),
                             usr_entry.get(),
                             pwd_entry.get())
            if svc and usr and pwd:
                add_password(svc, usr, pwd)
                messagebox.showinfo("Saved", "Credential saved!")
                add_win.destroy()
            else:
                messagebox.showwarning("Input", "Please fill all fields.")

        ttk.Button(add_win, text="Save", command=save).pack(pady=10)

    # ----- view window -----
    def open_view_window(self):
        view_win = tk.Toplevel(self)
        view_win.title("Stored Credentials")
        view_win.geometry("400x300")

        cols = ("Service", "Username", "Password")
        tree = ttk.Treeview(view_win, columns=cols, show="headings")
        for c in cols:
            tree.heading(c, text=c)
            tree.column(c, anchor=tk.CENTER, width=120)
        tree.pack(expand=True, fill="both")

        for name, user, pwd in read_passwords():
            tree.insert("", tk.END, values=(name, user, pwd))


# ---------- main ----------
if __name__ == "__main__":
    if verify_master_password():
        app = VaultApp()
        app.mainloop()
