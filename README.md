# 🦅 Faulty Hermes Backend

The robust backend infrastructure for the Faulty Hermes ecosystem. This platform is engineered for high-performance multilingual communication, utilizing a modern Django architecture integrated with PostgreSQL and Google Gemini AI-powered translation.

---

## ✨ What's Been Built

### 👤 User System
- **Registration & Profiles** — Users sign up with a username, email, password, and target language
- **Target Language Profiles** — Each user has a `target_lang` stored on their profile that drives personalized translations
- **User Listing API** — Real-time list of all registered users for the chat interface

### 💬 Chat Engine
- **Message API** — Full send/receive message support via REST
- **Auto-Translation** — Every message is automatically translated into the **recipient's target language** using Google Gemini AI the moment it is saved (via Django signals)
- **Conversation Filtering** — The frontend displays only messages between two specific users, not global broadcasts

### 🤝 Contacts / Friends System *(New)*
- **`GET /api/v1/users/new/?username=X`** — Returns all users X has **not yet added**, newest first (used to show the "New People" panel)
- **`GET /api/v1/users/contacts/?username=X`** — Returns X's confirmed contact list
- **`POST /api/v1/users/contacts/`** — Adds a contact by username. Once added, they appear in the chat sidebar

### 🌐 Network Access
- The server is designed to run on `0.0.0.0:8000` so all devices on the local network can connect
- CORS is configured to allow the Vite frontend origin

---

## 🚀 Quick Start

### 1. Clone & Environment
```powershell
git clone https://github.com/hendrix-llouchi/Faulty-Hermes-backend.git
cd Faulty-Hermes-backend

# Create virtual environment
python -m venv venv
.\venv\Scripts\Activate.ps1
```

### 2. Configure Environment Variables
Create a `.env` file in the root directory (never commit this):
```env
DB_NAME=hermes_db
DB_USER=hermes_user
DB_PASSWORD=your_secure_password
DB_HOST=localhost
DB_PORT=5432
SECRET_KEY=your_django_secret_key
DEBUG=True

# Google Gemini AI for chat translation
GEMINI_API_KEY=your_gemini_api_key_here
```

### 3. Install & Migrate
```powershell
.\venv\Scripts\pip.exe install -r requirements.txt
.\venv\Scripts\python.exe manage.py migrate
```

### 4. Run (Network-accessible)
```powershell
# Expose to your local network (required for multi-device testing)
.\venv\Scripts\python.exe manage.py runserver 0.0.0.0:8000
```
Visit the API at `http://YOUR_LOCAL_IP:8000/` (find your IP with `ipconfig`).

---

## 📡 API Reference

| Method | Endpoint | Description |
|:---|:---|:---|
| `POST` | `/api/v1/users/register/` | Create a new user account |
| `GET` | `/api/v1/users/` | List all registered users |
| `PATCH` | `/api/v1/users/profile/` | Update user's target language |
| `GET` | `/api/v1/users/contacts/?username=X` | Get X's contact list |
| `POST` | `/api/v1/users/contacts/` | Add a new contact |
| `GET` | `/api/v1/users/new/?username=X` | Get users not yet added by X |
| `GET` | `/api/v1/users/leaderboard/` | Top 10 users by XP |
| `GET/POST` | `/api/v1/chat/messages/` | Send and retrieve chat messages |
| `POST` | `/api/v1/auth/token/` | Obtain JWT token pair |
| `POST` | `/api/v1/auth/token/refresh/` | Refresh JWT access token |

---

## 📂 Project Structure

```
Faulty-Hermes-backend/
├── core/           # Project engine — settings, routing, Gemini translate utils
├── users/          # User profiles, contacts system, leaderboard, registration
├── chat/           # Message model, send/receive API, auto-translation signals
├── lessons/        # Content models: languages, modules, lessons, exercises
├── requirements.txt
├── .env            # 🔒 Secret config — never committed (in .gitignore)
└── .env.example    # Safe template for new contributors
```

---

## 🛠 Tech Stack

| Technology | Purpose |
| :--- | :--- |
| **Django 5.1** | Core Backend Framework |
| **Django REST Framework** | API Layer |
| **PostgreSQL** | Primary Relational Database |
| **Google Gemini AI** | Real-time Message Translation |
| **Simple JWT** | Token-based Auth |
| **django-cors-headers** | Cross-Origin Frontend Access |
| **Python Dotenv** | Secrets Management |

---

## 🔒 Security Notes

- All secrets (`SECRET_KEY`, `DB_PASSWORD`, `GEMINI_API_KEY`) are stored in `.env` — **never committed to Git**
- `.gitignore` excludes `.env`, `venv/`, `__pycache__/`, and `db.sqlite3`
- For production, set `DEBUG=False` and restrict `ALLOWED_HOSTS`

---

## 💡 Troubleshooting

### VS Code Import Errors
These are false positives from the IDE not finding the venv packages. The server runs fine:
1. `Ctrl+Shift+P` → **Python: Select Interpreter**
2. Choose `.\venv\Scripts\python.exe`
3. Reload window if necessary.

### "Network error" on sign-up
Make sure the server is running with `0.0.0.0:8000` (not just `127.0.0.1:8000`), and that the frontend `.env` points to your machine's local IP address.

---

© 2026 Faulty Hermes Team