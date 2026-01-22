
"""
Personal Finance Tracker
A command-line application for managing personal income and expenses
"""

import json
import os
from datetime import datetime
from typing import List, Dict, Optional

class Transaction:
    """Represents a financial transaction"""
    
    def __init__(self, transaction_id: int, transaction_type: str, 
                 category: str, amount: float, description: str, 
                 date: str = None):
        self.transaction_id = transaction_id
        self.transaction_type = transaction_type  # 'income' or 'expense'
        self.category = category
        self.amount = amount
        self.description = description
        self.date = date if date else datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    def to_dict(self) -> Dict:
        """Convert transaction to dictionary"""
        return {
            'transaction_id': self.transaction_id,
            'transaction_type': self.transaction_type,
            'category': self.category,
            'amount': self.amount,
            'description': self.description,
            'date': self.date
        }
    
    @staticmethod
    def from_dict(data: Dict) -> 'Transaction':
        """Create transaction from dictionary"""
        return Transaction(
            data['transaction_id'],
            data['transaction_type'],
            data['category'],
            data['amount'],
            data['description'],
            data['date']
        )


class FinanceManager:
    """Manages all financial transactions"""
    
    def __init__(self, data_file: str = "finance_data.json"):
        self.data_file = data_file
        self.transactions: List[Transaction] = []
        self.next_transaction_id = 1
        self.load_transactions()
    
    def load_transactions(self):
        """Load transactions from JSON file"""
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, 'r') as file:
                    data = json.load(file)
                    self.transactions = [Transaction.from_dict(t) for t in data['transactions']]
                    self.next_transaction_id = data.get('next_id', 1)
            except (json.JSONDecodeError, KeyError):
                print("Error loading data. Starting fresh.")
                self.transactions = []
                self.next_transaction_id = 1
    
    def save_transactions(self):
        """Save transactions to JSON file"""
        data = {
            'transactions': [t.to_dict() for t in self.transactions],
            'next_id': self.next_transaction_id
        }
        with open(self.data_file, 'w') as file:
            json.dump(data, file, indent=4)
    
    def add_transaction(self, transaction_type: str, category: str, 
                       amount: float, description: str) -> Transaction:
        """Add a new transaction"""
        transaction = Transaction(
            self.next_transaction_id,
            transaction_type,
            category,
            amount,
            description
        )
        self.transactions.append(transaction)
        self.next_transaction_id += 1
        self.save_transactions()
        return transaction
    
    def delete_transaction(self, transaction_id: int) -> bool:
        """Delete a transaction by ID"""
        for i, t in enumerate(self.transactions):
            if t.transaction_id == transaction_id:
                self.transactions.pop(i)
                self.save_transactions()
                return True
        return False
    
    def get_all_transactions(self) -> List[Transaction]:
        """Get all transactions"""
        return self.transactions
    
    def get_transactions_by_type(self, transaction_type: str) -> List[Transaction]:
        """Get transactions filtered by type"""
        return [t for t in self.transactions if t.transaction_type == transaction_type]
    
    def calculate_balance(self) -> float:
        """Calculate current balance"""
        income = sum(t.amount for t in self.transactions if t.transaction_type == 'income')
        expenses = sum(t.amount for t in self.transactions if t.transaction_type == 'expense')
        return income - expenses
    
    def get_category_summary(self) -> Dict[str, float]:
        """Get spending summary by category"""
        summary = {}
        for t in self.transactions:
            if t.transaction_type == 'expense':
                summary[t.category] = summary.get(t.category, 0) + t.amount
        return summary


