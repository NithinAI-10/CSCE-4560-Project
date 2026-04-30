# SecureShop — Secure E-Commerce Platform

A full-stack B2C dropshipping web application built with security-first design principles. Developed as a capstone project for **CSCE 4560: Introduction to Computer Security** at the University of North Texas.

🔗 **Live Demo:** [csce-4560-project.onrender.com](https://csce-4560-project.onrender.com)

---

## Overview

SecureShop demonstrates how real-world web vulnerabilities can be mitigated through secure development practices. The platform supports end-to-end shopping functionality — from account creation with email verification, to MFA-protected login, product browsing, cart management, and simulated Stripe checkout — with security controls implemented at every layer.

---

## Tech Stack

| Layer | Technology |
|---|---|
| Frontend | HTML, CSS, JavaScript |
| Backend | Python (Flask) |
| Database | SQLite / Render PostgreSQL |
| Deployment | Render |
| Payments | Stripe (sandbox) |
| Auth | Email verification + TOTP-style MFA |

---

## Features

- **Account registration** with email verification via tokenized link
- **Multi-Factor Authentication (MFA)** on every login — time-limited tokens sent to email
- **Hashed passwords** using PBKDF2-SHA256 via Werkzeug
- **Stripe sandbox checkout** for payment simulation
- **Order history** — users can view past orders and line items
- **Environment variable protection** for all sensitive credentials
- **Parameterized SQL queries** throughout — no raw string interpolation

---

## Security Controls

| Threat | Mitigation |
|---|---|
| SQL Injection | Parameterized queries via SQLite3 |
| XSS | Server-side output escaping via Jinja2 |
| Credential exposure | Passwords hashed with PBKDF2:SHA256 |
| Account takeover | MFA tokens expire after 5 minutes |
| Secret leakage | All credentials stored in environment variables |
| Unverified access | Email must be verified before login is permitted |

---

## Architecture

```
┌─────────────────────────────────────────────────────┐
│                    Frontend (HTML/JS)                │
│         Register · Login · Shop · Cart · Orders      │
└──────────────────────┬──────────────────────────────┘
                       │ HTTP/JSON
┌──────────────────────▼──────────────────────────────┐
│                Flask Backend (app.py)                │
│   /register  /login  /mfa/*  /checkout  /orders     │
└──────────┬───────────────────────────┬──────────────┘
           │                           │
┌──────────▼──────────┐   ┌────────────▼──────────────┐
│   SQLite / Render   │   │       Gmail SMTP           │
│   users · orders    │   │  Verification + MFA email  │
│   mfa · order_items │   └───────────────────────────┘
└─────────────────────┘
```

---

## Getting Started

### Prerequisites

- Python 3.8+
- pip

### Installation

```bash
# 1. Clone the repo
git clone https://github.com/NithinAI-10/CSCE-4560-Project.git
cd CSCE-4560-Project

# 2. Create and activate a virtual environment (recommended)
python -m venv venv
source venv/bin/activate        # macOS/Linux
venv\Scripts\activate           # Windows

# 3. Install dependencies
pip install -r requirements.txt

# 4. Set environment variables
cp .env.example .env
# Edit .env with your credentials (see below)

# 5. Run the app
python app.py
```

### Environment Variables

Create a `.env` file in the project root (never commit this file):

```env
WEBSITE_EMAIL=your-email@gmail.com
WEBSITE_EMAIL_PASSWORD=your-app-password
WEBSITE_URL=http://localhost:5000
```

> **Note:** Use a [Gmail App Password](https://support.google.com/accounts/answer/185833), not your regular Gmail password.

---

## Project Structure

```
CSCE-4560-Project/
├── app.py              # Flask application — routes, auth, checkout logic
├── requirements.txt    # Python dependencies
├── templates/          # Jinja2 HTML templates
│   ├── index.html
│   └── ...
├── .gitignore
└── README.md
```

---

## Known Limitations

This is an academic project. The following are known gaps that would need to be addressed before production use:

- No server-side session — `user_id` is currently trusted from the client on checkout/orders endpoints
- No rate limiting on login or MFA endpoints (brute-force risk)
- No CSRF protection
- SQLite is used locally; Render provides a Postgres connection in production

---

## Contributors

- **Nithin Arya Inturi** — [@NithinAI-10](https://github.com/NithinAI-10)
- **Ryan Contreras** — [@RyanContreras2539](https://github.com/RyanContreras2539)
- **Jesus D Barco** — [@AstrialTrinity](https://github.com/AstrialTrinity)
- **Catcher Jones** — [@CatcherJones](https://github.com/CatcherJones)

---

## License

This project was developed for educational purposes as part of CSCE 4560 at UNT. Not licensed for production use without additional security hardening.
