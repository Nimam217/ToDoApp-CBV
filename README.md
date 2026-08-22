# Django Task Manager

A task management web application built with Django, PostgreSQL, Docker, and Bootstrap 5.

The project provides user authentication, profile management, task CRUD operations, task filtering, search, and a responsive user interface.

---

## Features

### Authentication

- Custom User model based on `AbstractBaseUser`
- Email-based authentication
- User registration
- Login and logout
- Logout confirmation
- Password change
- Password reset via email
- Django built-in authentication views
- Custom authentication forms
- Protected views using `LoginRequiredMixin`

### Profile

- View user profile
- Edit personal profile
- First name
- Last name
- Description
- Profile creation date
- Profile update date
- Users can only edit their own profile

### Task Management

- Create tasks
- View task details
- Update tasks
- Delete tasks
- Mark tasks as completed
- Mark tasks as pending
- Tasks belong to their owner
- Users can only access their own tasks

### Dashboard

- Display user's tasks
- Separate pending and completed tasks
- Filter tasks by status
- Search tasks by title
- Display total task count
- Display pending task count
- Display completed task count

### UI

- Bootstrap 5
- Responsive design
- Bootstrap cards
- Bootstrap alerts
- Django messages
- Responsive navigation
- Clean dashboard interface

---

## Tech Stack

- Python
- Django 5.2
- PostgreSQL 15
- Bootstrap 5
- Docker
- Docker Compose

---

## Project Structure

```text
.
├── accounts
│   ├── admin.py
│   ├── apps.py
│   ├── forms.py
│   ├── __init__.py
│   ├── migrations
│   │   ├── 0001_initial.py
│   │   ├── 0002_user_image.py
│   │   ├── 0003_alter_user_image.py
│   │   ├── 0004_alter_profile_user.py
│   │   ├── 0005_remove_user_image_profile_image.py
│   │   └── __init__.py
│   ├── models.py
│   ├── signals.py
│   ├── tests.py
│   ├── urls.py
│   └── views.py
│
├── core
│   ├── admin.py
│   ├── apps.py
│   ├── __init__.py
│   ├── migrations
│   │   └── __init__.py
│   ├── models.py
│   ├── tests.py
│   ├── urls.py
│   └── views.py
│
├── docker-compose.yml
├── Dockerfile
├── manage.py
├── README.md
├── requirements.txt
│
├── task
│   ├── admin.py
│   ├── apps.py
│   ├── forms.py
│   ├── __init__.py
│   ├── migrations
│   │   ├── 0001_initial.py
│   │   └── __init__.py
│   ├── models.py
│   ├── tests.py
│   ├── urls.py
│   └── views.py
│
├── templates
│   ├── accounts
│   │   ├── profile_edit.html
│   │   └── profile.html
│   ├── base.html
│   ├── core
│   │   └── home.html
│   ├── registration
│   │   ├── logged_out.html
│   │   ├── login.html
│   │   ├── password_change_done.html
│   │   ├── password_change.html
│   │   ├── password_reset_complete.html
│   │   ├── password_reset_confirm.html
│   │   ├── password_reset_done.html
│   │   ├── password_reset_email.html
│   │   ├── password_reset.html
│   │   └── register.html
│   └── task
│       ├── create.html
│       ├── dashboard.html
│       ├── delete.html
│       ├── detail.html
│       └── update.html
│
├── ToDoApp
│   ├── asgi.py
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
│
└── wait-for-it.sh
```

---

## Docker

The project uses Docker Compose to run Django and PostgreSQL.

### Services

The application consists of two services:

- `web` — Django application
- `db` — PostgreSQL database

PostgreSQL uses a Docker named volume to persist database data.

```yaml
volumes:
  postgres_data:
```

### Web Service

The Django application is built using the project's `Dockerfile`.

The project directory is mounted into the container:

```yaml
volumes:
  - .:/app
```

The Django development server runs on:

```text
0.0.0.0:8000
```

Docker maps port `8000` inside the container to port `80` on the host:

```yaml
ports:
  - "80:8000"
```

The application can therefore be accessed at:

