# ✅ IMPLEMENTED.md — Faulty Hermes Backend

> A full audit of every component implemented in the `feature/implementation` branch as of **February 28, 2026**.

---

## 📦 1. Project Configuration (`core/`)

### `core/settings.py`

| Setting | Value |
|---|---|
| Django version | 5.2.11 |
| Database | PostgreSQL via `psycopg2-binary` |
| Secret key | Read from `.env` via `python-dotenv` |
| Debug flag | Read from `.env`, defaults to `True` |
| Allowed hosts | Read from `.env`, comma-separated |
| Default auto field | `BigAutoField` |

**JWT Configuration added:**
```python
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
}

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(days=1),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),
    'ROTATE_REFRESH_TOKENS': False,
    'BLACKLIST_AFTER_ROTATION': False,
    'AUTH_HEADER_TYPES': ('Bearer',),
}
```

**Installed apps:** `rest_framework`, `users`, `lessons`

---

### `core/urls.py`

Root URL configuration with all top-level routes registered:

```
admin/                          → Django admin panel
api/v1/                         → lessons.urls (router)
api/v1/users/                   → users.urls
api/v1/auth/login/              → TokenObtainPairView
api/v1/auth/refresh/            → TokenRefreshView
```

---

## 👤 2. Users App (`users/`)

### `users/models.py` — `UserProfile`

Extended profile model linked to Django's built-in `User` via a `OneToOneField`.

| Field | Type | Notes |
|---|---|---|
| `user` | `OneToOneField(User)` | `on_delete=CASCADE`, `related_name='profile'` |
| `firebase_uid` | `CharField(128)` | `unique=True`, `null=True`, `blank=True` — for future Firebase auth |
| `bio` | `TextField` | Optional |
| `profile_photo_url` | `URLField` | Optional |
| `interests` | `JSONField` | Defaults to `[]` |
| `streak_days` | `IntegerField` | Defaults to `0` |
| `xp` | `IntegerField` | Defaults to `0` — incremented by signal |

---

### `users/serializers.py` — `UserRegistrationSerializer`

Handles new user creation via DRF's `ModelSerializer`.

- **Fields exposed:** `id`, `username`, `email`, `password` (write-only)
- **Password minimum length:** 8 characters
- **`validate_email`:** Rejects duplicate email addresses with a `ValidationError`
- **`create()`:** Hashes the password with `make_password()` before saving — plain-text passwords are never stored

---

### `users/views.py` — `RegisterView`

```python
class RegisterView(generics.CreateAPIView):
    serializer_class = UserRegistrationSerializer
    permission_classes = [AllowAny]
```

- Handles `POST api/v1/users/register/`
- Open to unauthenticated users (`AllowAny`)
- Delegates all logic to `UserRegistrationSerializer`

---

### `users/urls.py`

```
register/   → RegisterView
```

---

### `users/signals.py` — Two Signal Receivers

#### Signal 1: `create_user_profile`
- **Trigger:** `post_save` on `User`, `created=True`
- **Action:** Automatically calls `UserProfile.objects.create(user=instance)`
- **Effect:** Every registered user gets a `UserProfile` created instantly and transparently

#### Signal 2: `award_xp_on_lesson_completion`
- **Trigger:** `post_save` on `lessons.UserProgress`, `created=True`
- **Action:** Reads `instance.lesson.xp_reward` and runs an atomic `UPDATE` on the user's `UserProfile.xp`
- **Anti-farming guard:** The `created` flag is `True` only when the `UserProgress` row is first inserted. Since `LogProgressView` uses `get_or_create`, repeated calls for the same lesson return `created=False` — XP is awarded **exactly once per lesson**
- **Atomic XP update:** Uses `models.F('xp') + xp_reward` to perform the increment at the database level, preventing race conditions

```python
UserProfile.objects.filter(user=instance.user).update(
    xp=models.F('xp') + xp_reward
)
```

---

### `users/apps.py` — Signal Registration

```python
class UsersConfig(AppConfig):
    def ready(self):
        import users.signals  # noqa: F401
```

Ensures both signals are registered as soon as Django loads the `users` app.

---

## 📚 3. Lessons App (`lessons/`)

