# AWS Secrets Manager

## General info

service to help protect secrets needed to access applications, services and IT resources

Features:

* encrypts secrets at rest using our own encryption keys stored in KMS or the one provided auto by KMS
* secrets can be DB cred, passwords, third party API keys or even text
* we store and control access to them with the Secrets Manager Console/CLI/API/SDK
* hardcoded credentials in code is replaced with an API call
* secrets can be rotated automatically according to our own schedule, passwords are then changed automatically every 30/60/90 days or custom like every day (max is 365 days). This functionality uses a lambda (existing one or new one)

3 types: credentials for RDS, credentials for other DB, other type of secrets (Key-value, plaintext)

Built in support for
* MySQL
* PostgreSQL
* Aurora

## Process

1. User saves DB credentials in Secrets Manger which encrypts them with KMS key.
2. App queries Secrets Manager for the credentials
3. Secrets Manager retrieves, decrypts and sends it to the app (HTTPS using TLS)
4. App uses the credentials