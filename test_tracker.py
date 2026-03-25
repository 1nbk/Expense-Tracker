import unittest
from expense_tracker import ExpenseTracker
import customtkinter as ctk

class TestExpenseTracker(unittest.TestCase):
    def setUp(self):
        # We need a headless instance if possible or just test logic
        self.app = ExpenseTracker()
        self.app.withdraw() # Hide window

    def test_add_expense_logic(self):
        # Manually trigger addition
        self.app.desc_entry.insert(0, "Test Item")
        self.app.amount_entry.insert(0, "100.50")
        self.app.category_var.set("Food")
        self.app.add_expense()
        
        self.assertEqual(len(self.app.expenses), 1)
        self.assertEqual(self.app.total_amount, 100.50)
        
    def test_delete_expense_logic(self):
        self.app.expenses = [("Item 1", "Food", 50.0), ("Item 2", "Study", 30.0)]
        self.app.update_stats()
        self.assertEqual(self.app.total_amount, 80.0)
        
        # Simulate deletion of the first item
        self.app.expenses.pop(0)
        self.app.update_stats()
        self.assertEqual(self.app.total_amount, 30.0)

    def tearDown(self):
        self.app.destroy()

if __name__ == "__main__":
    unittest.main()
