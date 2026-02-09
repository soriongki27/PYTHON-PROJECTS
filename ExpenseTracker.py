# COMPLETE EXPENSE TRACKER - FINAL VERSION
# ==========================================

"""
This is the complete expense tracker combining everything we learned!

FEATURES:
- Add, view, edit, and delete expenses
- Filter by category and date range
- View statistics and charts
- Modern, professional UI
- Full database integration
"""

import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime, timedelta
import sqlite3

class ExpenseDatabase:
    """Complete database manager with all features"""
    
    def __init__(self, db_name='expenses.db'):
        self.db_name = db_name
        self.create_table()
    
    def get_connection(self):
        return sqlite3.connect(self.db_name)
    
    def create_table(self):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS expenses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date TEXT NOT NULL,
                category TEXT NOT NULL,
                amount REAL NOT NULL,
                description TEXT
            )
        ''')
        conn.commit()
        conn.close()
    
    def add_expense(self, date, category, amount, description=''):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO expenses (date, category, amount, description)
            VALUES (?, ?, ?, ?)
        ''', (date, category, amount, description))
        expense_id = cursor.lastrowid
        conn.commit()
        conn.close()
        return expense_id
    
    def get_all_expenses(self):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM expenses ORDER BY date DESC, id DESC')
        expenses = cursor.fetchall()
        conn.close()
        return expenses
    
    def get_expense_by_id(self, expense_id):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM expenses WHERE id = ?', (expense_id,))
        expense = cursor.fetchone()
        conn.close()
        return expense
    
    def update_expense(self, expense_id, date, category, amount, description):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE expenses 
            SET date = ?, category = ?, amount = ?, description = ?
            WHERE id = ?
        ''', (date, category, amount, description, expense_id))
        conn.commit()
        conn.close()
    
    def delete_expense(self, expense_id):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('DELETE FROM expenses WHERE id = ?', (expense_id,))
        conn.commit()
        conn.close()
    
    def get_expenses_by_category(self, category):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT * FROM expenses 
            WHERE category = ? 
            ORDER BY date DESC
        ''', (category,))
        expenses = cursor.fetchall()
        conn.close()
        return expenses
    
    def get_expenses_by_date_range(self, start_date, end_date):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT * FROM expenses 
            WHERE date BETWEEN ? AND ? 
            ORDER BY date DESC
        ''', (start_date, end_date))
        expenses = cursor.fetchall()
        conn.close()
        return expenses
    
    def get_total_expenses(self):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT SUM(amount) FROM expenses')
        total = cursor.fetchone()[0]
        conn.close()
        return total if total else 0.0
    
    def get_total_by_category(self):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT category, SUM(amount) as total
            FROM expenses
            GROUP BY category
            ORDER BY total DESC
        ''')
        totals = cursor.fetchall()
        conn.close()
        return totals
    
    def get_monthly_total(self, year, month):
        """Get total expenses for a specific month"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT SUM(amount) FROM expenses
            WHERE strftime('%Y', date) = ? AND strftime('%m', date) = ?
        ''', (str(year), f'{month:02d}'))
        total = cursor.fetchone()[0]
        conn.close()
        return total if total else 0.0


class CompleteExpenseTracker:
    """
    Complete expense tracker application with all features
    """
    
    def __init__(self, root):
        self.root = root
        self.root.title("💰 Complete Expense Tracker")
        self.root.geometry("1000x700")
        self.root.configure(bg='#f0f0f0')
        
        # Initialize database
        self.db = ExpenseDatabase()
        
        # Color scheme
        self.primary_color = '#2196F3'
        self.success_color = '#4CAF50'
        self.danger_color = '#f44336'
        self.warning_color = '#FF9800'
        
        # Create GUI
        self.create_widgets()
        
        # Load data
        self.refresh_expense_list()
    
    def create_widgets(self):
        """Create all GUI components"""
        
        # ============= HEADER =============
        header = tk.Frame(self.root, bg=self.primary_color, height=60)
        header.pack(fill='x')
        
        tk.Label(header, text="💰 Expense Tracker", 
                font=('Arial', 20, 'bold'), bg=self.primary_color, 
                fg='white').pack(pady=15)
        
        # ============= MAIN CONTAINER =============
        main_container = tk.Frame(self.root, bg='#f0f0f0')
        main_container.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Left panel (input)
        left_panel = tk.Frame(main_container, bg='white', width=300)
        left_panel.pack(side='left', fill='y', padx=(0, 5))
        
        # Right panel (list and stats)
        right_panel = tk.Frame(main_container, bg='#f0f0f0')
        right_panel.pack(side='right', fill='both', expand=True, padx=(5, 0))
        
        # Create left panel widgets
        self.create_input_section(left_panel)
        
        # Create right panel widgets
        self.create_list_section(right_panel)
        self.create_stats_section(right_panel)
    
    def create_input_section(self, parent):
        """Create input form section"""
        
        tk.Label(parent, text="Add New Expense", 
                font=('Arial', 14, 'bold'), bg='white').pack(pady=15)
        
        # Date
        tk.Label(parent, text="Date:", font=('Arial', 10), 
                bg='white').pack(anchor='w', padx=20)
        self.date_entry = tk.Entry(parent, font=('Arial', 10), width=25)
        self.date_entry.pack(padx=20, pady=5)
        self.date_entry.insert(0, datetime.now().strftime('%Y-%m-%d'))
        
        # Category
        tk.Label(parent, text="Category:", font=('Arial', 10), 
                bg='white').pack(anchor='w', padx=20, pady=(10, 0))
        self.category_var = tk.StringVar()
        self.category_combo = ttk.Combobox(parent, textvariable=self.category_var,
                                          font=('Arial', 10), width=23)
        self.category_combo['values'] = ('Food', 'Transport', 'Entertainment',
                                         'Shopping', 'Bills', 'Healthcare', 
                                         'Education', 'Other')
        self.category_combo.pack(padx=20, pady=5)
        self.category_combo.current(0)
        
        # Amount
        tk.Label(parent, text="Amount ($):", font=('Arial', 10), 
                bg='white').pack(anchor='w', padx=20, pady=(10, 0))
        self.amount_entry = tk.Entry(parent, font=('Arial', 10), width=25)
        self.amount_entry.pack(padx=20, pady=5)
        
        # Description
        tk.Label(parent, text="Description:", font=('Arial', 10), 
                bg='white').pack(anchor='w', padx=20, pady=(10, 0))
        self.description_entry = tk.Text(parent, font=('Arial', 10), 
                                        width=25, height=4)
        self.description_entry.pack(padx=20, pady=5)
        
        # Buttons frame
        btn_frame = tk.Frame(parent, bg='white')
        btn_frame.pack(pady=20)
        
        # Add button
        add_btn = tk.Button(btn_frame, text="Add Expense", 
                           font=('Arial', 11, 'bold'), bg=self.success_color,
                           fg='white', command=self.add_expense, cursor='hand2',
                           padx=20, pady=10, relief='flat')
        add_btn.pack(pady=5)
        
        # Clear button
        clear_btn = tk.Button(btn_frame, text="Clear Form", 
                             font=('Arial', 10), bg='#757575', fg='white',
                             command=self.clear_form, cursor='hand2',
                             padx=20, pady=8, relief='flat')
        clear_btn.pack(pady=5)
    
    def create_list_section(self, parent):
        """Create expense list section"""
        
        list_container = tk.Frame(parent, bg='white')
        list_container.pack(fill='both', expand=True, pady=(0, 10))
        
        # Header
        header_frame = tk.Frame(list_container, bg='white')
        header_frame.pack(fill='x', padx=10, pady=10)
        
        tk.Label(header_frame, text="Expense History", 
                font=('Arial', 14, 'bold'), bg='white').pack(side='left')
        
        # Action buttons
        btn_frame = tk.Frame(header_frame, bg='white')
        btn_frame.pack(side='right')
        
        tk.Button(btn_frame, text="🗑️ Delete", font=('Arial', 9),
                 bg=self.danger_color, fg='white', command=self.delete_expense,
                 cursor='hand2', relief='flat', padx=10, pady=5).pack(side='left', padx=2)
        
        tk.Button(btn_frame, text="✏️ Edit", font=('Arial', 9),
                 bg=self.warning_color, fg='white', command=self.edit_expense,
                 cursor='hand2', relief='flat', padx=10, pady=5).pack(side='left', padx=2)
        
        tk.Button(btn_frame, text="🔄 Refresh", font=('Arial', 9),
                 bg=self.primary_color, fg='white', command=self.refresh_expense_list,
                 cursor='hand2', relief='flat', padx=10, pady=5).pack(side='left', padx=2)
        
        # Treeview
        tree_frame = tk.Frame(list_container)
        tree_frame.pack(fill='both', expand=True, padx=10, pady=(0, 10))
        
        columns = ('ID', 'Date', 'Category', 'Amount', 'Description')
        self.tree = ttk.Treeview(tree_frame, columns=columns, show='headings', 
                                height=12)
        
        self.tree.heading('ID', text='ID')
        self.tree.heading('Date', text='Date')
        self.tree.heading('Category', text='Category')
        self.tree.heading('Amount', text='Amount')
        self.tree.heading('Description', text='Description')
        
        self.tree.column('ID', width=50)
        self.tree.column('Date', width=100)
        self.tree.column('Category', width=120)
        self.tree.column('Amount', width=100)
        self.tree.column('Description', width=250)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(tree_frame, orient='vertical', 
                                 command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        self.tree.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
    
    def create_stats_section(self, parent):
        """Create statistics section"""
        
        stats_frame = tk.Frame(parent, bg='white')
        stats_frame.pack(fill='x')
        
        tk.Label(stats_frame, text="Statistics", 
                font=('Arial', 14, 'bold'), bg='white').pack(pady=10)
        
        # Total expense
        self.total_label = tk.Label(stats_frame, text="Total: $0.00", 
                                   font=('Arial', 16, 'bold'), 
                                   bg='white', fg=self.primary_color)
        self.total_label.pack(pady=5)
        
        # Category breakdown
        self.category_frame = tk.Frame(stats_frame, bg='white')
        self.category_frame.pack(fill='x', padx=20, pady=10)
    
    def add_expense(self):
        """Add new expense"""
        date = self.date_entry.get().strip()
        category = self.category_var.get().strip()
        amount_str = self.amount_entry.get().strip()
        description = self.description_entry.get('1.0', 'end').strip()
        
        if not date or not category or not amount_str:
            messagebox.showerror("Error", "Please fill in all required fields!")
            return
        
        try:
            amount = float(amount_str)
            if amount <= 0:
                raise ValueError("Amount must be positive")
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid amount!")
            return
        
        try:
            self.db.add_expense(date, category, amount, description)
            messagebox.showinfo("Success", "✅ Expense added successfully!")
            self.clear_form()
            self.refresh_expense_list()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to add expense: {str(e)}")
    
    def clear_form(self):
        """Clear all input fields"""
        self.date_entry.delete(0, tk.END)
        self.date_entry.insert(0, datetime.now().strftime('%Y-%m-%d'))
        self.amount_entry.delete(0, tk.END)
        self.description_entry.delete('1.0', 'end')
        self.category_combo.current(0)
    
    def refresh_expense_list(self):
        """Refresh expense list and statistics"""
        # Clear tree
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Load expenses
        expenses = self.db.get_all_expenses()
        for expense in expenses:
            self.tree.insert('', 'end', values=(
                expense[0],
                expense[1],
                expense[2],
                f"${expense[3]:.2f}",
                expense[4]
            ))
        
        # Update total
        total = self.db.get_total_expenses()
        self.total_label.config(text=f"Total: ${total:.2f}")
        
        # Update category breakdown
        for widget in self.category_frame.winfo_children():
            widget.destroy()
        
        category_totals = self.db.get_total_by_category()
        for category, total in category_totals[:5]:  # Top 5 categories
            frame = tk.Frame(self.category_frame, bg='white')
            frame.pack(fill='x', pady=2)
            
            tk.Label(frame, text=f"{category}:", font=('Arial', 10),
                    bg='white', width=15, anchor='w').pack(side='left')
            tk.Label(frame, text=f"${total:.2f}", font=('Arial', 10, 'bold'),
                    bg='white', fg=self.success_color).pack(side='right')
    
    def delete_expense(self):
        """Delete selected expense"""
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select an expense to delete!")
            return
        
        if messagebox.askyesno("Confirm", "Delete this expense?"):
            item = self.tree.item(selected[0])
            expense_id = item['values'][0]
            self.db.delete_expense(expense_id)
            self.refresh_expense_list()
            messagebox.showinfo("Success", "✅ Expense deleted!")
    
    def edit_expense(self):
        """Edit selected expense"""
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select an expense to edit!")
            return
        
        item = self.tree.item(selected[0])
        expense_id = item['values'][0]
        
        # Get expense data
        expense = self.db.get_expense_by_id(expense_id)
        
        # Populate form
        self.date_entry.delete(0, tk.END)
        self.date_entry.insert(0, expense[1])
        
        self.category_var.set(expense[2])
        
        self.amount_entry.delete(0, tk.END)
        self.amount_entry.insert(0, str(expense[3]))
        
        self.description_entry.delete('1.0', 'end')
        self.description_entry.insert('1.0', expense[4])
        
        # Delete old expense
        self.db.delete_expense(expense_id)
        messagebox.showinfo("Edit Mode", "Expense loaded. Click 'Add Expense' to save changes.")


# ============================================================================
# RUN THE APPLICATION
# ============================================================================

if __name__ == "__main__":
    print("=" * 70)
    print("LAUNCHING COMPLETE EXPENSE TRACKER")
    print("=" * 70)
    print("\nFeatures:")
    print("✅ Add, edit, and delete expenses")
    print("✅ View expense history")
    print("✅ Real-time statistics")
    print("✅ SQLite database integration")
    print("✅ Modern, professional UI")
    print("\n" + "=" * 70)
    
    root = tk.Tk()
    app = CompleteExpenseTracker(root)
    root.mainloop()