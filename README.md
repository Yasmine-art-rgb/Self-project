# Personal Finance Tracker

A command-line application for managing personal income and expenses with transaction tracking, balance calculation, and category-based expense analysis.

---

## Table of Contents
- [Project Overview](#project-overview)
- [Software Development Life Cycle (SDLC)](#software-development-life-cycle-sdlc)
  - [1. Planning Phase](#1-planning-phase)
  - [2. Requirements Analysis Phase](#2-requirements-analysis-phase)
  - [3. Design Phase](#3-design-phase)
  - [4. Implementation Phase](#4-implementation-phase)
  - [5. Testing Phase](#5-testing-phase)
  - [6. Deployment Phase](#6-deployment-phase)
  - [7. Maintenance Phase](#7-maintenance-phase)
- [Installation](#installation)
- [Usage](#usage)
- [Features](#features)
- [Project Structure](#project-structure)
- [Technologies Used](#technologies-used)

---

## Project Overview

The **Personal Finance Tracker** is a Python-based application designed to help individuals manage their personal finances by tracking income and expenses, calculating balances, and providing insights into spending patterns by category.

---

## Software Development Life Cycle (SDLC)

This project follows the **Waterfall SDLC Model** with the following phases:

### 1. Planning Phase

**Objective:** Define the project scope, goals, and feasibility.

**Activities:**
- Identified the problem: Many individuals struggle to track their daily income and expenses effectively
- Defined project goals: Create a simple, user-friendly CLI application for personal finance management
- Determined target users: Individuals who want to manage personal finances without complex software
- Established timeline: 2-week development cycle
- Resource allocation: Solo developer project using Python

**Deliverables:**
- Project proposal
- Feasibility study
- Resource allocation plan

---

### 2. Requirements Analysis Phase

**Objective:** Gather and document functional and non-functional requirements.

#### Functional Requirements:
1. **Transaction Management**
   - Add income transactions with category, amount, and description
   - Add expense transactions with category, amount, and description
   - Delete transactions by ID
   - View all transactions

2. **Financial Reporting**
   - Calculate and display current balance (income - expenses)
   - Generate category-wise expense summary
   - Display transaction history with details

3. **Data Persistence**
   - Store transaction data in JSON format
   - Load previous transactions on application startup
   - Auto-save after each transaction modification

#### Non-Functional Requirements:
- **Usability:** Simple command-line interface with clear menu options
- **Performance:** Fast data retrieval and calculations (< 1 second for operations)
- **Reliability:** Data integrity through proper file handling and error management
- **Maintainability:** Clean, modular code structure with proper documentation
- **Portability:** Cross-platform compatibility (Windows, Linux, macOS)

**Deliverables:**
- Software Requirements Specification (SRS) document
- Use case diagrams
- User stories

---

### 3. Design Phase

**Objective:** Create the system architecture and detailed design.

#### System Architecture:

```
┌─────────────────────────────────────┐
│     FinanceTrackerUI (View)        │
│   - display_menu()                  │
│   - add_income()                    │
│   - add_expense()                   │
│   - view_all_transactions()         │
│   - view_balance()                  │
│   - view_category_summary()         │
│   - delete_transaction()            │
│   - run()                           │
└──────────────┬──────────────────────┘
               │
               │ uses
               ↓
┌─────────────────────────────────────┐
│   FinanceManager (Controller)       │
│   - load_transactions()             │
│   - save_transactions()             │
│   - add_transaction()               │
│   - delete_transaction()            │
│   - get_all_transactions()          │
│   - get_transactions_by_type()      │
│   - calculate_balance()             │
│   - get_category_summary()          │
└──────────────┬──────────────────────┘
               │
               │ manages
               ↓
┌─────────────────────────────────────┐
│      Transaction (Model)            │
│   - transaction_id: int             │
│   - transaction_type: str           │
│   - category: str                   │
│   - amount: float                   │
│   - description: str                │
│   - date: str                       │
│   + to_dict()                       │
│   + from_dict()                     │
└─────────────────────────────────────┘
```

#### Class Design:

**1. Transaction Class**
- Attributes: transaction_id, transaction_type, category, amount, description, date
- Methods: to_dict(), from_dict()

**2. FinanceManager Class**
- Attributes: data_file, transactions, next_transaction_id
- Methods: load_transactions(), save_transactions(), add_transaction(), delete_transaction(), get_all_transactions(), get_transactions_by_type(), calculate_balance(), get_category_summary()

**3. FinanceTrackerUI Class**
- Attributes: manager
- Methods: display_menu(), add_income(), add_expense(), view_all_transactions(), view_balance(), view_category_summary(), delete_transaction(), run()

#### Data Model:

**JSON File Structure (finance_data.json):**
```json
{
  "transactions": [
    {
      "transaction_id": 1,
      "transaction_type": "income",
      "category": "Salary",
      "amount": 5000.0,
      "description": "Monthly salary",
      "date": "2025-01-22 10:30:00"
    }
  ],
  "next_id": 2
}
```

**Deliverables:**
- System architecture diagram
- Class diagrams
- Database schema (JSON structure)
- UI mockups/wireframes

---

### 4. Implementation Phase

**Objective:** Convert design into working code.

#### Development Environment:
- **Language:** Python 3.8+
- **Libraries:** json, os, datetime, typing
- **IDE:** Any Python IDE (VS Code, PyCharm, etc.)
- **Version Control:** Git

#### Implementation Details:

**Transaction Class Implementation:**
- Encapsulates individual transaction data
- Provides serialization methods (to_dict, from_dict) for JSON storage
- Automatically timestamps transactions

**FinanceManager Class Implementation:**
- Implements singleton-like pattern for data management
- Handles all CRUD operations on transactions
- Manages file I/O operations
- Implements business logic for balance calculation and category summaries

**FinanceTrackerUI Class Implementation:**
- Provides menu-driven interface
- Handles user input validation
- Displays formatted output
- Orchestrates calls to FinanceManager

#### Coding Standards:
- PEP 8 compliance for Python code style
- Type hints for better code documentation
- Docstrings for all classes and methods
- Descriptive variable and function names

**Deliverables:**
- Source code (finance_tracker.py)
- Code documentation
- Version control commits

---

### 5. Testing Phase

**Objective:** Verify the application works correctly and meets requirements.

#### Test Cases:

**Unit Testing:**

| Test Case ID | Test Scenario | Input | Expected Output | Status |
|-------------|---------------|-------|-----------------|--------|
| TC001 | Add income transaction | Type: income, Category: Salary, Amount: 5000 | Transaction created with ID | ✓ Pass |
| TC002 | Add expense transaction | Type: expense, Category: Food, Amount: 50 | Transaction created with ID | ✓ Pass |
| TC003 | Calculate balance | Income: 5000, Expenses: 200 | Balance: 4800 | ✓ Pass |
| TC004 | Delete transaction | Transaction ID: 1 | Transaction removed | ✓ Pass |
| TC005 | Delete non-existent transaction | Transaction ID: 999 | Error message displayed | ✓ Pass |
| TC006 | Load transactions from file | Existing finance_data.json | All transactions loaded | ✓ Pass |
| TC007 | Save transactions to file | Add new transaction | Data persisted to JSON | ✓ Pass |
| TC008 | View category summary | Multiple expenses | Categories with totals | ✓ Pass |

**Integration Testing:**
- Verified UI correctly interacts with FinanceManager
- Tested data persistence across application restarts
- Validated transaction flow from input to storage

**System Testing:**
- End-to-end testing of all features
- User acceptance testing with sample scenarios
- Cross-platform testing (Windows, Linux, macOS)

**Error Handling Testing:**
- Invalid input handling (non-numeric amounts, empty fields)
- File corruption scenarios
- Edge cases (empty transaction list, zero balance)

**Deliverables:**
- Test cases document
- Test execution reports
- Bug reports and fixes

---

### 6. Deployment Phase

**Objective:** Make the application available for use.

#### Deployment Strategy:

**Local Deployment:**
1. Clone repository from GitHub
2. Ensure Python 3.8+ is installed
3. Run the application: `python finance_tracker.py`

**GitHub Repository Setup:**
- Repository name: personal-finance-tracker
- README.md with installation and usage instructions
- LICENSE file (MIT License)
- .gitignore for Python projects

**Deliverables:**
- GitHub repository
- README.md
- Installation guide
- User manual

---

### 7. Maintenance Phase

**Objective:** Provide ongoing support and improvements.

#### Maintenance Activities:

**Corrective Maintenance:**
- Bug fixes based on user reports
- Error handling improvements
- Data validation enhancements

**Adaptive Maintenance:**
- Python version compatibility updates
- Operating system compatibility fixes

**Perfective Maintenance:**
- Performance optimizations
- UI/UX improvements
- Code refactoring

**Preventive Maintenance:**
- Code review and quality checks
- Security audits
- Documentation updates

#### Future Enhancements:
1. **Data Visualization:** Add charts and graphs for expense trends
2. **Budget Management:** Set monthly budgets per category with alerts
3. **Export Functionality:** Export data to CSV or PDF
4. **Multi-user Support:** User authentication and multiple profiles
5. **Recurring Transactions:** Support for automatic monthly bills
6. **Search and Filter:** Advanced search by date range, category, amount
7. **Currency Support:** Multi-currency transactions with conversion
8. **Mobile App:** Develop mobile version for iOS and Android

**Deliverables:**
- Bug fix releases
- Feature updates
- Updated documentation

---

## Installation

### Prerequisites
- Python 3.8 or higher

### Steps

1. Clone the repository:
```bash
git clone https://github.com/yourusername/personal-finance-tracker.git
cd personal-finance-tracker
```

2. Run the application:
```bash
python finance_tracker.py
```

---

## Usage

### Starting the Application

Run the main script:
```bash
python finance_tracker.py
```

### Menu Options

1. **Add Income:** Record income transactions (salary, freelance work, etc.)
2. **Add Expense:** Record expense transactions (food, transport, bills, etc.)
3. **View All Transactions:** Display complete transaction history
4. **View Balance:** See total income, expenses, and current balance
5. **View Category Summary:** Analyze spending by category
6. **Delete Transaction:** Remove a transaction by its ID
7. **Exit:** Close the application

### Example Workflow

```
1. Select "Add Income" → Enter category: "Salary", amount: 5000, description: "January salary"
2. Select "Add Expense" → Enter category: "Food", amount: 150, description: "Groceries"
3. Select "View Balance" → See current balance: $4850
4. Select "View Category Summary" → See expense breakdown by category
```

---

## Features

✅ **Transaction Management**
- Add, view, and delete income and expense transactions
- Automatic timestamp for each transaction
- Unique transaction IDs

✅ **Financial Analysis**
- Real-time balance calculation
- Category-wise expense breakdown
- Comprehensive transaction history

✅ **Data Persistence**
- JSON-based storage
- Automatic data saving
- Data recovery on application restart

✅ **User-Friendly Interface**
- Clear menu-driven navigation
- Formatted table displays
- Input validation and error handling

---

## Project Structure

```
personal-finance-tracker/
│
├── finance_tracker.py       # Main application file
├── finance_data.json        # Auto-generated data storage file
├── README.md                # Project documentation
└── .gitignore              # Git ignore file
```

---

