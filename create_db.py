import sqlite3
import tkinter as tk
from tkinter import messagebox, ttk

# Function to connect to the database
def connect_db():
    return sqlite3.connect('vet_health_tracker.db')

# Function to create the database (if not already created)
def create_database():
    conn = sqlite3.connect('vet_health_tracker.db')
    cursor = conn.cursor()

    # Create pet table
    cursor.execute('''CREATE TABLE IF NOT EXISTS pets (
                        id INTEGER PRIMARY KEY,
                        name TEXT NOT NULL,
                        species TEXT NOT NULL,
                        age INTEGER,
                        health_status TEXT,
                        owner_name TEXT)''')

    # Create vaccination table
    cursor.execute('''CREATE TABLE IF NOT EXISTS vaccinations (
                        id INTEGER PRIMARY KEY,
                        pet_id INTEGER,
                        vaccine_name TEXT,
                        date DATE,
                        FOREIGN KEY(pet_id) REFERENCES pets(id))''')

    conn.commit()
    conn.close()

# Function to create the main window
def create_main_window():
    root = tk.Tk()
    root.title("Veterinary Health Tracker")
    root.geometry("600x400")  # Set the window size

    # Add Pet Button
    btn_add_pet = tk.Button(root, text="Add Pet", command=open_add_pet_window, width=20, height=2)
    btn_add_pet.pack(pady=20)

    # View Pets Button
    btn_view_pets = tk.Button(root, text="View Pets", command=view_pets, width=20, height=2)
    btn_view_pets.pack(pady=20)

    root.mainloop()

# Function to open Add Pet form
def open_add_pet_window():
    add_pet_window = tk.Toplevel()
    add_pet_window.title("Add Pet")
    add_pet_window.geometry("400x300")  # Set the window size

    # Create the form to add pet details
    label_name = tk.Label(add_pet_window, text="Pet Name:")
    label_name.grid(row=0, column=0, sticky="e", padx=10, pady=5)
    entry_name = tk.Entry(add_pet_window, width=30)
    entry_name.grid(row=0, column=1, padx=10, pady=5)

    label_species = tk.Label(add_pet_window, text="Species:")
    label_species.grid(row=1, column=0, sticky="e", padx=10, pady=5)
    entry_species = tk.Entry(add_pet_window, width=30)
    entry_species.grid(row=1, column=1, padx=10, pady=5)

    label_age = tk.Label(add_pet_window, text="Age:")
    label_age.grid(row=2, column=0, sticky="e", padx=10, pady=5)
    entry_age = tk.Entry(add_pet_window, width=30)
    entry_age.grid(row=2, column=1, padx=10, pady=5)

    label_health = tk.Label(add_pet_window, text="Health Status:")
    label_health.grid(row=3, column=0, sticky="e", padx=10, pady=5)
    entry_health = tk.Entry(add_pet_window, width=30)
    entry_health.grid(row=3, column=1, padx=10, pady=5)

    label_owner = tk.Label(add_pet_window, text="Owner Name:")
    label_owner.grid(row=4, column=0, sticky="e", padx=10, pady=5)
    entry_owner = tk.Entry(add_pet_window, width=30)
    entry_owner.grid(row=4, column=1, padx=10, pady=5)

    # Save Pet function
    def save_pet():
        name = entry_name.get()
        species = entry_species.get()
        age = entry_age.get()
        health = entry_health.get()
        owner = entry_owner.get()

        if not name or not species or not age or not health or not owner:
            messagebox.showwarning("Input Error", "All fields are required!")
            return

        # Insert pet data into the database
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute('''INSERT INTO pets (name, species, age, health_status, owner_name) 
                          VALUES (?, ?, ?, ?, ?)''', (name, species, age, health, owner))
        conn.commit()
        conn.close()

        messagebox.showinfo("Success", "Pet added successfully!")
        add_pet_window.destroy()  # Close the add pet window

    # Save Button
    btn_save_pet = tk.Button(add_pet_window, text="Save Pet", command=save_pet, width=20, height=2)
    btn_save_pet.grid(row=5, columnspan=2, pady=20)

