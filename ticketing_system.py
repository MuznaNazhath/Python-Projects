import json
import uuid
import os

# Ticketing system file paths
TICKET_FILE = "tickets.json"

# Function to load tickets from the JSON file
# If the file does not exist, it returns an empty list


def load_tickets():
    if not os.path.exists(TICKET_FILE):
        return []

    with open(TICKET_FILE, "r") as file:
        return json.load(file)


# Function to save tickets to the JSON file
# It overwrites the existing file with the updated list of tickets
def save_tickets(tickets):
    with open(TICKET_FILE, "w") as file:
        json.dump(tickets, file, indent=4)


# Function to create a new ticket
# It generates a unique ID for the ticket and saves it with the user's name and issue description
# The ticket status is set to "Open" by default
def create_ticket():
    name = input("Enter your name: ")
    issue = input("Describe the issue: ")
    ticket_id = str(uuid.uuid4())[:8]  # short unique ID for the ticket

    # Create a ticket dictionary
    # It contains the ticket ID, user's name, issue description, and status

    ticket = {
        "id": ticket_id,
        "name": name,
        "issue": issue,
        "status": "Open"
    }

    tickets = load_tickets()
    tickets.append(ticket)
    save_tickets(tickets)

    print(f"\n✅ Ticket created successfully! Ticket ID: {ticket_id}")


# Function to update the status of a ticket
# It searches for the ticket by ID and updates its status to "Resolved" or "Closed"
def view_tickets():
    tickets = load_tickets()
    if not tickets:
        print("\nNo tickets found.")
        return

    for t in tickets:
        print(f"\n🆔 ID: {t['id']}")
        print(f"👤 Name: {t['name']}")
        print(f"📋 Issue: {t['issue']}")
        print(f"📌 Status: {t['status']}")


# Function to close a ticket
# It searches for the ticket by ID and changes its status to "Closed"
# If the ticket is not found, it informs the user
def close_ticket():
    ticket_id = input("Enter ticket ID to close: ")
    tickets = load_tickets()
    found = False

    for t in tickets:
        if t["id"] == ticket_id:
            t["status"] = "Closed"
            found = True
            break

    if found:
        save_tickets(tickets)
        print("✅ Ticket closed.")
    else:
        print("❌ Ticket not found.")

# Main function to run the ticketing system
# It provides a simple text-based menu for the user to create, view, or close tickets


def main():
    while True:
        print("\n--- Simple Ticketing System ---")
        print("1. Create a new ticket")
        print("2. View all tickets")
        print("3. Close a ticket")
        print("4. Exit")

        choice = input("Choose an option (1-4): ")

        if choice == "1":
            create_ticket()
        elif choice == "2":
            view_tickets()
        elif choice == "3":
            close_ticket()
        elif choice == "4":
            print("👋 Goodbye!")
            break
        else:
            print("Invalid choice. Try again.")


if __name__ == "__main__":
    main()
