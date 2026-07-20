# Studio Management

Internal Django platform for managing the studio's work. The project is a
modular monolith: each domain has an independent Django application, while
deployment and shared infrastructure remain centralized.

## Quick start

```bash
./run.sh
docker compose run --rm backend python manage.py createsuperuser
```

The application is available at <http://localhost:8080> and the administration
site at <http://localhost:8080/admin/>.

## API

- API root: `/api/`
- Current API version: `/api/v1/`
- JWT obtain: `/api/v1/auth/token/`
- JWT refresh: `/api/v1/auth/token/refresh/`
- JWT logout: `/api/v1/auth/logout/`
- Current profile: `/api/v1/accounts/me/`
- User management: `/api/v1/accounts/users/`
- Employees: `/api/v1/employees/`
- Teams: `/api/v1/employees/teams/`
- Positions: `/api/v1/employees/positions/`
- Liveness: `/health/`
- Readiness: `/health/ready/`

The legacy `/api/health/` route remains available for container health checks.

## Development setup

Install development tools in a Python 3.13 virtual environment:

```bash
python -m pip install -r requirements-dev.txt
```

Run the quality checks:

```bash
black --check .
ruff check .
pytest
```

Docker and Django commands are listed in `start.txt`.

## Architecture

Business applications live in `apps/`. Each application owns its models,
administration, API, services, selectors, background jobs, and tests. Shared
technical code belongs in `apps/common/`; domain-specific behavior does not.

Detailed placement rules and the complete tree are documented in
`docs/project-structure.md`.