```text
http://127.0.0.1
```

---

## Database Startup

The project uses `wait-for-it.sh` to wait until PostgreSQL is available before starting Django.

The startup process is:

```text
Docker Compose
      ↓
PostgreSQL starts
      ↓
wait-for-it.sh
      ↓
Wait for db:5432
      ↓
Django migrations
      ↓
Django development server
```

The web container runs the following startup command:

```bash
./wait-for-it.sh db:5432 --timeout=60 -- \
python manage.py migrate && \
python manage.py runserver 0.0.0.0:8000
```

---

## Docker Compose Configuration

The project uses the following Docker Compose structure:

```yaml
services:
  db:
    image: postgres:15
    env_file:
      - .env
    volumes:
      - postgres_data:/var/lib/postgresql/data

  web:
    build: .
    command: >
      sh -c "
        ./wait-for-it.sh db:5432 --timeout=60 --
        python manage.py migrate &&
        python manage.py runserver 0.0.0.0:8000
      "
    volumes:
      - .:/app
    ports:
      - "80:8000"
    depends_on:
      - db
    env_file:
      - .env

volumes:
  postgres_data:
```

---

## Environment Variables

Create a `.env` file in the root directory.

Example:

```env
SECRET_KEY=your-secret-key
DEBUG=1

POSTGRES_DB=your_database
POSTGRES_USER=your_user
POSTGRES_PASSWORD=your_password

DB_NAME=your_database
DB_USER=your_user
DB_PASSWORD=your_password
DB_HOST=db
DB_PORT=5432
```

Do not commit your `.env` file to Git.

Add it to `.gitignore`:

```gitignore
.env
```

---

## Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/Nimam217/ToDoApp-CBV.git
cd ToDoApp-CBV
```

### 2. Create the `.env` file

Create a `.env` file in the project root and configure the required Django and PostgreSQL environment variables.

### 3. Build and start the containers

```bash
docker compose up --build
```

Or run the containers in detached mode:

```bash
docker compose up -d --build
```

### 4. Open the application

Visit:

```text
http://127.0.0.1
```

---

## Useful Docker Commands

### Start the application

```bash
docker compose up
```

### Build and start

```bash
docker compose up --build
```

### Run in background

```bash
docker compose up -d
```

### Stop containers

```bash
docker compose down
```

### View running containers

```bash
docker compose ps
```

### View all logs

```bash
docker compose logs
```

### View Django logs

```bash
docker compose logs web
```

### View PostgreSQL logs

```bash
docker compose logs db
```

### Open a shell inside the Django container

```bash
docker compose exec web sh
```

### Create migrations

```bash
docker compose exec web python manage.py makemigrations
```

### Apply migrations

```bash
docker compose exec web python manage.py migrate
```

### Create a superuser

```bash
docker compose exec web python manage.py createsuperuser
```

---

## Migrations

When models are changed, create new migration files:

```bash
docker compose exec web python manage.py makemigrations
```

Then apply them:

```bash
docker compose exec web python manage.py migrate
```

The Docker startup command automatically runs:

```bash
python manage.py migrate
```

Migration files should be committed to Git.

---

## Django Messages

The project uses Django's messages framework to provide feedback to users.

For example:

```python
from django.contrib import messages

messages.success(
    self.request,
    "Task created successfully."
)
```

Messages are displayed as Bootstrap alerts in the base template.

---

## Query Optimization

The project uses `select_related()` for the relationship between `Task` and `User`.

Example:

```python
Task.objects.select_related("user").filter(
    user=self.request.user
)
```

This helps reduce unnecessary database queries when accessing related user information.

---

## Security

Task views use `LoginRequiredMixin` and restrict querysets to the currently authenticated user.

Example:

```python
def get_queryset(self):
    return Task.objects.select_related("user").filter(
        user=self.request.user
    )
```

This prevents users from accessing, editing, or deleting tasks belonging to other users.

---

## Development Note

The frontend/UI was developed with assistance from ChatGPT.

The Django backend, application logic, authentication system, database models, views, forms, and project structure were implemented by me.

---

## License

This project is licensed under the MIT License.