class FinanceTrackerUI:
    """User Interface for Finance Tracker"""
    
    def __init__(self):
        self.manager = FinanceManager()
    
    def display_menu(self):
        """Display main menu"""
        print("\n" + "="*50)
        print("PERSONAL FINANCE TRACKER")
        print("="*50)
        print("1. Add Income")
        print("2. Add Expense")
        print("3. View All Transactions")
        print("4. View Balance")
        print("5. View Category Summary")
        print("6. Delete Transaction")
        print("7. Exit")
        print("="*50)
    
    def add_income(self):
        """Add income transaction"""
        print("\n--- Add Income ---")
        category = input("Category (e.g., Salary, Freelance): ").strip()
        amount = float(input("Amount: "))
        description = input("Description: ").strip()
        
        transaction = self.manager.add_transaction('income', category, amount, description)
        print(f"✓ Income added successfully! (ID: {transaction.transaction_id})")
    
    def add_expense(self):
        """Add expense transaction"""
        print("\n--- Add Expense ---")
        category = input("Category (e.g., Food, Transport, Bills): ").strip()
        amount = float(input("Amount: "))
        description = input("Description: ").strip()
        
        transaction = self.manager.add_transaction('expense', category, amount, description)
        print(f"✓ Expense added successfully! (ID: {transaction.transaction_id})")
    
    def view_all_transactions(self):
        """Display all transactions"""
        transactions = self.manager.get_all_transactions()
        
        if not transactions:
            print("\nNo transactions found.")
            return
        
        print("\n" + "="*80)
        print(f"{'ID':<5} {'Type':<10} {'Category':<15} {'Amount':<12} {'Description':<20} {'Date':<20}")
        print("="*80)
        
        for t in transactions:
            print(f"{t.transaction_id:<5} {t.transaction_type.capitalize():<10} "
                  f"{t.category:<15} ${t.amount:<11.2f} {t.description:<20} {t.date:<20}")
        print("="*80)
    
    def view_balance(self):
        """Display current balance"""
        balance = self.manager.calculate_balance()
        income = sum(t.amount for t in self.manager.get_transactions_by_type('income'))
        expenses = sum(t.amount for t in self.manager.get_transactions_by_type('expense'))
        
        print("\n" + "="*40)
        print("FINANCIAL SUMMARY")
        print("="*40)
        print(f"Total Income:  ${income:,.2f}")
        print(f"Total Expenses: ${expenses:,.2f}")
        print("-"*40)
        print(f"Current Balance: ${balance:,.2f}")
        print("="*40)
    
    def view_category_summary(self):
        """Display spending by category"""
        summary = self.manager.get_category_summary()
        
        if not summary:
            print("\nNo expense categories found.")
            return
        
        print("\n" + "="*40)
        print("EXPENSE BREAKDOWN BY CATEGORY")
        print("="*40)
        
        for category, amount in sorted(summary.items(), key=lambda x: x[1], reverse=True):
            print(f"{category:<20} ${amount:,.2f}")
        
        total = sum(summary.values())
        print("-"*40)
        print(f"{'TOTAL':<20} ${total:,.2f}")
        print("="*40)
    
    def delete_transaction(self):
        """Delete a transaction"""
        self.view_all_transactions()
        
        if not self.manager.get_all_transactions():
            return
        
        try:
            transaction_id = int(input("\nEnter Transaction ID to delete: "))
            if self.manager.delete_transaction(transaction_id):
                print("✓ Transaction deleted successfully!")
            else:
                print("✗ Transaction not found.")
        except ValueError:
            print("✗ Invalid ID.")
    
    def run(self):
        """Main application loop"""
        print("Welcome to Personal Finance Tracker!")
        
        while True:
            self.display_menu()
            choice = input("\nEnter your choice (1-7): ").strip()
            
            try:
                if choice == '1':
                    self.add_income()
                elif choice == '2':
                    self.add_expense()
                elif choice == '3':
                    self.view_all_transactions()
                elif choice == '4':
                    self.view_balance()
                elif choice == '5':
                    self.view_category_summary()
                elif choice == '6':
                    self.delete_transaction()
                elif choice == '7':
                    print("\nThank you for using Personal Finance Tracker!")
                    break
                else:
                    print("✗ Invalid choice. Please try again.")
            except Exception as e:
                print(f"✗ An error occurred: {e}")
                print("Please try again.")


if __name__ == "__main__":
    app = FinanceTrackerUI()
    app.run()
