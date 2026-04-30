# Secure E-Commerce Dropshipping Website

## Overview
This project is a secure Business-to-Customer (B2C) dropshipping web application built with a 3-tier architecture (Frontend, Backend, Database).

The platform allows users to:
- Create accounts with email verification
- Log in with Multi-Factor Authentication (MFA)
- Browse a product catalogue
- Add items to cart
- Simulate checkout with Stripe sandbox
- View order history

## Tech Stack
- Frontend: HTML, CSS, JavaScript
- Backend: Python (Flask)
- Database: SQLite / Render DB
- Deployment: Render
- Security: MFA, email verification, hashed passwords

## Features
- Secure authentication (email verification + MFA)
- Order tracking system
- Stripe sandbox payment simulation
- Environment variable protection for sensitive data
- Basic protection against common vulnerabilities

## Security Focus
This project addresses:
- SQL Injection (via server-side validation)
- XSS prevention
- Secure password handling (hashing)
- MFA-based authentication
- Secure email handling using environment variables

## Live Demo
https://csce-4560-project.onrender.com/

## How to Run Locally
1. Clone repo
2. Install dependencies:
   pip install -r requirements.txt
3. Run:
   python app.py

## Contributors
- Nithin Arya Inturi
- Team Members

## Notes
This project was developed as part of CSCE 4560 with a focus on secure system design and vulnerability mitigation.
