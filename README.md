# Trees Everywhere

Trees Everywhere is a lightweight Django application that enables volunteers around the globe to log every tree they plant and share the data with members of their accounts. This project is make in YouShop admission tech challange.

## Tech Stack

- [Python 3.13](https://www.python.org/)
- [Django 5](https://www.djangoproject.com/)
- [Django REST Framework](https://www.django-rest-framework.org/)
- [PostgreSQL](https://www.postgresql.org/)
- [Docker](https://www.docker.com/) & [Docker Compose](https://docs.docker.com/compose/)
- [Django's Test](https://docs.djangoproject.com/en/5.2/topics/testing/tools/)
- [Ruff](https://docs.astral.sh/ruff/)

## Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/sandrosmarzaro/trees-everywhere.git
cd trees-everywhere
```

### 2. Configure environment variables

Create a `.env` file at the project root with the database credentials expected by `docker-compose.yml`:

```env
DB_NAME=trees_everywhere
DB_USER=trees
DB_PASSWORD=trees
```

Feel free to use any values—just keep them in sync with your environment.

### 3. Build and start the containers

```bash
docker compose build        # one-time image build
docker compose up -d        # start app & database in the background
```

The API will be reachable at http://localhost:8000 when the containers are healthy.

### 4. Apply database migrations

```bash
docker compose exec app python manage.py migrate
```

(Optional) create an admin account:

```bash
docker compose exec app python manage.py createsuperuser
```

### 5. Run the tests

```bash
docker compose exec app python manage.py test
```

### 6. API documentation

The project ships with interactive, auto-generated OpenAPI documentation powered by [drf-spectacular](https://drf-spectacular.readthedocs.io/):

| Endpoint | Description |
|----------|-------------|
| `/api/schema/` | Raw OpenAPI 3 schema (JSON or YAML, depending on `Accept` header) |
| `/api/schema/swagger-ui/` | Swagger-UI explorer |
| `/api/schema/redoc/` | ReDoc static documentation |

These routes are served as soon as the application container is running.

### 7. Key API endpoints

Base path: `/api/`

**Authentication & user management**

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/login/` | Obtain auth token |
| GET/POST | `/users/` | List users / create a user |
| GET/PUT/PATCH/DELETE | `/users/<id>/` | User detail & management |
| POST | `/users/add-to-account/` | Add the current user to a given account |

**Accounts**

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET/POST | `/accounts/` | List accounts / create account |
| GET/PUT/PATCH/DELETE | `/accounts/<id>/` | Account detail & management |

**Trees catalog**

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET/POST | `/trees/` | List tree species / create a tree species |
| GET/PUT/PATCH/DELETE | `/trees/<uuid>/` | Tree species detail & management |

**Planted trees**

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/trees-planted` | Register a single tree planted by the current user |
| POST | `/trees-planted/bulk/` | Register multiple trees at once |
| GET | `/trees-planted/my/` | List trees planted by the current user |
| GET | `/trees-planted/accounts/` | List trees planted under the accounts the user belongs to |
| GET | `/trees-planted/<uuid>/` | Retrieve details of a specific planted tree |

All endpoints require authentication unless explicitly noted otherwise (e.g., user creation and login).

---

To stop everything:

```bash
docker compose down
```