### `lessons/models.py` — Content Tree + Progress

#### `Language`
| Field | Type | Notes |
|---|---|---|
| `name` | `CharField(100)` | `unique=True` |
| `code` | `CharField(10)` | `unique=True` — e.g. `'es'` for Spanish |

#### `Module`
| Field | Type | Notes |
|---|---|---|
| `language` | `ForeignKey(Language)` | `related_name='modules'` |
| `title` | `CharField(200)` | |
| `order` | `IntegerField` | Defaults to `0` |
| `description` | `TextField` | Optional |

#### `Lesson`
| Field | Type | Notes |
|---|---|---|
| `module` | `ForeignKey(Module)` | `related_name='lessons'` |
| `title` | `CharField(200)` | |
| `order` | `IntegerField` | Defaults to `0` |
| `xp_reward` | `IntegerField` | Defaults to `10` — awarded on completion |

#### `Exercise`
| Field | Type | Notes |
|---|---|---|
| `lesson` | `ForeignKey(Lesson)` | `related_name='exercises'` |
| `type` | `CharField` | Choices: `translate`, `mcq`, `fill` |
| `question` | `TextField` | |
| `answer` | `TextField` | |
| `options` | `JSONField` | For MCQ choices, defaults to `{}` |

#### `UserProgress`
| Field | Type | Notes |
|---|---|---|
| `user` | `ForeignKey(User)` | `related_name='progress'` |
| `lesson` | `ForeignKey(Lesson)` | `related_name='progress'` |
| `is_completed` | `BooleanField` | Defaults to `True` |
| `completed_at` | `DateTimeField` | `auto_now_add=True` — set on creation |

**Constraint:** `unique_together = ('user', 'lesson')` — one record per user/lesson pair

---

### `lessons/serializers.py`

Fully nested read-optimised serializer chain:

```
LanguageSerializer
  └── ModuleSerializer
        └── LessonSerializer
              └── ExerciseSerializer
```

| Serializer | Fields |
|---|---|
| `ExerciseSerializer` | `id`, `type`, `question`, `answer`, `options` |
| `LessonSerializer` | `id`, `title`, `order`, `xp_reward`, `exercises` (nested) |
| `ModuleSerializer` | `id`, `title`, `order`, `description`, `lessons` (nested) |
| `LanguageSerializer` | `id`, `name`, `code`, `modules` (nested) |
| `UserProgressSerializer` | `id`, `lesson`, `is_completed`, `completed_at` (all read-only except `id`) |

---

### `lessons/views.py`

#### Read-only ViewSets (List + Retrieve only)

| ViewSet | Queryset optimisation | Permission |
|---|---|---|
| `LanguageViewSet` | `prefetch_related('modules__lessons__exercises')` | `IsAuthenticatedOrReadOnly` |
| `ModuleViewSet` | `select_related('language')` + `prefetch_related('lessons__exercises')` | `IsAuthenticatedOrReadOnly` |
| `LessonViewSet` | `select_related('module')` + `prefetch_related('exercises')` | `IsAuthenticatedOrReadOnly` |
| `ExerciseViewSet` | `select_related('lesson')` | `IsAuthenticatedOrReadOnly` |

All ViewSets expose only `list` and `retrieve` actions (no create/update/delete via API).

#### `LogProgressView(APIView)`

- **Permission:** `IsAuthenticated` — requires a valid JWT `Bearer` token
- **Method:** `POST`
- **Input:** `{ "lesson_id": <int> }`
- **Logic:**
  1. Validates `lesson_id` is present → `400` if missing
  2. Fetches `Lesson` via `get_object_or_404` → `404` if not found
  3. Calls `UserProgress.objects.get_or_create(user, lesson)` → atomic, safe against duplicates
  4. Returns `201 Created` on first log, `200 OK` on repeat calls
  5. The `post_save` signal fires on creation and awards XP automatically

---

### `lessons/urls.py`

Uses DRF `DefaultRouter` for ViewSets, with `progress/` added manually:

```
languages/          → LanguageViewSet  (list, retrieve)
modules/            → ModuleViewSet    (list, retrieve)
lessons/            → LessonViewSet    (list, retrieve)
exercises/          → ExerciseViewSet  (list, retrieve)
progress/           → LogProgressView  (POST only)
```

