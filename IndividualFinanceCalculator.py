def IFC(): 
  """
Individual_finance_Calculator.py
Author: Oladipo Towobola
Date written: 04/08/2025
Purpose: Individual Finance Calculator - Tkinter GUI application to manage income, expenses, and view financial summary
"""
import tkinter as tk
from tkinter import messagebox
from datetime import datetime
from PIL import Image, ImageTk
import requests
from io import BytesIO
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Global storage for income and expenses
income_data = []
expense_data = []

# Validate input function
def validate_entry(entry, data_type):
    if not entry:
        return False
    try:
        if data_type == 'float':
            float(entry)
        elif data_type == 'date':
            datetime.strptime(entry, '%Y-%m-%d')
        return True
    except ValueError:
        return False
   

# Main Application Class
class IndividualFinanceCalculator:
    def __init__(self, root):
        self.root = root
        self.root.title("Individual Finance Calculator")
        self.display_image("https://thumbs.dreamstime.com/b/growing-money-plant-coins-finance-investment-concept-generative-ai-business-274026331.jpg", alt_text="Financial Growth", size=(100, 100))
        self.create_main_menu()

    def display_image(self, url, alt_text="", size=(80, 80)):
        try:
            response = requests.get(url)
            img_data = response.content
            img = Image.open(BytesIO(img_data))
            img = img.resize(size, Image.Resampling.LANCZOS)
            img_tk = ImageTk.PhotoImage(img)

            label = tk.Label(self.root, image=img_tk)
            label.image = img_tk  # Keep a reference
            label.pack()
            label.tooltip_text = alt_text # Add tooltip if needed (requires separate library)
        except Exception as e:
            print(f"Image loading failed: {e}")
            tk.Label(self.root, text=f"[{alt_text}]").pack() # Display alt text if image fails

    def create_main_menu(self):
        self.clear_window()
        tk.Label(self.root, text="Individual Finance Calculator", font=("Arial", 20)).pack(pady=10)
        tk.Label(self.root, text="Welcome to your Individual Finance Calculator!").pack(pady=5)

        tk.Button(self.root, text="Enter Income", width=20, command=self.enter_income).pack(pady=5)
        tk.Button(self.root, text="Enter Expenses", width=20, command=self.enter_expense).pack(pady=5)
        tk.Button(self.root, text="View Summary", width=20, command=self.view_summary).pack(pady=5)
        tk.Button(self.root, text="Exit", width=20, command=self.root.quit).pack(pady=5)

    def enter_income(self):
        self.clear_window()

        tk.Label(self.root, text="Enter Income", font=("Arial", 14)).pack(pady=10)
        self.display_image("https://static.vecteezy.com/system/resources/previews/020/600/795/large_2x/bag-of-money-pixel-perfect-linear-ui-icon-personal-savings-business-investment-gui-ux-design-outline-isolated-user-interface-element-for-app-and-web-editable-stroke-vector.jpg", alt_text="Income", size=(50, 50))
        tk.Label(self.root, text="Source of Income:").pack()
        source_entry = tk.Entry(self.root)
        source_entry.pack()

        tk.Label(self.root, text="Amount ($):").pack()
        amount_entry = tk.Entry(self.root)
        amount_entry.pack()

        tk.Label(self.root, text="Date (YYYY-MM-DD):").pack()
        date_entry = tk.Entry(self.root)
        date_entry.pack()

        def save_income():
            source = source_entry.get()
            amount = amount_entry.get()
            date = date_entry.get()

            if not (source and validate_entry(amount, 'float') and validate_entry(date, 'date')):
                messagebox.showerror("Input Error", "Please enter valid income details.")
                return
            income_data.append((source, float(amount), date))
            messagebox.showinfo("Saved", "Income data saved successfully!")

        tk.Button(self.root, text="Save Income", command=save_income).pack(pady=5)
        tk.Button(self.root, text="Back to Main Menu", command=self.create_main_menu).pack(pady=5)

    def enter_expense(self):
        self.clear_window()

        tk.Label(self.root, text="Enter Expenses", font=("Arial", 14)).pack(pady=10)
        self.display_image("https://thumbs.dreamstime.com/b/growing-money-plant-coins-finance-investment-concept-generative-ai-business-274026331.jpg", alt_text="Expenses", size=(50, 50))
        tk.Label(self.root, text="Category:").pack()
        category_entry = tk.Entry(self.root)
        category_entry.pack()

        tk.Label(self.root, text="Amount ($):").pack()
        amount_entry = tk.Entry(self.root)
        amount_entry.pack()

        tk.Label(self.root, text="Date (YYYY-MM-DD):").pack()
        date_entry = tk.Entry(self.root)
        date_entry.pack()

        def save_expense():
            category = category_entry.get()
            amount = amount_entry.get()
            date = date_entry.get()

            if not (category and validate_entry(amount, 'float') and validate_entry(date, 'date')):
                messagebox.showerror("Input Error", "Please enter valid expense details.")
                return
            expense_data.append((category, float(amount), date))
            messagebox.showinfo("Saved", "Expense data saved successfully!")

        tk.Button(self.root, text="Save Expense", command=save_expense).pack(pady=5)
        tk.Button(self.root, text="Back to Main Menu", command=self.create_main_menu).pack(pady=5)

    def view_summary(self):
        self.clear_window()

        tk.Label(self.root, text="Financial Summary", font=("Arial", 14)).pack(pady=10)

        total_income = sum([item[1] for item in income_data])
        total_expense = sum([item[1] for item in expense_data])
        savings = total_income - total_expense

        tk.Label(self.root, text=f"Total Income: ${total_income:.2f}").pack()
        tk.Label(self.root, text=f"Total Expenses: ${total_expense:.2f}").pack()
        tk.Label(self.root, text=f"Total Savings/Loss: ${savings:.2f}").pack(pady=5)

        fig, ax = plt.subplots(figsize=(4, 3))
        ax.bar(['Income', 'Expenses'], [total_income, total_expense], color=['green', 'red'])
        ax.set_title('Income vs Expenses')
        canvas = FigureCanvasTkAgg(fig, master=self.root)
        canvas.draw()
        canvas.get_tk_widget().pack()

        tk.Button(self.root, text="Back to Main Menu", command=self.create_main_menu).pack(pady=5)

    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()
print(IFC.__doc__)
IFC()
if __name__ == '__main__':
    root = tk.Tk()
    app = IndividualFinanceCalculator(root)
    root.mainloop()
