FINANCIALTRACKER
 Full-Stack Web ApplicationA complete full-stack web application built with Python and Flask. It allows users to create secure accounts to track personal expenses and monitor the real-time value and performance of their stock portfolio, with a focus on the Indian stock market (NSE).
 Core Features-- Secure User Authentication: Full signup, login, and logout functionality with password hashing.
   Personalized Data: Each user can only see and manage their own private financial data.Expense Tracking: 
   Full CRUD (Create, Read, Delete) functionality for personal expenses.
   Live Stock Portfolio:Add stocks from the National Stock Exchange (NSE).Live price data is fetched from the Alpha Vantage API.Calculates real-time portfolio value, cost basis, and profit/loss.
   Dynamic Autocomplete: A user-friendly search feature suggests NSE stock symbols and company names as you type.
   Data Validation: Robust frontend and backend validation to ensure data integrity.
   User Feedback: Professional flash messages to confirm user actions.
   Project Journey & Learning Curve -- This project was built from the ground up as a step-by-step learning journey. The process began with foundational data analysis of CSV files, which evolved into a simple Flask web application. 
Key milestones included:
  Backend Development: Building the initial Flask server and routing.
  Database Integration: Moving from temporary in-memory storage to a permanent SQLite database with Flask-SQLAlchemy.
  Full CRUD Functionality: Implementing the core features to create, read, and delete expenses and stocks.
  User Authentication: Architecting a secure, multi-user system with password hashing and session management.
  API Integration: Connecting to a live, third-party API (Alpha Vantage) to fetch real-world financial data.
  Deployment: Taking the application from a local development server to a live, public website hosted on PythonAnywhere.Throughout this process, a significant emphasis was placed on debugging and problem-solving, tackling common but complex issues related to database initialization, server configuration (WSGI), and dependency management in a live production environment.
Tech StackBackend: Python, Flask, Flask-SQLAlchemy, Flask-LoginDatabase: SQLiteFrontend: HTML, CSS, JavaScriptLibraries: Pandas, RequestsAPIs: Alpha Vantage API for live stock dataLocal Setup 
cd FinancialTracker
private URL: http://127.0.0.1:5000
<img width="911" height="612" alt="Screenshot 2025-09-15 051420" src="https://github.com/user-attachments/assets/dc8788fb-1a1c-4a72-913e-843bc049404e" />
<img width="1717" height="960" alt="Screenshot 2025-09-15 051404" src="https://github.com/user-attachments/assets/c1d407e5-52aa-4bc5-a9c4-d30498cf5e1a" />
Author & ContactFor any questions or collaboration inquiries, please feel free to reach out.Email: anuraganand638@gmail.com
