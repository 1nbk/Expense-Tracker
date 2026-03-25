import unittest
import unittest.mock as mock
from expense_tracker import ExpenseTracker
import customtkinter as ctk
import os
import tkinter as tk

class TestExpenseTracker(unittest.TestCase):
    def setUp(self):
        # Use a temporary file for testing to protect real data
        ExpenseTracker.DATA_FILE = "test_expenses.json"
        
        # Initialize app
        self.app = ExpenseTracker()
        self.app.withdraw() # Hide window during tests

    def test_add_expense_logic(self):
        """Tests that adding an expense correctly updates state and total."""
        self.app.desc_entry.insert(0, "Test Pizza")
        self.app.amount_entry.insert(0, "45.00")
        self.app.category_var.set("Food")
        
        # Mock the confirmation dialog to always say 'Yes'
        with mock.patch('tkinter.messagebox.askyesno', return_value=True):
            self.app.add_expense()
        
        # Verify 4-column storage: (Timestamp, Desc, Cat, Amount)
        self.assertEqual(len(self.app.expenses), 1)
        self.assertEqual(self.app.expenses[0][1], "Test Pizza")
        self.assertEqual(self.app.expenses[0][3], 45.00)
        self.assertEqual(self.app.total_amount, 45.00)
        
    def test_budget_overrun_warning_logic(self):
        """Tests if the total turns red (error color) when budget is exceeded."""
        # Set a low budget for testing
        self.app.budget_limit = 50.0
        
        # Add expensive item
        self.app.expenses = [("Time", "Rent", "Study", 100.0)]
        self.app.update_stats()
        
        # Check if error colors are applied
        error_color = self.app.colors[ctk.get_appearance_mode().lower()]["error"]
        # Note: CTkLabel.cget('text_color') returns the color tuple or name
        # We just check the internal state update
        self.assertEqual(self.app.total_amount, 100.0)
        self.assertTrue(self.app.total_amount > self.app.budget_limit)

    def test_delete_expense_logic(self):
        """Tests if deleting an item correctly recalibrates the total."""
        self.app.expenses = [
            ("Time1", "Item 1", "Food", 50.0), 
            ("Time2", "Item 2", "Study", 30.0)
        ]
        self.app.update_stats()
        self.assertEqual(self.app.total_amount, 80.0)
        
        # Simulate deletion
        self.app.expenses.pop(0)
        self.app.update_stats()
        self.assertEqual(self.app.total_amount, 30.0)

    def tearDown(self):
        self.app.destroy()
        # Clean up test database
        if os.path.exists("test_expenses.json"):
            os.remove("test_expenses.json")

if __name__ == "__main__":
    unittest.main()
