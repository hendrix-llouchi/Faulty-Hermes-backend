# Faulty Hermes Backend

The backend infrastructure for the Hermes project. Built with Django and designed for scalability.

## 🚀 Getting Started

Follow these steps to set up the project locally.

### 1. Environment Setup

It is recommended to use a virtual environment to manage dependencies.

```powershell
# Create a virtual environment
python -m venv venv

# Activate the virtual environment
.\venv\Scripts\activate
```

### 2. Install Dependencies

Install the required Python packages:

```powershell
pip install -r requirements.txt
```

### 3. Database Initialization

Run the migrations to set up your local SQLite database:

```powershell
python manage.py migrate
```

### 4. Run the Development Server

Start the server:

```powershell
python manage.py runserver
```

The API will be accessible at `http://127.0.0.1:8000/`.

## 🛠 Tech Stack

- **Framework:** Django
- **API Support:** Django REST Framework
- **Asynchronous Support:** Django Channels (setup in progress)
- **Database:** PostgreSQL (Production) / SQLite (Local)
- **Caching/Message Broker:** Redis

## 📂 Project Structure

- `core/` - Project settings, URLs, and ASGI/WSGI configuration.
- `requirements.txt` - Project dependencies.
- `manage.py` - Django management CLI.