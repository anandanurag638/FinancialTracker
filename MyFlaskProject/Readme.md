FinancialTracker
A full-stack financial dashboard built with Python and Flask. This application provides users with a secure, personal space to track their daily expenses and monitor a live stock portfolio, with a focus on companies listed on the Indian National Stock Exchange (NSE).

Live Demo
A live, deployed version of this application can be accessed at:
http://anura.pythonanywhere.com

Key Features
Secure User Accounts: Full signup and login functionality with hashed passwords for security. Each user's data is private and linked to their account.

Expense Tracking: Complete CRUD (Create, Read, Delete) functionality for managing personal expenses.

Live Stock Portfolio: Track stock holdings with real-time price data fetched from the Alpha Vantage API. The dashboard calculates and displays current value, total cost basis, and profit/loss.

Autocomplete Search: A dynamic search bar suggests NSE stock symbols and company names as the user types, powered by a cached, comprehensive list of all traded companies.

Data Validation: Both frontend (HTML) and backend (Python) validation are in place to prevent the submission of invalid data, ensuring application robustness.

User Feedback: Professional flash messages provide clear confirmation for actions like adding/deleting items or logging in/out.

Tech Stack
Backend: Python, Flask, Flask-SQLAlchemy, Flask-Login

Database: SQLite

Frontend: HTML, CSS, JavaScript

Libraries: Pandas, Requests
