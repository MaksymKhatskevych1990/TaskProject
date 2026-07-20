# Test fixtures

Store only stable, hand-maintained fixture data here. Prefer factories for records
whose values are relevant to a test, and keep fixtures small enough to review.

Load a JSON fixture with:

```bash
python manage.py loaddata tests/fixtures/<name>.json
```
