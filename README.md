# Student Expense Tracker

This is a Python GUI application built for the CSM 357 Human-Computer Interaction assignment. It helps students quickly track their daily expenses like food, transport, and study materials. The main focus of this project is on usability and applying good HCI principles to make the interface clean and easy to understand.

## Features
- Add new expenses with a description, amount (GH₵), and category.
- View all saved expenses in a clear data table.
- Delete any selected expense.
- Toggle between Light Mode and Dark Mode for better accessibility.

## HCI Principles Applied
I made sure to include several HCI concepts we discussed in class:
1. **Consistency and Standards**: I used a consistent color palette, button styling, and layout structure across the whole app.
2. **Error Prevention**: If a user tries to add an expense without a description or with an invalid/negative amount, the app catches it and shows an error message instead of crashing.
3. **Clear Feedback**: When you add an item, delete an item, or switch the theme, a small status message shows up briefly at the top to let you know the action was successful.
4. **User Control and Freedom**: You can select any expense from the list and delete it if you made a mistake.
5. **Recognition rather than recall**: All the expenses are always visible in a structured table so users don't have to remember what they inputted earlier. 

## How to Run
1. Make sure you have standard Python installed on your computer.
2. Clone or download this project folder.
3. Open a terminal or command prompt in the folder and run:
   `python expense_tracker.py`
