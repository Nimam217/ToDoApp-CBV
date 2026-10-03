# ToDoApp

A full-featured task management application built with **Django 5.2**, **Django REST Framework**, **PostgreSQL**, and **Docker**.

The project offers two interfaces on top of the same data:

- A server-rendered web UI (class-based views + Bootstrap 5)
- A versioned REST API (`/api/v1/`) with Token and JWT authentication, filtering, pagination, and Swagger/ReDoc documentation

---

## Table of Contents

- [Features](#features)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Data Models](#data-models)
- [Web Routes](#web-routes)
- [REST API](#rest-api)
- [API Documentation](#api-documentation)
- [Environment Variables](#environment-variables)
- [Getting Started](#getting-started)
- [Running Tests](#running-tests)
- [Load Testing](#load-testing)
- [Code Style](#code-style)
- [Production Deployment](#production-deployment)
- [Useful Docker Commands](#useful-docker-commands)

---

## Features

### Authentication and Accounts

- Custom `User` model based on `AbstractBaseUser` with **email as the login field**
- Registration with **email activation** (`is_verified` flag) and resend-activation support
- Login, logout (with confirmation page), password change, and password reset via email
- Email templates rendered with `django-mail-templated`
- A `Profile` is created automatically for every new user through a `post_save` signal
- Profile page and edit page with image upload (users can only edit their own profile)
- Background email sending (Celery tasks and threads)

### Task Management

- Create, view, update, and delete tasks
- Mark tasks as done or pending
- Each task belongs to its owner, and users can only access their own tasks
- Dashboard with pending/completed separation, status filter, title search, and task counters
- Management commands in `task/management/commands`

### REST API

- Versioned endpoints under `api/v1/` for both `accounts` and `task`
- Token authentication and JWT authentication (create, refresh, verify)
- Task CRUD through a `ModelViewSet`
- Filtering by creation date range and completion status (`django-filter`)
- Custom pagination
- Custom permissions per app
- Interactive documentation with Swagger UI and ReDoc (`drf-yasg`)

* Authentication
* Registration
* JWT authentication
* Account activation
* Password management
* Profile management
* Task CRUD
* Object-level permissions
* Filtering
* Searching
* Ordering
* Pagination

- Bootstrap 5, responsive layout
- Bootstrap cards and alerts together with the Django messages framework

OpenAPI documentation is available through:

```text
/swagger/
/redoc/
```

## Tech Stack

| Area | Technology |
|------|------------|
| Language | Python 3.11 |
| Framework | Django 5.2, Django REST Framework |
| Database | PostgreSQL 15 (SQLite file is included for quick local experiments) |
| Auth | Django auth, DRF Token auth, `djangorestframework-simplejwt` |
| API docs | `drf-yasg` (Swagger / ReDoc) |
| Filtering | `django-filter` |
| Background jobs | Celery |
| Email (dev) | smtp4dev |
| Web server (prod) | Gunicorn + Nginx |
| Containers | Docker, Docker Compose |
| Testing | pytest |
| Load testing | Locust |
| Code quality | black, flake8 |

### Performance & Testing

* Redis caching
* Locust load testing

## Architecture

```text
                         Client
                           │
             ┌─────────────┴─────────────┐
             │                           │
       Django Templates             REST API
             │                           │
             └─────────────┬─────────────┘
                           │
                        Django
                           │
             ┌─────────────┼─────────────┐
             │             │             │
         PostgreSQL      Redis        Celery
                                       │
                                ┌──────┴──────┐
                                │             │
                              Worker         Beat
```

For the production-like environment:

```text
Client
  │
  ▼
Nginx
  │
  ▼
Gunicorn
  │
  ▼
Django
 ├── PostgreSQL
 ├── Redis
 └── Celery
      ├── Worker
      └── Beat
```

## Project Structure

```text
.
├── accounts                 # Users, profiles, authentication
│   ├── api/v1               # Accounts REST API
│   ├── tests                # test_accounts_api, test_accounts_render
│   ├── models.py            # User, Profile
│   ├── forms.py
│   ├── mixins.py
│   ├── services.py
│   ├── signals.py           # Auto-create Profile
│   ├── tasks.py             # Celery tasks
│   ├── threads.py
│   ├── urls.py
│   └── views.py
├── core                     # Home page and load testing
│   ├── locust/locustfile.py
│   ├── tsets                # Render tests for core
│   ├── urls.py
│   └── views.py
├── task                     # Task management
│   ├── api/v1               # Task REST API
│   ├── management/commands  # Custom management commands
│   ├── tests                # test_task_api, test_task_render
│   ├── models.py            # Task
│   ├── forms.py
│   ├── signals.py
│   ├── urls.py
│   └── views.py
├── templates                # accounts, core, email, registration, task
├── ToDoApp                  # Project configuration
│   ├── settings
│   │   ├── base.py
│   │   ├── development.py
│   │   └── production.py
│   ├── celery.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
├── nginx/nginx.conf
├── conftest.py
├── pytest.ini
├── Dockerfile
├── docker-compose.yml       # Development stack
├── docker-compose.prod.yml  # Production stack
├── wait-for-it.sh
├── requirements.txt
└── manage.py
```

---

## Data Models

### User

| Field | Type | Notes |
|-------|------|-------|
| `email` | EmailField | Unique, used as `USERNAME_FIELD` |
| `is_active` | Boolean | Default `True` |
| `is_verified` | Boolean | Default `False`, set after email activation |
| `is_staff`, `is_superuser` | Boolean | Standard Django flags |
| `date_joined`, `date_updated` | DateTime | Automatic |

### Profile

One-to-one with `User` (`related_name="profile"`).

| Field | Type |
|-------|------|
| `first_name`, `last_name` | CharField (max 50) |
| `image` | ImageField (`upload_to="images"`, optional) |
| `description` | TextField (optional) |
| `date_joined`, `date_updated` | DateTime |

### Task

| Field | Type | Notes |
|-------|------|-------|
| `title` | CharField (max 100) | |
| `description` | TextField | |
| `user` | ForeignKey to `User` | Owner, cascade delete |
| `done` | Boolean | Default `False` |
| `created_at`, `updated_at` | DateTime | Automatic |

---

## Web Routes

| URL | Description |
|-----|-------------|
| `/` | Home page |
| `/accounts/register/` | Registration |
| `/accounts/login/` | Login |
| `/accounts/logout_confirm/` | Logout confirmation |
| `/accounts/password_change/` | Change password |
| `/accounts/password_reset/` | Reset password by email |
| `/accounts/profile/<id>/` | View profile |
| `/accounts/profile/<id>/edit/` | Edit profile |
| `/task/dashboard/` | Task dashboard |
| `/task/create/` | Create task |
| `/task/detail/<id>/` | Task details |
| `/task/update/<id>/` | Update task |
| `/task/delete/<id>/` | Delete task |
| `/admin/` | Django admin |

---

## REST API

### Accounts: `/accounts/api/v1/`

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `registration/` | Register a new user (sends activation email) |
| GET | `activation/confirm/<token>/` | Activate account |
| POST | `activation/resend/` | Resend activation email |
| POST | `token-auth/create/` | Obtain an auth token |
| POST | `token-auth/discard/` | Discard the auth token |
| POST | `jwt/create/` | Obtain JWT access and refresh tokens |
| POST | `jwt/refresh/` | Refresh the access token |
| POST | `jwt/verify/` | Verify a token |
| GET, PUT, PATCH | `profile/` | Retrieve or update the current user's profile |
| PUT | `change_password/` | Change password |
| POST | `reset_password/` | Request a password reset email |
| POST | `reset_password/confirm/<token>/` | Set a new password |

### Tasks: `/task/api/v1/`

Registered through a DRF router:

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `my-task/` | List the current user's tasks (paginated) |
| POST | `my-task/` | Create a task |
| GET | `my-task/<id>/` | Retrieve a task |
| PUT, PATCH | `my-task/<id>/` | Update a task |
| DELETE | `my-task/<id>/` | Delete a task |

**Query parameters for `GET my-task/`:**

| Parameter | Description |
|-----------|-------------|
| `is_done` | Filter by completion status (`true` / `false`) |
| `from_this_date` | Tasks created on or after this datetime |
| `to_this_date` | Tasks created on or before this datetime |

### Authentication example

```bash
# Get a JWT
curl -X POST http://127.0.0.1/accounts/api/v1/jwt/create/ \
  -H "Content-Type: application/json" \
  -d '{"email": "user@example.com", "password": "your-password"}'

# Use it
curl http://127.0.0.1/task/api/v1/my-task/?is_done=false \
  -H "Authorization: Bearer <access_token>"
```

---

## API Documentation

Interactive documentation is generated automatically:

| URL | Description |
|-----|-------------|
| `/swagger/` | Swagger UI |
| `/redoc/` | ReDoc |
| `/swagger.json/` | Raw OpenAPI schema |

The caching layer includes:

* Cache keys
* TTL
* Cache invalidation
* User-specific data handling
* Cache consistency after data changes

Create a `.env` file in the project root:

* Account activation
* Password reset
* Resending activation emails

Email operations can be processed asynchronously using Celery.

## Testing

> Never commit your `.env` file. It is already listed in `.gitignore`.

---

## Getting Started

### Prerequisites

- Docker
- Docker Compose

### 1. Clone the repository

```bash
pytest
```

### 2. Create the `.env` file

See [Environment Variables](#environment-variables).

### 3. Build and start the containers

```bash
pytest --cov=.
```

On startup, the `web` container waits for PostgreSQL using `wait-for-it.sh`, applies migrations, and then starts the server:

```text
PostgreSQL starts -> wait-for-it.sh (db:5432) -> migrate -> web server
```

### 4. Open the application

| Service | URL |
|---------|-----|
| Web application | http://127.0.0.1 |
| Swagger UI | http://127.0.0.1/swagger/ |
| smtp4dev (catches outgoing emails) | http://127.0.0.1:5000 |

### 5. Create a superuser

```bash
docker compose exec web python manage.py createsuperuser
```

### Development services

| Service | Purpose |
|---------|---------|
| `web` | Django application (port 80 on the host maps to 8000 in the container) |
| `db` | PostgreSQL 15 with the `postgres_data` named volume |
| `smtp4dev` | Fake SMTP server for activation and password reset emails |

Registration and password reset emails are not delivered to real inboxes in development. Open the smtp4dev web interface to read them and click the activation links.

---

## Running Tests

The project uses **pytest** (see `pytest.ini` and `conftest.py`). Tests live inside each app:

- `accounts/tests/test_accounts_api`, `accounts/tests/test_accounts_render`
- `task/tests/test_task_api`, `task/tests/test_task_render`
- `core/tsets/test_core_render`

Run them inside the container:

```bash
docker compose exec web pytest
```

Run a single app or file:

```bash
docker compose exec web pytest task/
docker compose exec web pytest accounts/tests/test_accounts_api -v
```

---

## Load Testing

A Locust scenario is provided in `core/locust/locustfile.py`:

```bash
locust -f core/locust/locustfile.py --host http://127.0.0.1
```

Then open http://localhost:8089 to start the test.

---

## Code Style

The project is formatted with **black** and linted with **flake8** (configuration in `.flake8`):

```bash
black .
flake8
```

---

## Production Deployment

The production stack is defined in `docker-compose.prod.yml` and uses:

- Django with the `ToDoApp.settings.production` settings module
- Gunicorn as the application server
- Nginx as the reverse proxy (`nginx/nginx.conf`)
- PostgreSQL with a persistent volume

```bash
docker compose -f docker-compose.prod.yml up -d --build
```

Before deploying, make sure that:

- `DEBUG` is disabled
- `SECRET_KEY` is a strong, private value
- `ALLOWED_HOSTS` contains your domain
- The `.env` file contains production credentials

---

## Useful Docker Commands

```bash
docker compose up -d --build        # Build and run in the background
docker compose down                 # Stop containers
docker compose ps                   # List running containers
docker compose logs -f web          # Follow Django logs
docker compose logs db              # PostgreSQL logs
docker compose exec web sh          # Shell inside the Django container
docker compose exec web python manage.py migrate
docker compose exec web python manage.py makemigrations
```

---

## Author

**Nima** — [GitHub: Nimam217](https://github.com/Nimam217)
