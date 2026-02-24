import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
from datetime import datetime
import json
import os

DATA_FILE = "blood_data.json"

class BloodManagementSystem:
    def __init__(self):
        self.blood_inventory = {}
        self.donation_records = []
        self._load_data()

    def _load_data(self):
        """Load inventory and records from JSON file if it exists."""
        if os.path.exists(DATA_FILE):
            try:
                with open(DATA_FILE, "r") as f:
                    data = json.load(f)
                self.blood_inventory = data.get("blood_inventory", {})
                self.donation_records = data.get("donation_records", [])
            except (json.JSONDecodeError, IOError):
                self.blood_inventory = {}
                self.donation_records = []

    def _save_data(self):
        """Save inventory and records to JSON file."""
        data = {
            "blood_inventory": self.blood_inventory,
            "donation_records": self.donation_records
        }
        with open(DATA_FILE, "w") as f:
            json.dump(data, f, indent=4)

    def add_blood(self, blood_type, units, donor_name="Anonymous"):
        if blood_type not in ["A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"]:
            return False, "Invalid blood type"
        
        if units <= 0:
            return False, "Units must be greater than 0"
        
        if blood_type not in self.blood_inventory:
            self.blood_inventory[blood_type] = 0
        
        self.blood_inventory[blood_type] += units
        
        record = {
            "blood_type": blood_type,
            "units": units,
            "donor_name": donor_name,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "type": "donation"
        }
        self.donation_records.append(record)
        self._save_data()
        
        return True, f"Successfully added {units} units of {blood_type}"
    
    def remove_blood(self, blood_type, units, recipient_name="Anonymous"):
        if blood_type not in self.blood_inventory:
            return False, f"Blood type {blood_type} not available"
        
        if units <= 0:
            return False, "Units must be greater than 0"
        
        if self.blood_inventory[blood_type] < units:
            return False, f"Insufficient stock. Available: {self.blood_inventory[blood_type]} units"
        
        self.blood_inventory[blood_type] -= units
        
        record = {
            "blood_type": blood_type,
            "units": units,
            "recipient_name": recipient_name,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "type": "usage"
        }
        self.donation_records.append(record)
        self._save_data()
        
        return True, f"Successfully removed {units} units of {blood_type}"
    
    def delete_blood_type(self, blood_type):
        if blood_type not in self.blood_inventory:
            return False, f"Blood type {blood_type} not found"
        
        units = self.blood_inventory[blood_type]
        del self.blood_inventory[blood_type]
        self._save_data()
        return True, f"Deleted {blood_type} ({units} units removed)"
    
    def get_inventory(self):
        return self.blood_inventory
    
    def get_records(self):
        return self.donation_records


class BloodManagementUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Blood Management System")
        self.root.geometry("900x650")
        self.root.configure(bg="#f2c5c5")
        
        self.bms = BloodManagementSystem()
        
        # Header
        header_frame = tk.Frame(root, bg="#8B0000", height=80)
        header_frame.pack(fill=tk.X)
        header_frame.pack_propagate(False)
        
        title_label = tk.Label(header_frame, text="🩸 BLOOD MANAGEMENT SYSTEM", 
                              font=("Arial", 24, "bold"), bg="#8B0000", fg="white")
        title_label.pack(pady=20)
        
        # Main container
        main_frame = tk.Frame(root, bg="#f0f0f0")
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Left Panel - Operations
        left_frame = tk.LabelFrame(main_frame, text="Operations", font=("Arial", 12, "bold"),
                                   bg="white", padx=15, pady=15)
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
        
        # Add Blood Section
        add_frame = tk.LabelFrame(left_frame, text="Add Blood", font=("Arial", 10, "bold"),
                                 bg="white", padx=10, pady=10)
        add_frame.pack(fill=tk.X, pady=(0, 15))
        
        tk.Label(add_frame, text="Blood Type:", bg="white").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.add_blood_type = ttk.Combobox(add_frame, values=["A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"], 
                                          state="readonly", width=10)
        self.add_blood_type.grid(row=0, column=1, pady=5, padx=5)
        self.add_blood_type.current(0)
        
        tk.Label(add_frame, text="Units:", bg="white").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.add_units = tk.Entry(add_frame, width=12)
        self.add_units.grid(row=1, column=1, pady=5, padx=5)
        
        tk.Label(add_frame, text="Donor Name:", bg="white").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.donor_name = tk.Entry(add_frame, width=12)
        self.donor_name.grid(row=2, column=1, pady=5, padx=5)
        
        tk.Button(add_frame, text="Add Blood", command=self.add_blood, 
                 bg="#28a745", fg="white", font=("Arial", 10, "bold"), 
                 cursor="hand2").grid(row=3, column=0, columnspan=2, pady=10, sticky=tk.EW)
        
        # Remove Blood Section
        remove_frame = tk.LabelFrame(left_frame, text="Remove Blood", font=("Arial", 10, "bold"),
                                    bg="white", padx=10, pady=10)
        remove_frame.pack(fill=tk.X, pady=(0, 15))
        
        tk.Label(remove_frame, text="Blood Type:", bg="white").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.remove_blood_type = ttk.Combobox(remove_frame, values=["A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"], 
                                             state="readonly", width=10)
        self.remove_blood_type.grid(row=0, column=1, pady=5, padx=5)
        self.remove_blood_type.current(0)
        
        tk.Label(remove_frame, text="Units:", bg="white").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.remove_units = tk.Entry(remove_frame, width=12)
        self.remove_units.grid(row=1, column=1, pady=5, padx=5)
        
        tk.Label(remove_frame, text="Recipient:", bg="white").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.recipient_name = tk.Entry(remove_frame, width=12)
        self.recipient_name.grid(row=2, column=1, pady=5, padx=5)
        
        tk.Button(remove_frame, text="Remove Blood", command=self.remove_blood, 
                 bg="#dc3545", fg="white", font=("Arial", 10, "bold"), 
                 cursor="hand2").grid(row=3, column=0, columnspan=2, pady=10, sticky=tk.EW)
        
        # Delete Blood Type Section
        delete_frame = tk.LabelFrame(left_frame, text="Delete Blood Type", font=("Arial", 10, "bold"),
                                    bg="white", padx=10, pady=10)
        delete_frame.pack(fill=tk.X)
        
        tk.Label(delete_frame, text="Blood Type:", bg="white").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.delete_blood_type = ttk.Combobox(delete_frame, values=["A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"], 
                                             state="readonly", width=10)
        self.delete_blood_type.grid(row=0, column=1, pady=5, padx=5)
        self.delete_blood_type.current(0)
        
        tk.Button(delete_frame, text="Delete Type", command=self.delete_blood, 
                 bg="#ffc107", fg="black", font=("Arial", 10, "bold"), 
                 cursor="hand2").grid(row=1, column=0, columnspan=2, pady=10, sticky=tk.EW)
        
        # Right Panel - Display
        right_frame = tk.Frame(main_frame, bg="#f0f0f0")
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        # Inventory Display
        inventory_frame = tk.LabelFrame(right_frame, text="Blood Inventory", font=("Arial", 12, "bold"),
                                       bg="white", padx=10, pady=10)
        inventory_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        # Create Treeview for inventory
        columns = ("Blood Type", "Units", "Status")
        self.inventory_tree = ttk.Treeview(inventory_frame, columns=columns, show="headings", height=8)
        
        for col in columns:
            self.inventory_tree.heading(col, text=col)
            self.inventory_tree.column(col, width=100, anchor=tk.CENTER)
        
        self.inventory_tree.pack(fill=tk.BOTH, expand=True, pady=5)
        
        # Records Display
        records_frame = tk.LabelFrame(right_frame, text="Recent Records", font=("Arial", 12, "bold"),
                                     bg="white", padx=10, pady=10)
        records_frame.pack(fill=tk.BOTH, expand=True)
        
        self.records_text = scrolledtext.ScrolledText(records_frame, height=10, wrap=tk.WORD,
                                                     font=("Courier", 9))
        self.records_text.pack(fill=tk.BOTH, expand=True, pady=5)
        
        # Refresh Button
        tk.Button(right_frame, text="🔄 Refresh Display", command=self.refresh_display,
                 bg="#17a2b8", fg="white", font=("Arial", 11, "bold"),
                 cursor="hand2").pack(pady=10, fill=tk.X)
        
        # Initial display
        self.refresh_display()
    
    def add_blood(self):
        try:
            blood_type = self.add_blood_type.get()
            units = int(self.add_units.get())
            donor = self.donor_name.get().strip() or "Anonymous"
            
            success, message = self.bms.add_blood(blood_type, units, donor)
            
            if success:
                messagebox.showinfo("Success", message)
                self.add_units.delete(0, tk.END)
                self.donor_name.delete(0, tk.END)
                self.refresh_display()
            else:
                messagebox.showerror("Error", message)
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid number for units")
    
    def remove_blood(self):
        try:
            blood_type = self.remove_blood_type.get()
            units = int(self.remove_units.get())
            recipient = self.recipient_name.get().strip() or "Anonymous"
            
            success, message = self.bms.remove_blood(blood_type, units, recipient)
            
            if success:
                messagebox.showinfo("Success", message)
                self.remove_units.delete(0, tk.END)
                self.recipient_name.delete(0, tk.END)
                self.refresh_display()
            else:
                messagebox.showerror("Error", message)
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid number for units")
    
    def delete_blood(self):
        blood_type = self.delete_blood_type.get()
        
        if messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete {blood_type}?"):
            success, message = self.bms.delete_blood_type(blood_type)
            
            if success:
                messagebox.showinfo("Success", message)
                self.refresh_display()
            else:
                messagebox.showerror("Error", message)
    
    def refresh_display(self):
        # Update inventory tree
        for item in self.inventory_tree.get_children():
            self.inventory_tree.delete(item)
        
        all_types = ["A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"]
        inventory = self.bms.get_inventory()
        
        for blood_type in all_types:
            units = inventory.get(blood_type, 0)
            status = "LOW" if units < 10 else "OK"
            
            self.inventory_tree.insert("", tk.END, values=(blood_type, units, status),
                                      tags=(status,))
        
        # Color coding
        self.inventory_tree.tag_configure("LOW", background="#ffcccc")
        self.inventory_tree.tag_configure("OK", background="#ccffcc")
        
        # Update records
        self.records_text.delete(1.0, tk.END)
        records = self.bms.get_records()
        
        if records:
            self.records_text.insert(tk.END, "═" * 60 + "\n")
            for record in reversed(records[-10:]):
                self.records_text.insert(tk.END, f"Type: {record['type'].upper()}\n")
                self.records_text.insert(tk.END, f"Blood: {record['blood_type']} | Units: {record['units']}\n")
                if record['type'] == 'donation':
                    self.records_text.insert(tk.END, f"Donor: {record['donor_name']}\n")
                else:
                    self.records_text.insert(tk.END, f"Recipient: {record['recipient_name']}\n")
                self.records_text.insert(tk.END, f"Time: {record['timestamp']}\n")
                self.records_text.insert(tk.END, "─" * 60 + "\n")
        else:
            self.records_text.insert(tk.END, "No records available yet.\n")


def main():
    root = tk.Tk()
    app = BloodManagementUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()