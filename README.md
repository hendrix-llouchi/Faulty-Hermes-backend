# 🦅 Faulty Hermes Backend

The robust backend infrastructure for the Faulty Hermes ecosystem. This platform is engineered for high-performance communication, utilizing a modern Django architecture integrated with PostgreSQL.

## ✨ Features

- **🛡️ Secure Architecture**: Environment-based configuration using `python-dotenv`.
- **👤 User Profiles**: Extended user management with the `UserProfile` system.
- **⚡ RESTful API**: Built with Django REST Framework for seamless frontend integration.
- **🐘 Database Power**: Full PostgreSQL integration for reliable data management.
- **🗣️ Universal Chat**: A built-in chat engine seamlessly equipped with auto-translations between users via the Google Gemini AI.
- **🏆 Leaderboards**: A high-score tracker natively listing users by their accumulated game XP.

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

# Translation APIs
GEMINI_API_KEY=your_gemini_api_key_here
```

### 3. Install & Migrate
```powershell
# Install dependencies
.\venv\Scripts\pip.exe install -r requirements.txt

# Apply database migrations
.\venv\Scripts\python.exe manage.py migrate
```

### 4. API Endpoints of Note
- `POST /api/v1/users/register/` -> Requires a `target_lang` payload to create a Universal Chat profile.
- `GET /api/v1/users/leaderboard/` -> Fetches the top 10 users ranked by XP descending.
- `GET/POST /api/v1/chat/messages/` -> Sends and retrieves localized chat items.

### 5. Launch
```powershell
.\venv\Scripts\python.exe manage.py runserver
```
Visit the API at `http://127.0.0.1:8000/`.

---

## 📂 Project Structure

- `core/` - Project engine, utils (holds AI translate logic), settings, and routing.
- `users/` - Authentication, Extended User Profiles, and Leaderboard logic.
- `chat/` - Message models, endpoints, and automatic Google Gemini Translation signals.
- `lessons/` - Content models handling languages, modules, lessons, and exercises.
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