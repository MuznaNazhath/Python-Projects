import tkinter as tk
from tkinter import ttk, messagebox
import json
import uuid
import os

TICKET_FILE = "tickets.json"

# Function to load tickets from the JSON file


def load_tickets():
    if not os.path.exists(TICKET_FILE):
        return []
    with open(TICKET_FILE, "r") as file:
        return json.load(file)


def save_tickets(tickets):
    with open(TICKET_FILE, "w") as file:
        json.dump(tickets, file, indent=4)


# main application class
class TicketApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("🎫 Simple Ticketing System")
        self.geometry("400x250")

        ttk.Style().theme_use("clam")

        ttk.Button(self, text="➕ Create Ticket",
                   command=self.open_add).pack(pady=10)
        ttk.Button(self, text="📋 View Tickets",
                   command=self.open_view).pack(pady=10)
        ttk.Button(self, text="✅ Close Ticket",
                   command=self.open_close).pack(pady=10)
        ttk.Button(self, text="❌ Exit", command=self.destroy).pack(pady=10)

# Function to add the tickets window
    def open_add(self):
        win = tk.Toplevel(self)
        win.title("Create Ticket")
        win.geometry("300x200")

        ttk.Label(win, text="Your Name:").pack()
        name = ttk.Entry(win)
        name.pack()

        ttk.Label(win, text="Describe Issue:").pack()
        issue = ttk.Entry(win)
        issue.pack()

        def submit():
            if not name.get() or not issue.get():
                messagebox.showwarning("Error", "Fill all fields")
                return

            ticket = {
                "id": str(uuid.uuid4())[:8],
                "name": name.get(),
                "issue": issue.get(),
                "status": "Open"
            }
            tickets = load_tickets()
            tickets.append(ticket)
            save_tickets(tickets)
            messagebox.showinfo("Success", f"Ticket ID: {ticket['id']}")
            win.destroy()

        ttk.Button(win, text="Submit", command=submit).pack(pady=10)


# Function to view tickets window

    def open_view(self):
        win = tk.Toplevel(self)
        win.title("View Tickets")
        win.geometry("500x300")

        cols = ("ID", "Name", "Issue", "Status")
        tree = ttk.Treeview(win, columns=cols, show="headings")

        for col in cols:
            tree.heading(col, text=col)
            tree.column(col, anchor=tk.CENTER, width=100)

        tickets = load_tickets()
        for t in tickets:
            tree.insert("", tk.END, values=(
                t["id"], t["name"], t["issue"], t["status"]))

        tree.pack(expand=True, fill="both")

# Function to close tickets window

    def open_close(self):
        win = tk.Toplevel(self)
        win.title("Close Ticket")
        win.geometry("300x150")

        ttk.Label(win, text="Enter Ticket ID:").pack()
        entry = ttk.Entry(win)
        entry.pack()

        def close_ticket():
            ticket_id = entry.get().strip()
            tickets = load_tickets()
            found = False

            for t in tickets:
                if t["id"] == ticket_id:
                    t["status"] = "Closed"
                    found = True
                    break

            if found:
                save_tickets(tickets)
                messagebox.showinfo("Success", "Ticket closed!")
                win.destroy()
            else:
                messagebox.showerror("Error", "Ticket not found.")

        ttk.Button(win, text="Close Ticket",
                   command=close_ticket).pack(pady=10)

# Run the application


if __name__ == "__main__":
    app = TicketApp()
    app.mainloop()
