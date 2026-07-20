# Project structure

## Top-level layout

```text
apps/                 Django applications and shared code
config/               Settings, root URLs, ASGI, WSGI, and Celery
docs/                 Architecture and operational documentation
scripts/              Repeatable operational scripts
tests/                Cross-application test helpers and architecture tests
docker/                Container entrypoint and Nginx configuration
```

`config/api/urls.py` owns API-version registration. `config/api/v1/urls.py` is
the only place where version 1 application APIs are mounted. A future version
can be introduced as `config/api/v2/` without changing existing clients.

## Application boundaries

Each domain is an independent package under `apps/`:

```text
apps/<application>/
    api/
        urls.py
        views.py
    apps.py
```

Add files only when the application needs them:

```text
admin.py               Admin registration and presentation
models.py              Persistence and model-level invariants
serializers.py         Input validation and representation
services.py            Writes and business operations
selectors.py           Read-only database queries
permissions.py         Domain-specific authorization
tasks.py               Celery entry points
signals.py             Framework event adapters
tests/                  Application-local tests
```

This avoids empty modules while preserving the same placement convention in
every application.

## Dependency direction

Views validate input through serializers, call services or selectors, and
return responses. They do not coordinate business workflows.

Services own business operations and transaction boundaries. Services may use
selectors, models, and infrastructure clients. A service must not depend on an
API view or serializer.

Selectors contain read queries only. They may return querysets or immutable
read results, but they never create, update, or delete records.

Celery tasks deserialize primitive arguments and call services. Signals perform
minimal event adaptation and call a service; they do not contain business
logic.

Admin classes use the same services and selectors as the API. Saving through
the admin must not introduce a second implementation of a workflow.

## Shared code

`apps/common/` contains technical functionality that is useful to multiple
domains:

- `models.py`: abstract identifiers, timestamps, and audit users
- `permissions.py`: framework-level permission helpers
- `pagination.py`: the default API pagination envelope
- `responses.py`: success and error response builders
- `exceptions.py`: centralized DRF exception handling
- `logging.py`: JSON log formatting
- `api/`: infrastructure health endpoints

Do not move code to `common` merely because two modules look similar. Shared
code must be domain-neutral and have a stable purpose.

Concrete models may inherit `BaseModel`. Services should set `created_by` and
`updated_by` when a request user is available; both fields are nullable for
scheduled and system operations.

`IsManager` and `IsEmployee` intentionally check user capabilities named
`is_manager` and `is_employee`. The accounts user model provides those
capabilities from the stored `role` field.

Organizational directory data (teams, positions, hire dates) lives in
`apps/employees/`. Identity remains in accounts. When an employee is assigned a
catalog position, `Profile.position` is synced to the position title for
compatibility with `/accounts/me/`.

## API and errors

Business endpoints are mounted below `/api/v1/`. Infrastructure health routes
remain unversioned at `/health/`. The standard error shape is:

```json
{
  "success": false,
  "error": {
    "code": "validation_error",
    "message": "The submitted data is invalid.",
    "details": {}
  }
}
```

Use `success_response` for non-paginated custom responses. Generic DRF views
may continue returning serializer data directly when an envelope adds no value.

## Testing

Application tests belong beside their application. Cross-application contract
tests and reusable test cases belong in `tests/`.

Pytest uses `config.settings.testing`, an in-memory SQLite database, local
memory caches, in-memory file storage, eager Celery execution, and fast password
hashing. Prefer factories for test-specific records and fixtures only for small,
stable reference datasets.

## Adding a feature

1. Put the model in the domain that owns the data.
2. Put input validation in that application's serializer.
3. Put writes and workflows in a service.
4. Put reusable reads in a selector.
5. Keep the view focused on HTTP concerns.
6. Register routes in the application's `api/urls.py`.
7. Add application-local tests.
8. Add admin integration and permissions where required.