# Function to view all pets with update and delete options
def view_pets():
    view_window = tk.Toplevel()
    view_window.title("View Pets")
    view_window.geometry("600x400")  # Set the window size

    # Create a frame for the list of pets with scroll bar
    frame = tk.Frame(view_window)
    frame.pack(pady=20, padx=20, fill="both", expand=True)

    # Create a vertical scrollbar
    canvas = tk.Canvas(frame)
    scrollbar = ttk.Scrollbar(frame, orient="vertical", command=canvas.yview)
    canvas.configure(yscrollcommand=scrollbar.set)

    # Add scroll bar to canvas
    scrollbar.pack(side="right", fill="y")
    canvas.pack(side="left", fill="both", expand=True)

    # Create another frame inside the canvas to hold pet info
    pet_frame = tk.Frame(canvas)
    canvas.create_window((0, 0), window=pet_frame, anchor="nw")

    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM pets")
    pets = cursor.fetchall()
    conn.close()

    if pets:
        for i, pet in enumerate(pets):
            pet_info = f"ID: {pet[0]} | Name: {pet[1]}, Species: {pet[2]}, Age: {pet[3]}, Health: {pet[4]}, Owner: {pet[5]}"

            # Create labels to display pet info
            label = tk.Label(pet_frame, text=pet_info, width=50, anchor="w")
            label.grid(row=i, column=0, sticky="w", padx=10, pady=5)

            # Update Button
            btn_update = tk.Button(pet_frame, text="Update", command=lambda pet_id=pet[0]: update_pet(pet_id), width=10)
            btn_update.grid(row=i, column=1, padx=10)

            # Delete Button
            btn_delete = tk.Button(pet_frame, text="Delete", command=lambda pet_id=pet[0]: delete_pet(pet_id), width=10)
            btn_delete.grid(row=i, column=2, padx=10)
    else:
        label = tk.Label(view_window, text="No pets found.")
        label.pack(pady=10)

    pet_frame.update_idletasks()
    canvas.config(scrollregion=canvas.bbox("all"))

# Function to update pet details and vaccination info
def update_pet(pet_id):
    update_window = tk.Toplevel()
    update_window.title("Update Pet")
    update_window.geometry("400x400")

    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM pets WHERE id=?", (pet_id,))
    pet = cursor.fetchone()
    conn.close()

    # Create the form with the current pet details
    label_name = tk.Label(update_window, text="Pet Name:")
    label_name.grid(row=0, column=0, sticky="e", padx=10, pady=5)
    entry_name = tk.Entry(update_window, width=30)
    entry_name.insert(0, pet[1])
    entry_name.grid(row=0, column=1, padx=10, pady=5)

    label_species = tk.Label(update_window, text="Species:")
    label_species.grid(row=1, column=0, sticky="e", padx=10, pady=5)
    entry_species = tk.Entry(update_window, width=30)
    entry_species.insert(0, pet[2])
    entry_species.grid(row=1, column=1, padx=10, pady=5)

    label_age = tk.Label(update_window, text="Age:")
    label_age.grid(row=2, column=0, sticky="e", padx=10, pady=5)
    entry_age = tk.Entry(update_window, width=30)
    entry_age.insert(0, pet[3])
    entry_age.grid(row=2, column=1, padx=10, pady=5)

    label_health = tk.Label(update_window, text="Health Status:")
    label_health.grid(row=3, column=0, sticky="e", padx=10, pady=5)
    entry_health = tk.Entry(update_window, width=30)
    entry_health.insert(0, pet[4])
    entry_health.grid(row=3, column=1, padx=10, pady=5)

    label_owner = tk.Label(update_window, text="Owner Name:")
    label_owner.grid(row=4, column=0, sticky="e", padx=10, pady=5)
    entry_owner = tk.Entry(update_window, width=30)
    entry_owner.insert(0, pet[5])
    entry_owner.grid(row=4, column=1, padx=10, pady=5)

    label_vaccination = tk.Label(update_window, text="Vaccination Details:")
    label_vaccination.grid(row=5, column=0, sticky="e", padx=10, pady=5)
    entry_vaccination = tk.Entry(update_window, width=30)
    entry_vaccination.insert(0, '')  # Leave this blank for now
    entry_vaccination.grid(row=5, column=1, padx=10, pady=5)

    # Save function to update pet details and vaccination info
    def save_updated_pet():
        name = entry_name.get()
        species = entry_species.get()
        age = entry_age.get()
        health = entry_health.get()
        owner = entry_owner.get()
        vaccination = entry_vaccination.get()

        if not name or not species or not age or not health or not owner:
            messagebox.showwarning("Input Error", "All fields are required!")
            return

        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute('''UPDATE pets SET name=?, species=?, age=?, health_status=?, owner_name=? WHERE id=?''',
                       (name, species, age, health, owner, pet_id))
        
        # Save vaccination details
        cursor.execute('''INSERT INTO vaccinations (pet_id, vaccine_name, date) VALUES (?, ?, ?)''', 
                       (pet_id, vaccination, '2024-11-24'))  # Use the current date or allow the user to input the date
        conn.commit()
        conn.close()

        messagebox.showinfo("Success", "Pet and vaccination details updated successfully!")
        update_window.destroy()

    # Save Button
    btn_save_pet = tk.Button(update_window, text="Save Changes", command=save_updated_pet, width=20, height=2)
    btn_save_pet.grid(row=6, columnspan=2, pady=20)

# Function to delete pet
def delete_pet(pet_id):
    confirm = messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this pet?")
    if confirm:
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM pets WHERE id=?", (pet_id,))
        conn.commit()
        conn.close()

        messagebox.showinfo("Success", "Pet deleted successfully!")
        view_pets()

# Create the database if not created
create_database()

# Start the main window
create_main_window()
