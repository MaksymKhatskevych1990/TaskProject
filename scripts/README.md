# Operational scripts

Place repeatable maintenance and deployment scripts in this directory.

`ngrok.sh` publishes the running Studio stack (`./run.sh`) through a public
HTTPS URL so you can open the landing page and admin on a phone.

Scripts must:

- use non-interactive arguments where practical;
- exit on errors and return meaningful status codes;
- read credentials from environment variables;
- be safe to run more than once when possible;
- delegate business operations to Django services or management commands.

One-off data corrections belong in reviewed Django management commands when
they need ORM or domain access.
