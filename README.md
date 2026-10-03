# ToDoApp

A full-stack task management application built with **Django** and **Django REST Framework**.

The project provides both a **server-rendered web interface** and a **versioned REST API**, with authentication, authorization, asynchronous tasks, caching, testing, and Docker-based deployment support.

## Features

### Authentication & Account Management

* Custom User model with email-based authentication
* User registration
* Email activation / verification
* Login and logout
* JWT authentication
* Refresh and verify tokens
* Password change
* Password reset via email
* Resend activation email
* User profile management
* Verified-user restrictions
* Authentication and permission handling

### Task Management

* Create, update and delete tasks
* View task details
* Mark tasks as completed or pending
* User-owned tasks
* Object-level ownership permissions
* Search tasks by title and description
* Filter tasks by status
* Order tasks
* Paginate API results

### Dashboard

The project also includes a server-rendered Django interface for managing tasks.

* Task dashboard
* Task statistics
* Search
* Status filtering
* Create / update / delete tasks
* Task detail pages
* User profile management

## REST API

The application provides a versioned REST API using **Django REST Framework**.

```text
/api/v1/
```

The API includes:

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

### API Documentation

OpenAPI documentation is available through:

```text
/swagger/
/redoc/
```

## Tech Stack

### Backend

* Python
* Django
* Django REST Framework
* Django Filter
* Simple JWT

### Database

* PostgreSQL

### Asynchronous Processing

* Redis
* Celery
* Celery Beat

### Testing

* pytest
* pytest-django
* Coverage
* Django / DRF testing utilities

### Deployment

* Docker
* Docker Compose
* Nginx
* Gunicorn

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
├── accounts
│   ├── api
│   │   └── v1
│   ├── migrations
│   ├── tests
│   │   ├── test_accounts_api
│   │   └── test_accounts_render
│   ├── admin.py
│   ├── forms.py
│   ├── mixins.py
│   ├── models.py
│   ├── services.py
│   ├── signals.py
│   ├── tasks.py
│   ├── threads.py
│   ├── urls.py
│   └── views.py
│
├── task
│   ├── api
│   │   └── v1
│   ├── management
│   │   └── commands
│   ├── migrations
│   ├── tests
│   │   ├── test_task_api
│   │   └── test_task_render
│   ├── admin.py
│   ├── forms.py
│   ├── models.py
│   ├── urls.py
│   └── views.py
│
├── core
│   ├── locust
│   │   └── locustfile.py
│   ├── models.py
│   ├── urls.py
│   └── views.py
│
├── templates
│   ├── accounts
│   ├── email
│   ├── registration
│   ├── task
│   └── base.html
│
├── ToDoApp
│   ├── settings
│   │   ├── base.py
│   │   ├── development.py
│   │   └── production.py
│   ├── asgi.py
│   ├── celery.py
│   ├── urls.py
│   └── wsgi.py
│
├── nginx
│   └── nginx.conf
│
├── Dockerfile
├── docker-compose.yml
├── docker-compose.prod.yml
├── conftest.py
├── pytest.ini
├── requirements.txt
├── manage.py
└── wait-for-it.sh
```

## Authentication

The API uses JWT-based authentication for protected endpoints.

Authentication-related functionality includes:

```text
Registration
Email Activation
Login
JWT Access Token
JWT Refresh Token
Password Change
Password Reset
Logout / Token Management
```

Users must verify their account before accessing protected functionality that requires verification.

## Authorization

Tasks are associated with their owner.

Users can only access and modify their own tasks.

Authorization is enforced through both queryset filtering and object-level permission checks.

```text
Authenticated User
        │
        ▼
      Task
        │
        ▼
    Is Owner?
      /   \
    Yes    No
     │      │
   Allow   Deny
```

## Redis & Celery

Redis is used for caching and as infrastructure for asynchronous task processing.

Celery handles background operations such as email-related tasks and scheduled jobs.

```text
Django
  │
  ├── Redis
  │
  └── Celery
       ├── Worker
       └── Beat
```

This allows background operations to run independently from HTTP requests.

## Caching

Redis-based caching is used to improve application performance.

The caching layer includes:

* Cache keys
* TTL
* Cache invalidation
* User-specific data handling
* Cache consistency after data changes

## Email

Email functionality is used for account-related workflows:

* Account activation
* Password reset
* Resending activation emails

Email operations can be processed asynchronously using Celery.

## Testing

Tests are organized by application and separated between API and server-rendered functionality.

```text
accounts/
└── tests/
    ├── test_accounts_api/
    └── test_accounts_render/

task/
└── tests/
    ├── test_task_api/
    └── test_task_render/
```

Run the test suite:

```bash
pytest
```

Run tests with coverage:

```bash
pytest --cov=.
```

## Load Testing

Locust is included for load-testing experiments.

The Locust configuration is located at:

```text
core/locust/locustfile.py
```

## Docker

The project includes separate Docker Compose configurations for development and production-like environments.

### Development

```bash
docker compose up --build
```

### Detached mode

```bash
docker compose up -d --build
```

### Production-like environment

```bash
docker compose -f docker-compose.prod.yml up --build
```

## Environment Variables

Sensitive configuration is provided through environment variables.

Example:

```env
SECRET_KEY=your-secret-key
DEBUG=1

POSTGRES_DB=your_database
POSTGRES_USER=your_user
POSTGRES_PASSWORD=your_password
```

**Never commit real secrets, passwords, tokens, or production credentials to the repository.**

## Useful Commands

### Run migrations

```bash
python manage.py migrate
```

### Create migrations

```bash
python manage.py makemigrations
```

### Create superuser

```bash
python manage.py createsuperuser
```

### Run tests

```bash
pytest
```

### Run development server

```bash
python manage.py runserver
```

## Production Stack

The production-like setup uses:

* Nginx as reverse proxy
* Gunicorn as the WSGI application server
* Django as the application layer
* PostgreSQL as the database
* Redis for caching and task infrastructure
* Celery Worker for background tasks
* Celery Beat for scheduled tasks

## Learning Goals

This project was built to practice real-world backend development concepts, including:

* Django architecture
* Custom User models
* Authentication and authorization
* Django ORM
* Django REST Framework
* JWT authentication
* Object-level permissions
* API filtering, searching and ordering
* Pagination
* Email workflows
* Redis
* Celery
* Caching
* PostgreSQL
* Docker and Docker Compose
* Nginx and Gunicorn
* Automated testing
* API documentation
* Load testing

The project intentionally provides both **server-rendered Django views** and a **REST API** over the same backend.
