import tkinter as tk
from tkinter import ttk
from typing import Any

class ExpenseTracker:
    def __init__(self, root):
        self.root = root
        self.root.title("Student Budget & Expense Tracker")
        self.root.geometry("800x550")
        self.root.minsize(750, 500)
        
        # State
        self.is_dark_mode = False
        self.expenses = [] # List of tuples (Description, Category, Amount)
        self.total_amount = 0.0
        self._feedback_timer = None
        
        # UI Attributes (initialized to None for type checker)
        self.header_frame: Any = None
        self.title_label: Any = None
        self.toggle_btn: Any = None
        self.input_frame: Any = None
        self.desc_entry: Any = None
        self.amount_entry: Any = None
        self.category_var: Any = None
        self.category_menu: Any = None
        self.add_btn: Any = None
        self.feedback_label: Any = None
        self.list_frame: Any = None
        self.tree: Any = None
        self.bottom_frame: Any = None
        self.total_label: Any = None
        self.delete_btn: Any = None
        self.style: Any = None
        
        # --- HCI Principle: Consistency & Standards (Color Palette) ---
        self.colors_light = {
            'bg': '#f4f6f8',
            'fg': '#333333',
            'entry_bg': '#ffffff',
            'list_bg': '#ffffff',
            'btn_bg': '#e0e0e0',
            'highlight': '#0056b3',
            'highlight_fg': '#ffffff',
            'error': '#d32f2f',
            'error_fg': '#ffffff',
            'success': '#388e3c'
        }
        self.colors_dark = {
            'bg': '#1e1e1e',
            'fg': '#e0e0e0',
            'entry_bg': '#2d2d2d',
            'list_bg': '#2d2d2d',
            'btn_bg': '#424242',
            'highlight': '#4dabf7',
            'highlight_fg': '#ffffff',
            'error': '#ff5252',
            'error_fg': '#ffffff',
            'success': '#69f0ae'
        }
        self.c = self.colors_light
        self.root.configure(bg=self.c['bg'])

        self.setup_ui()
        self.apply_theme()

    def setup_ui(self):
        # 1. Header Frame (Minimalist design)
        self.header_frame = tk.Frame(self.root)
        self.header_frame.pack(fill=tk.X, padx=20, pady=(20, 10))
        
        self.title_label = tk.Label(self.header_frame, text="Expense Tracker", font=("Poppins", 18, "bold"))
        self.title_label.pack(side=tk.LEFT)
        
        # --- Mandatory Feature: Dark Mode Toggle ---
        self.toggle_btn = tk.Button(self.header_frame, text="🌙 Dark Mode", command=self.toggle_dark_mode, 
                                    relief=tk.FLAT, font=("Poppins", 10, "bold"), padx=10, pady=5)
        self.toggle_btn.pack(side=tk.RIGHT)

        # 2. Input Frame
        self.input_frame = tk.Frame(self.root)
        self.input_frame.pack(fill=tk.X, padx=20, pady=10)
        
        # Input Fields using Grid Layout for organized structure
        self.input_frame.columnconfigure(1, weight=1, minsize=150) # Allow Description field to scale responsively
        
        tk.Label(self.input_frame, text="Description:", font=("Poppins", 11)).grid(row=0, column=0, sticky='w', padx=(0, 5), pady=5)
        self.desc_entry = tk.Entry(self.input_frame, font=("Poppins", 12), width=30)
        self.desc_entry.grid(row=0, column=1, padx=5, pady=5, sticky='ew')
        
        tk.Label(self.input_frame, text="Amount (GH₵):", font=("Poppins", 11)).grid(row=0, column=2, sticky='w', padx=10, pady=5)
        self.amount_entry = tk.Entry(self.input_frame, font=("Poppins", 12), width=10)
        self.amount_entry.grid(row=0, column=3, padx=5, pady=5)
        
        self.category_var = tk.StringVar()
        categories = ["Food", "Transport", "Study", "Fun", "Other"]
        self.category_menu = ttk.Combobox(self.input_frame, textvariable=self.category_var, values=categories, state="readonly", font=("Poppins", 11), width=10)
        self.category_menu.set("Food")
        self.category_menu.grid(row=0, column=4, padx=10, pady=5)
        
        self.add_btn = tk.Button(self.input_frame, text="Add Expense", command=self.add_expense, 
                                 font=("Poppins", 11, "bold"), relief=tk.FLAT, padx=10)
        self.add_btn.grid(row=0, column=5, padx=(10, 0), pady=5)

        # --- HCI Principle: Clear Feedback / Visibility of System Status ---
        self.feedback_label = tk.Label(self.root, text="Welcome! Ready to track expenses.", font=("Poppins", 10, "italic"))
        self.feedback_label.pack(fill=tk.X, padx=20, pady=(0, 10))

        # 3. List Area (HCI Principle: Recognition rather than recall)
        self.list_frame = tk.Frame(self.root)
        self.list_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=5)
        
        # Columns for Treeview (Tabular Data presentation)
        columns = ("desc", "category", "amount")
        self.tree = ttk.Treeview(self.list_frame, columns=columns, show="headings", selectmode="browse")
        self.tree.heading("desc", text="Description")
        self.tree.heading("category", text="Category")
        self.tree.heading("amount", text="Amount (GH₵)")
        
        self.tree.column("desc", width=250)
        self.tree.column("category", width=120, anchor=tk.CENTER)
        self.tree.column("amount", width=100, anchor=tk.E)
        
        # Scrollbar integration
        scrollbar = ttk.Scrollbar(self.list_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # 4. Bottom Frame (Total & Delete Actions)
        self.bottom_frame = tk.Frame(self.root)
        self.bottom_frame.pack(fill=tk.X, padx=20, pady=20)
        
        # --- HCI Principle: Visibility of system status (Running total) ---
        self.total_label = tk.Label(self.bottom_frame, text="Total: GH₵0.00", font=("Poppins", 16, "bold"))
        self.total_label.pack(side=tk.LEFT)
        
        # --- HCI Principle: User control and freedom (Delete function) ---
        self.delete_btn = tk.Button(self.bottom_frame, text="Delete Selected", command=self.delete_expense, 
                                    font=("Poppins", 11, "bold"), relief=tk.FLAT, padx=10, pady=5)
        self.delete_btn.pack(side=tk.RIGHT)

        # Style Treeview a bit
        self.style = ttk.Style()
        self.style.theme_use('clam')

    def apply_theme(self):
        """Update colors of widgets based on light/dark mode."""
        c = self.colors_dark if self.is_dark_mode else self.colors_light
        self.c = c
        
        # Backgrounds
        self.root.configure(bg=c['bg'])
        self.header_frame.configure(bg=c['bg'])
        self.input_frame.configure(bg=c['bg'])
        self.list_frame.configure(bg=c['bg'])
        self.bottom_frame.configure(bg=c['bg'])
        
        # Labels and specific widgets
        self.title_label.configure(bg=c['bg'], fg=c['fg'])
        self.toggle_btn.configure(bg=c['btn_bg'], fg=c['fg'], activebackground=c['btn_bg'], activeforeground=c['fg'])
        
        for child in self.input_frame.winfo_children():
            if isinstance(child, tk.Label):
                child.configure(bg=c['bg'], fg=c['fg'])
            elif isinstance(child, tk.Entry) and not isinstance(child, ttk.Combobox):
                child.configure(bg=c['entry_bg'], fg=c['fg'], insertbackground=c['fg'])

        # Accent Buttons
        self.add_btn.configure(bg=c['highlight'], fg=c['highlight_fg'], activebackground=c['highlight'], activeforeground=c['highlight_fg'])
        self.delete_btn.configure(bg=c['error'], fg=c['error_fg'], activebackground=c['error'], activeforeground=c['error_fg'])
        
        self.feedback_label.configure(bg=c['bg'], fg=c['fg'])
        self.total_label.configure(bg=c['bg'], fg=c['fg'])
        
        # Treeview and Combobox coloring
        self.style.configure("Treeview", 
                             background=c['list_bg'], 
                             fieldbackground=c['list_bg'], 
                             foreground=c['fg'],
                             font=("Poppins", 10),
                             rowheight=25)
        self.style.map('Treeview', background=[('selected', c['highlight'])], foreground=[('selected', c['highlight_fg'])])
        self.style.configure("Treeview.Heading", 
                             background=c['btn_bg'], 
                             foreground=c['fg'], 
                             font=("Poppins", 10, "bold"))
        
        # Configure Dropdown (Combobox) styles
        self.style.configure("TCombobox", 
                             fieldbackground=c['entry_bg'], 
                             background=c['btn_bg'], 
                             foreground=c['fg'],
                             selectbackground=c['highlight'],
                             selectforeground=c['highlight_fg'])
        
        # Ensure total color is correctly updated based on current value when theme changes
        self.update_total()


    def toggle_dark_mode(self):
        """Toggle the application theme between Light and Dark."""
        self.is_dark_mode = not self.is_dark_mode
        self.toggle_btn.config(text="☀️ Light Mode" if self.is_dark_mode else "🌙 Dark Mode")
        self.apply_theme()
        self.show_feedback("Theme updated.", "success")

    def show_feedback(self, message, msg_type="default"):
        """Displays temporary feedback messages to the user."""
        c = self.c
        color = c['fg']
        if msg_type == "error": color = c['error']
        elif msg_type == "success": color = c['success']
        
        self.feedback_label.config(text=message, fg=color)
        
        # Clear feedback after 3 seconds asynchronously
        if self._feedback_timer is not None:
            self.root.after_cancel(self._feedback_timer)
        self._feedback_timer = self.root.after(3000, lambda: self.feedback_label.config(text="", fg=c['fg']))

    def add_expense(self):
        """Adds a new expense item to the tracker."""
        desc = self.desc_entry.get().strip()
        amt_str = self.amount_entry.get().strip()
        cat = self.category_var.get()
        
        # --- HCI Principle: Error Prevention ---
        if not desc:
            self.show_feedback("Error: Description cannot be empty!", "error")
            return
            
        if not amt_str:
            self.show_feedback("Error: Amount cannot be empty!", "error")
            return
            
        try:
            amount = float(amt_str)
            if amount <= 0:
                self.show_feedback("Error: Amount must be greater than zero!", "error")
                return
        except ValueError:
            self.show_feedback("Error: Amount must be a valid number!", "error")
            return
            
        # Add to data list (No database needed per requirements)
        self.expenses.append((desc, cat, amount))
        
        # Add to UI treeview
        self.tree.insert("", tk.END, values=(desc, cat, f"{amount:.2f}"))
        
        self.update_total()
        
        # Reset inputs for next entry
        self.desc_entry.delete(0, tk.END)
        self.amount_entry.delete(0, tk.END)
        
        # --- HCI Principle: Clear feedback ---
        self.show_feedback(f"Expense '{desc}' added successfully!", "success")

    def delete_expense(self):
        """Deletes the selected expense item."""
        selected_item = self.tree.selection()
        if not selected_item:
            self.show_feedback("Please select an item to delete first.", "error")
            return
            
        for item in selected_item:
            values = self.tree.item(item, "values")
            desc, cat, amt_str = values
            
            # Remove from backend data list
            for i, exp in enumerate(self.expenses):
                # Match by value approximation
                if exp[0] == desc and exp[1] == cat and f"{exp[2]:.2f}" == amt_str:
                    self.expenses.pop(i)
                    break
                    
            # Remove from UI
            self.tree.delete(item)
            
        self.update_total()
        self.show_feedback("Expense item deleted.", "success")

    def update_total(self):
        """Updates the running total based on current expenses."""
        self.total_amount = sum(exp[2] for exp in self.expenses)
        
        # Color the total red if it gets over 1000 (just a cool little UI detail)
        self.total_label.config(text=f"Total: GH₵{self.total_amount:.2f}")
        
        if self.total_amount > 1000:
            self.total_label.config(fg=self.c['error'])
        else:
            self.total_label.config(fg=self.c['fg'])

if __name__ == "__main__":
    root = tk.Tk()
    app = ExpenseTracker(root)
    root.mainloop()
