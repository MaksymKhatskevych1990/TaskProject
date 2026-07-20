# Operational scripts

Place repeatable maintenance and deployment scripts in this directory.

Scripts must:

- use non-interactive arguments where practical;
- exit on errors and return meaningful status codes;
- read credentials from environment variables;
- be safe to run more than once when possible;
- delegate business operations to Django services or management commands.

One-off data corrections belong in reviewed Django management commands when
they need ORM or domain access.
