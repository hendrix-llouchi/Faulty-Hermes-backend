# 🦅 Faulty Hermes Backend

The robust backend infrastructure for the Faulty Hermes ecosystem. This platform is engineered for high-performance communication, utilizing a modern Django architecture integrated with PostgreSQL.

## ✨ Features

- **🛡️ Secure Architecture**: Environment-based configuration using `python-dotenv`.
- **👤 User Profiles**: Extended user management with the `UserProfile` system.
- **⚡ RESTful API**: Built with Django REST Framework for seamless frontend integration.
- **🐘 Database Power**: Full PostgreSQL integration for reliable data management.

---

## 🚀 Quick Start

### 1. Clone & Environment
```powershell
git clone https://github.com/hendrix-llouchi/Faulty-Hermes-backend.git
cd Faulty-Hermes-backend

# Create virtual environment
python -m venv venv
```

### 2. Configure Environment Variables
Create a `.env` file in the root directory:
```env
DB_NAME=hermes_db
DB_USER=hermes_user
DB_PASSWORD=your_secure_password
DB_HOST=localhost
DB_PORT=5432
SECRET_KEY=your_django_secret_key
DEBUG=True
```

### 3. Install & Migrate
```powershell
# Install dependencies
.\venv\Scripts\pip.exe install -r requirements.txt

# Apply database migrations
.\venv\Scripts\python.exe manage.py migrate
```

### 4. Launch
```powershell
.\venv\Scripts\python.exe manage.py runserver
```
Visit the API at `http://127.0.0.1:8000/`.

---

## 📂 Project Structure

- `core/` - Project engine, settings, and routing.
- `users/` - Authentication and User Profile management.
- `requirements.txt` - Python ecosystem dependencies.
- `.gitignore` - Standard protections for `.env` and `venv/`.

---

## 🛠 Tech Stack

| Technology | Purpose |
| :--- | :--- |
| **Django 5.2** | Core Backend Framework |
| **Django REST Framework** | API Layer |
| **PostgreSQL** | Primary Relational Database |
| **Python Dotenv** | Configuration Security |

---

## 💡 Troubleshooting

### VS Code Import Errors
If your IDE marks imports as errors:
1. `Ctrl+Shift+P` -> **Python: Select Interpreter**
2. Choose `.\venv\Scripts\python.exe`.
3. Reload window if necessary.

---
© 2026 Faulty Hermes Team