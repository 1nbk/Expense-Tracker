import tkinter as tk
from tkinter import ttk
import customtkinter as ctk
from typing import Any
from datetime import datetime

# Configure CustomTkinter
ctk.set_appearance_mode("light")  # Default mode
ctk.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"

class ExpenseTracker(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Student Budget & Expense Tracker")
        self.geometry("1000x700")
        self.minsize(950, 650)
        
        # State
        self.expenses = [] # List of tuples (Date/Time, Description, Category, Amount)
        self.total_amount = 0.0
        self._feedback_timer = None
        self.budget_limit = 1000.0
        
        # Color Palette (Modern)
        self.colors = {
            "light": {
                "bg": "#F8FAFC",
                "card": "#FFFFFF",
                "text": "#1E293B",
                "accent": "#3B82F6",
                "success": "#10B981",
                "error": "#EF4444",
                "border": "#E2E8F0"
            },
            "dark": {
                "bg": "#0F172A",
                "card": "#1E293B",
                "text": "#F8FAFC",
                "accent": "#60A5FA",
                "success": "#34D399",
                "error": "#F87171",
                "border": "#334155"
            }
        }
        
        self.setup_ui()
        
    def setup_ui(self):
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)
        
        # 1. Header & Stats Section
        self.header_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.header_frame.grid(row=0, column=0, padx=30, pady=(30, 20), sticky="ew")
        self.header_frame.grid_columnconfigure(0, weight=1)
        
        self.title_label = ctk.CTkLabel(
            self.header_frame, 
            text="Student Expense Tracker", 
            font=("Poppins", 32, "bold")
        )
        self.title_label.grid(row=0, column=0, sticky="w")
        
        self.theme_toggle = ctk.CTkButton(
            self.header_frame, 
            text="🌙 Dark Mode", 
            width=140,
            height=40,
            corner_radius=20,
            command=self.toggle_theme,
            font=("Poppins", 13, "bold")
        )
        self.theme_toggle.grid(row=0, column=1, sticky="e")
        
        # 2. Stats Dashboard Cards
        self.stats_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.stats_frame.grid(row=1, column=0, padx=30, pady=(0, 20), sticky="ew")
        self.stats_frame.grid_columnconfigure((0, 1), weight=1)
        
        # Total Spent Card
        self.total_card = ctk.CTkFrame(self.stats_frame, corner_radius=15)
        self.total_card.grid(row=0, column=0, padx=(0, 15), sticky="ew")
        
        self.total_title = ctk.CTkLabel(self.total_card, text="Total Spent", font=("Poppins", 16))
        self.total_title.pack(pady=(15, 0))
        
        self.total_val_label = ctk.CTkLabel(self.total_card, text="GH₵ 0.00", font=("Poppins", 28, "bold"))
        self.total_val_label.pack(pady=(5, 15))
        
        # Budget Status Card
        self.status_card = ctk.CTkFrame(self.stats_frame, corner_radius=15)
        self.status_card.grid(row=0, column=1, padx=(15, 0), sticky="ew")
        
        self.status_title = ctk.CTkLabel(self.status_card, text="Budget Overview", font=("Poppins", 16))
        self.status_title.pack(pady=(15, 0))
        
        # Progress Bar Frame (to center the percentage next to it or below)
        self.prog_frame = ctk.CTkFrame(self.status_card, fg_color="transparent")
        self.prog_frame.pack(pady=(10, 0))
        
        self.progress_bar = ctk.CTkProgressBar(self.prog_frame, width=220, height=12)
        self.progress_bar.set(0)
        self.progress_bar.pack(side="left", padx=(0, 10))
        
        self.percentage_label = ctk.CTkLabel(self.prog_frame, text="0%", font=("Poppins", 14, "bold"))
        self.percentage_label.pack(side="left")
        
        self.status_text = ctk.CTkLabel(self.status_card, text="Safe (Limit: GH₵ 1000)", font=("Poppins", 13, "italic"))
        self.status_text.pack(pady=(5, 15))
        
        # 3. Content Area (Form and Table)
        self.content_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.content_frame.grid(row=2, column=0, padx=30, pady=0, sticky="nsew")
        self.content_frame.grid_columnconfigure(0, weight=1)
        self.content_frame.grid_rowconfigure(2, weight=1) # The list card
        
        # --- Input Card ---
        self.input_card = ctk.CTkFrame(self.content_frame, corner_radius=15)
        self.input_card.grid(row=0, column=0, pady=(0, 20), sticky="ew")
        self.input_card.grid_columnconfigure((0, 1, 2, 3), weight=1)
        
        # Row 0: Labels
        ctk.CTkLabel(self.input_card, text="Item Description:", font=("Poppins", 14, "bold")).grid(row=0, column=0, padx=(20, 10), pady=(15, 0), sticky="w")
        ctk.CTkLabel(self.input_card, text="Amount (GH₵):", font=("Poppins", 14, "bold")).grid(row=0, column=1, padx=10, pady=(15, 0), sticky="w")
        ctk.CTkLabel(self.input_card, text="Category:", font=("Poppins", 14, "bold")).grid(row=0, column=2, padx=10, pady=(15, 0), sticky="w")
        
        # Row 1: Input Fields
        self.desc_entry = ctk.CTkEntry(self.input_card, placeholder_text="e.g. Lunch", height=45, font=("Poppins", 14))
        self.desc_entry.grid(row=1, column=0, padx=(20, 10), pady=(5, 20), sticky="ew")
        
        self.amount_entry = ctk.CTkEntry(self.input_card, placeholder_text="0.00", height=45, font=("Poppins", 14))
        self.amount_entry.grid(row=1, column=1, padx=10, pady=(5, 20), sticky="ew")
        
        self.category_var = tk.StringVar(value="Food")
        self.category_menu = ctk.CTkComboBox(
            self.input_card, 
            values=["Food", "Transport", "Study", "Fun", "Other"],
            variable=self.category_var,
            height=45,
            font=("Poppins", 14)
        )
        self.category_menu.grid(row=1, column=2, padx=10, pady=(5, 20), sticky="ew")
        
        self.add_btn = ctk.CTkButton(
            self.input_card, 
            text="Add Expense", 
            command=self.add_expense,
            font=("Poppins", 14, "bold"),
            height=45,
            corner_radius=10
        )
        self.add_btn.grid(row=1, column=3, padx=(10, 20), pady=(5, 20), sticky="ew")
        
        # --- List Card ---
        self.list_card = ctk.CTkFrame(self.content_frame, corner_radius=15)
        self.list_card.grid(row=2, column=0, sticky="nsew")
        self.list_card.grid_columnconfigure(0, weight=1)
        self.list_card.grid_rowconfigure(0, weight=1)
        
        # Treeview Configuration
        self.tree_style = ttk.Style()
        self.tree_style.theme_use("clam")
        
        initial_bg = self.colors["light"]["card"] if ctk.get_appearance_mode() == "Light" else self.colors["dark"]["card"]
        self.tree_frame = tk.Frame(self.list_card, bg=initial_bg) 
        self.tree_frame.grid(row=0, column=0, padx=15, pady=15, sticky="nsew")
        
        self.configure_tree_style()
        
        columns = ("date", "desc", "category", "amount")
        self.tree = ttk.Treeview(self.tree_frame, columns=columns, show="headings", selectmode="browse")
        self.tree.heading("date", text="Date & Time")
        self.tree.heading("desc", text="Description")
        self.tree.heading("category", text="Category")
        self.tree.heading("amount", text="Amount (GH₵)")
        
        self.tree.column("date", width=250, anchor="center")
        self.tree.column("desc", width=300)
        self.tree.column("category", width=150, anchor="center")
        self.tree.column("amount", width=120, anchor="e")
        
        scrollbar = ttk.Scrollbar(self.tree_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # --- Footer ---
        self.footer_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.footer_frame.grid(row=3, column=0, padx=30, pady=20, sticky="ew")
        
        self.feedback_label = ctk.CTkLabel(self.footer_frame, text="Ready to track.", font=("Poppins", 14))
        self.feedback_label.pack(side="left")
        
        self.delete_btn = ctk.CTkButton(
            self.footer_frame, 
            text="Delete Selected", 
            command=self.delete_expense,
            fg_color="#EF4444", 
            hover_color="#DC2626",
            font=("Poppins", 13, "bold"),
            height=35,
            corner_radius=10
        )
        self.delete_btn.pack(side="right")

        # Initial stats update
        self.update_stats()

    def configure_tree_style(self):
        appearance = ctk.get_appearance_mode()
        c = self.colors[appearance.lower()]
        
        # Update standard frame background
        self.tree_frame.configure(bg=c["card"])
        
        self.tree_style.configure(
            "Treeview",
            background=c["card"],
            foreground=c["text"],
            fieldbackground=c["card"],
            rowheight=45,
            font=("Poppins", 14),
            borderwidth=0
        )
        self.tree_style.map(
            "Treeview",
            background=[("selected", c["accent"])],
            foreground=[("selected", "#FFFFFF")]
        )
        self.tree_style.configure(
            "Treeview.Heading",
            background=c["bg"],
            foreground=c["text"],
            font=("Poppins", 14, "bold"),
            borderwidth=0
        )
        
        # Scrollbar styling for a modern look in both themes
        self.tree_style.configure(
            "TScrollbar",
            arrowcolor=c["text"],
            background=c["card"],
            troughcolor=c["bg"],
            borderwidth=0,
            relief="flat"
        )

    def toggle_theme(self):
        new_mode = "dark" if ctk.get_appearance_mode() == "Light" else "light"
        ctk.set_appearance_mode(new_mode)
        self.theme_toggle.configure(text="☀️ Light Mode" if new_mode == "dark" else "🌙 Dark Mode")
        self.after(100, self.configure_tree_style)
        self.show_feedback("Theme updated.", "success")

    def show_feedback(self, message, msg_type="default"):
        appearance = ctk.get_appearance_mode().lower()
        colors = self.colors[appearance]
        color = colors["text"]
        if msg_type == "error": color = colors["error"]
        elif msg_type == "success": color = colors["success"]
        self.feedback_label.configure(text=message, text_color=color)
        if self._feedback_timer is not None:
            self.after_cancel(self._feedback_timer)
        self._feedback_timer = self.after(3000, lambda: self.feedback_label.configure(text="", text_color=colors["text"]))

    def add_expense(self):
        desc = self.desc_entry.get().strip()
        amt_str = self.amount_entry.get().strip()
        cat = self.category_var.get()
        
        if not desc:
            self.show_feedback("Error: Description required!", "error")
            return
        try:
            amount = float(amt_str)
            if amount <= 0:
                self.show_feedback("Error: Value must be positive!", "error")
                return
        except ValueError:
            self.show_feedback("Error: Invalid amount!", "error")
            return
            
        timestamp = datetime.now().strftime("%b %d, %Y — %I:%M %p")
        self.expenses.append((timestamp, desc, cat, amount))
        self.tree.insert("", tk.END, values=(timestamp, desc, cat, f"{amount:.2f}"))
        
        self.update_stats()
        self.desc_entry.delete(0, tk.END)
        self.amount_entry.delete(0, tk.END)
        self.show_feedback(f"Added '{desc}'", "success")

    def delete_expense(self):
        selected_item = self.tree.selection()
        if not selected_item:
            self.show_feedback("No item selected.", "error")
            return
        for item in selected_item:
            values = self.tree.item(item, "values")
            timestamp, desc, cat, amt_str = values
            for i, exp in enumerate(self.expenses):
                if exp[0] == timestamp and exp[1] == desc and exp[2] == cat and f"{exp[3]:.2f}" == amt_str:
                    self.expenses.pop(i)
                    break
            self.tree.delete(item)
        self.update_stats()
        self.show_feedback("Deleted item.", "success")

    def update_stats(self):
        self.total_amount = sum(exp[3] for exp in self.expenses)
        self.total_val_label.configure(text=f"GH₵ {self.total_amount:.2f}")
        
        # Calculate percentage
        percent = (self.total_amount / self.budget_limit) * 100
        self.percentage_label.configure(text=f"{int(percent)}%")
        
        progress = min(self.total_amount / self.budget_limit, 1.0)
        self.progress_bar.set(progress)
        
        appearance = ctk.get_appearance_mode().lower()
        colors = self.colors[appearance]
        
        # Color coding stats and progress
        if self.total_amount <= 0:
             self.progress_bar.configure(progress_color=colors["border"])
             self.percentage_label.configure(text_color=colors["text"])
        elif self.total_amount > self.budget_limit:
            self.total_val_label.configure(text_color=colors["error"])
            self.status_text.configure(text="Warning: Budget Exceeded!", text_color=colors["error"])
            self.progress_bar.configure(progress_color=colors["error"])
            self.percentage_label.configure(text_color=colors["error"])
        else:
            self.total_val_label.configure(text_color=colors["text"])
            self.status_text.configure(text="Safe (Limit: GH₵ 1000)", text_color=colors["text"])
            self.progress_bar.configure(progress_color=colors["accent"])
            self.percentage_label.configure(text_color=colors["accent"])

if __name__ == "__main__":
    app = ExpenseTracker()
    app.mainloop()

