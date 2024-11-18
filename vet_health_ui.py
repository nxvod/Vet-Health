import sqlite3
import tkinter as tk
from tkinter import ttk, filedialog, messagebox

# Create the main window
root = tk.Tk()
root.title("Veterinary Health System")
root.geometry("800x600")
root.configure(bg="#f7f9fc")  # Light grayish blue background

# Style
style = ttk.Style()
style.theme_use("clam")  # Modern theme
style.configure(
    "TLabel", background="#f7f9fc", font=("Helvetica", 12), foreground="#2b3e50"
)
style.configure("TButton", font=("Helvetica", 10, "bold"), background="#2b3e50")
style.map("TButton", background=[("active", "#547aa5")])  # Button hover color

# Header
header = tk.Frame(root, bg="#2b3e50", height=80)
header.pack(fill="x", side="top")
header_label = tk.Label(
    header,
    text="Veterinary Health System",
    font=("Helvetica", 24, "bold"),
    bg="#2b3e50",
    fg="white",
)
header_label.pack(pady=20)

# Content Frame
content = tk.Frame(root, bg="#f7f9fc", padx=20, pady=20)
content.pack(expand=True, fill="both")

# Input Fields
tk.Label(content, text="Pet Name:", font=("Helvetica", 12), bg="#f7f9fc").grid(
    row=0, column=0, sticky="w", pady=10
)
pet_name_entry = ttk.Entry(content, width=40)
pet_name_entry.grid(row=0, column=1, pady=10)

tk.Label(content, text="Pet Age (Years):", font=("Helvetica", 12), bg="#f7f9fc").grid(
    row=1, column=0, sticky="w", pady=10
)
pet_age_entry = ttk.Entry(content, width=40)
pet_age_entry.grid(row=1, column=1, pady=10)

tk.Label(content, text="Owner's Name:", font=("Helvetica", 12), bg="#f7f9fc").grid(
    row=2, column=0, sticky="w", pady=10
)
owner_name_entry = ttk.Entry(content, width=40)
owner_name_entry.grid(row=2, column=1, pady=10)

# Dropdown for Pet Type
tk.Label(content, text="Pet Type:", font=("Helvetica", 12), bg="#f7f9fc").grid(
    row=3, column=0, sticky="w", pady=10
)
pet_type = ttk.Combobox(content, values=["Dog", "Cat", "Bird", "Other"], width=38)
pet_type.grid(row=3, column=1, pady=10)

# Upload Pet Image
tk.Label(content, text="Pet Image:", font=("Helvetica", 12), bg="#f7f9fc").grid(
    row=4, column=0, sticky="w", pady=10
)

image_path = tk.StringVar()

def upload_image():
    file_path = filedialog.askopenfilename(
        title="Select Image",
        filetypes=[("Image Files", "*.png;*.jpg;*.jpeg;*.gif")]
    )
    if file_path:
        image_path.set(file_path)
        messagebox.showinfo("Image Uploaded", f"Selected: {file_path}")

upload_btn = ttk.Button(content, text="Upload Image", command=upload_image)
upload_btn.grid(row=4, column=1, sticky="w", pady=10)

# Connect to the existing database
def connect_db():
    return sqlite3.connect("vet_health_app.db")  # Ensure the path matches your database file

# Submit Button - Insert data into the database
def insert_pet():
    pet_name = pet_name_entry.get()
    pet_age = pet_age_entry.get()
    owner_name = owner_name_entry.get()
    pet_type_val = pet_type.get()
    pet_image = image_path.get()

    if pet_name and pet_age and owner_name and pet_type_val:
        conn = connect_db()
        c = conn.cursor()
        c.execute("INSERT INTO pets (pet_name, pet_age, owner_name, pet_type, pet_image) VALUES (?, ?, ?, ?, ?)",
                  (pet_name, pet_age, owner_name, pet_type_val, pet_image))
        conn.commit()
        conn.close()
        messagebox.showinfo("Success", "Pet record added successfully!")
        clear_fields()
    else:
        messagebox.showerror("Error", "All fields are required!")

submit_btn = ttk.Button(content, text="Submit", command=insert_pet)
submit_btn.grid(row=5, column=1, pady=20, sticky="e")

# Clear Input Fields after submission
def clear_fields():
    pet_name_entry.delete(0, tk.END)
    pet_age_entry.delete(0, tk.END)
    owner_name_entry.delete(0, tk.END)
    pet_type.set('')
    image_path.set('')

# Footer
footer = tk.Frame(root, bg="#547aa5", height=30)
footer.pack(fill="x", side="bottom")
footer_label = tk.Label(
    footer,
    text="Veterinary Health System © 2024",
    font=("Helvetica", 10),
    bg="#547aa5",
    fg="white",
)
footer_label.pack(pady=5)

# Run the application
root.mainloop()
z