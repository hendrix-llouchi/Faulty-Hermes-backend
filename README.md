# 🦅 Faulty Hermes Backend

The robust backend infrastructure for the Faulty Hermes language-learning ecosystem. Engineered for high-performance communication, utilizing a modern Django architecture integrated with PostgreSQL, JWT authentication, and a real-time XP progression system.

---

## ✨ Features

- **🔐 JWT Authentication**: Secure stateless auth via `djangorestframework-simplejwt` with 1-day access tokens.
- **👤 User Registration & Profiles**: Auto-created `UserProfile` linked to every Django `User` via signals.
- **📚 Lessons API**: Full content tree — Languages → Modules → Lessons → Exercises.
- **📈 Progress Tracking**: Log lesson completions per user with duplicate-safe `get_or_create` logic.
- **⚡ XP System**: Automatically awards `xp_reward` from a completed lesson to the user's profile via Django signals. XP is granted only once per lesson to prevent farming.
- **🛡️ Secure Configuration**: Environment-based secrets using `python-dotenv`.
- **🐘 PostgreSQL Integration**: Full relational database support via `psycopg2-binary`.
- **🔥 Firebase Ready**: `firebase_admin` integrated for future Firebase auth and storage.

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
SECRET_KEY=your_django_secret_key
DEBUG=True
ALLOWED_HOSTS=

DB_NAME=hermes_db
DB_USER=hermes_user
DB_PASSWORD=your_secure_password
DB_HOST=localhost
DB_PORT=5432
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

```
Faulty-Hermes-backend/
├── core/               # Project settings, root URLs, WSGI/ASGI
├── users/              # User registration, UserProfile model, signals
│   ├── models.py       # UserProfile (OneToOne → User)
│   ├── serializers.py  # UserRegistrationSerializer
│   ├── views.py        # RegisterView
│   ├── urls.py         # api/v1/users/
│   ├── signals.py      # Auto-create profile + XP award on lesson completion
│   └── apps.py         # Registers signals via ready()
├── lessons/            # Content tree and progress tracking
│   ├── models.py       # Language, Module, Lesson, Exercise, UserProgress
│   ├── serializers.py  # Nested serializers + UserProgressSerializer
│   ├── views.py        # ViewSets + LogProgressView
│   ├── urls.py         # Router URLs + progress/ path
│   └── admin.py        # All models registered
├── requirements.txt
├── .gitignore
└── .env                # (not committed)
```

---

## 🌐 API Endpoints

### Auth
| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| `POST` | `api/v1/auth/login/` | None | Obtain JWT access + refresh tokens |
| `POST` | `api/v1/auth/refresh/` | None | Refresh an access token |

### Users
| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| `POST` | `api/v1/users/register/` | None | Register a new user account |

### Lessons (read-only)
| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| `GET` | `api/v1/languages/` | Optional | List all languages with full content tree |
| `GET` | `api/v1/modules/` | Optional | List all modules with lessons |
| `GET` | `api/v1/lessons/` | Optional | List all lessons with exercises |
| `GET` | `api/v1/exercises/` | Optional | List all exercises |

### Progress
| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| `POST` | `api/v1/progress/` | ✅ Bearer token | Log a lesson as completed & award XP |

**Progress request body:**
```json
{ "lesson_id": 1 }
```
**Response:** `201 Created` on first completion, `200 OK` if already logged.

---

## 🛠 Tech Stack

| Technology | Version | Purpose |
| :--- | :--- | :--- |
| **Django** | 5.2 | Core backend framework |
| **Django REST Framework** | 3.16 | API layer |
| **djangorestframework-simplejwt** | 5.5 | JWT authentication |
| **PostgreSQL** | — | Primary relational database |
| **psycopg2-binary** | 2.9 | PostgreSQL driver |
| **python-dotenv** | 1.2 | Environment variable management |
| **firebase-admin** | 7.2 | Firebase integration (auth/storage) |
| **channels** | 4.3 | WebSocket / async support |
| **redis** | 7.2 | Channel layer backend |

---

## 💡 Troubleshooting

### VS Code Import Errors
If your IDE marks imports as errors:
1. `Ctrl+Shift+P` → **Python: Select Interpreter**
2. Choose `.\venv\Scripts\python.exe`
3. Reload the window if necessary.

### ModuleNotFoundError for simplejwt
If `rest_framework_simplejwt` is not found when running with the venv, the package may have installed to the system Python instead of the venv. Install it explicitly:
```powershell
.\venv\Scripts\pip.exe install djangorestframework-simplejwt
```

---

© 2026 Faulty Hermes Team