---

### `lessons/admin.py`

All models registered with useful list columns and filters:

| Model | `list_display` | `list_filter` |
|---|---|---|
| `Language` | `name`, `code` | — |
| `Module` | `title`, `language`, `order` | `language` |
| `Lesson` | `title`, `module`, `order`, `xp_reward` | `module` |
| `Exercise` | `lesson`, `type` | `type`, `lesson` |
| `UserProgress` | `user`, `lesson`, `is_completed`, `completed_at` | `is_completed`, `lesson` |

---

## 🗄️ 4. Database Migrations

| App | Migration | Description |
|---|---|---|
| `users` | `0001_initial` | Creates `UserProfile` |
| `users` | `0002_...` | Adds `user` OneToOneField, makes `firebase_uid` optional, removes standalone `username` |
| `lessons` | `0001_initial` | Creates `Language`, `Module`, `Lesson`, `Exercise` |
| `lessons` | `0002_userprogress` | Creates `UserProgress` |

All migrations applied to the PostgreSQL database. ✅

---

## 🌐 5. Full API Reference

### Authentication
| Method | Endpoint | Auth | Body | Description |
|---|---|---|---|---|
| `POST` | `api/v1/auth/login/` | None | `{username, password}` | Returns `access` + `refresh` JWT tokens |
| `POST` | `api/v1/auth/refresh/` | None | `{refresh}` | Returns a new `access` token |

### Users
| Method | Endpoint | Auth | Body | Description |
|---|---|---|---|---|
| `POST` | `api/v1/users/register/` | None | `{username, email, password}` | Creates a new user + auto-creates `UserProfile` |

### Content (read-only)
| Method | Endpoint | Auth | Description |
|---|---|---|---|
| `GET` | `api/v1/languages/` | Optional | Full nested content tree |
| `GET` | `api/v1/languages/{id}/` | Optional | Single language detail |
| `GET` | `api/v1/modules/` | Optional | All modules with lessons |
| `GET` | `api/v1/modules/{id}/` | Optional | Single module detail |
| `GET` | `api/v1/lessons/` | Optional | All lessons with exercises |
| `GET` | `api/v1/lessons/{id}/` | Optional | Single lesson detail |
| `GET` | `api/v1/exercises/` | Optional | All exercises |
| `GET` | `api/v1/exercises/{id}/` | Optional | Single exercise detail |

### Progress
| Method | Endpoint | Auth | Body | Description |
|---|---|---|---|---|
| `POST` | `api/v1/progress/` | ✅ Bearer token | `{lesson_id}` | Logs lesson completion + awards XP |

---

## 🔗 6. Data Flow — Registration to XP

```
POST /api/v1/users/register/
        │
        ▼
UserRegistrationSerializer.create()
  → make_password() → User saved
        │
        ▼ (post_save signal fires)
create_user_profile()
  → UserProfile.objects.create(user=instance)

POST /api/v1/auth/login/
  → Returns { access, refresh }

POST /api/v1/progress/   [Authorization: Bearer <token>]
        │
        ▼
LogProgressView.post()
  → get_or_create(UserProgress)
        │
        ▼ (post_save signal fires, created=True)
award_xp_on_lesson_completion()
  → UserProfile.xp += lesson.xp_reward  (atomic F() update)
```

---

## 🛠️ 7. Key Technical Decisions

| Decision | Rationale |
|---|---|
| `make_password()` in serializer | Keeps hashing logic in the data layer, not the view |
| `get_or_create` in `LogProgressView` | Duplicate-safe; avoids `IntegrityError` from `unique_together` |
| `created` flag as XP guard | Natural anti-farming: XP signal only fires on the first DB insert |
| `models.F('xp')` for XP update | Atomic DB-level increment; race-condition safe |
| String sender `'lessons.UserProgress'` in signal | Avoids circular import between `users` and `lessons` apps |
| `prefetch_related` on ViewSets | Minimises N+1 queries on nested content tree reads |
| JWT over session auth | Stateless — suitable for mobile/frontend clients |

---

*Generated: February 28, 2026*
