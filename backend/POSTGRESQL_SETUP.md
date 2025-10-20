# PostgreSQL Setup Guide for EduGraph

> **Note:** If you're using Docker (recommended), PostgreSQL is automatically configured via `docker-compose up`. This guide is for reference or manual setup only.

## Recommended: Docker Setup

For the easiest setup, use Docker Compose which automatically configures PostgreSQL:

```powershell
docker-compose up -d
```

See [../DOCKER_SETUP.md](../DOCKER_SETUP.md) for complete Docker instructions.

---

## Manual PostgreSQL Setup (Advanced)

This section is for advanced users who want to set up PostgreSQL manually without Docker.

## Step 1: Setting up PostgreSQL with Docker

1. Pull the PostgreSQL Docker image:
```bash
docker pull postgres:latest
```

2. Create and run the PostgreSQL container:
```bash
docker run --name postgres -e POSTGRES_PASSWORD=postgres -p 5432:5432 -d postgres
```

This command:
- Names the container 'postgres'
- Sets the default password to 'postgres'
- Maps port 5432 on your host to port 5432 in the container
- Runs the container in detached mode (-d)

## Step 2: Project Configuration

1. Install required Python packages:
```bash
pip install psycopg2-binary python-decouple django-extensions
```

2. Create or update your `.env` file in the project root:
```ini
# Database Configuration for PostgreSQL
DB_NAME=edugraph
DB_USER=postgres
DB_PASSWORD=postgres
DB_HOST=localhost
DB_PORT=5432

# Django Secret Key (generate a new one for production)
SECRET_KEY=your-secret-key-here

# Debug setting
DEBUG=True

# Allowed hosts (comma-separated for multiple hosts)
ALLOWED_HOSTS=localhost,127.0.0.1,*
```

3. Verify your database settings in `backend/settings.py`:
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': config('DB_NAME', default='edugraph'),
        'USER': config('DB_USER', default='postgres'),
        'PASSWORD': config('DB_PASSWORD', default=''),
        'HOST': config('DB_HOST', default='localhost'),
        'PORT': config('DB_PORT', default='5432'),
    }
}
```

## Step 3: Database Setup

1. Create the database (if it doesn't exist):
```bash
docker exec -it postgres psql -U postgres -c "CREATE DATABASE edugraph;"
```

2. Apply migrations:
```bash
python manage.py migrate
```

## Step 4: Verifying the Setup

1. Test the database connection:
```bash
python manage.py dbshell
```

2. Create a superuser:
```bash
python manage.py createsuperuser
```

## Common Issues and Solutions

### Connection Refused
If you get a "connection refused" error:
1. Check if the Docker container is running:
```bash
docker ps
```
2. Verify PostgreSQL is listening on port 5432:
```bash
docker exec -it postgres psql -U postgres -c "\l"
```

### Database Doesn't Exist
If you get "database does not exist" error:
1. Connect to PostgreSQL:
```bash
docker exec -it postgres psql -U postgres
```
2. Create the database manually:
```sql
CREATE DATABASE edugraph;
```

### Permission Issues
If you encounter permission issues:
1. Check your `.env` file credentials
2. Verify the user has proper permissions:
```sql
ALTER USER postgres WITH PASSWORD 'postgres';
GRANT ALL PRIVILEGES ON DATABASE edugraph TO postgres;
```

## Production Considerations

For production deployment:
1. Use strong, unique passwords
2. Restrict database access to specific IP addresses
3. Regular backups
4. Consider using managed PostgreSQL services (like AWS RDS)
5. Update `DEBUG=False` in production
6. Use environment-specific `.env` files

## Maintenance

### Backup
```bash
docker exec -t postgres pg_dumpall -U postgres > backup.sql
```

### Restore
```bash
cat backup.sql | docker exec -i postgres psql -U postgres
```

## Checking PostgreSQL Status

### For Docker Installation
```bash
# Check if container is running
docker ps | grep postgres

# Check container logs
docker logs postgres
```

## Notes

- Keep your `.env` file secure and never commit it to version control
- In production, use strong passwords and restrict database access
- Regular backups are recommended
- Consider using connection pooling in production

## Alternative Setup Methods

- **Docker Compose (Recommended)**: For a complete containerized setup with web server and database, see [../DOCKER_SETUP.md](../DOCKER_SETUP.md)
- **Backend API**: For Django-specific configuration, see [README.md](README.md)

## Additional Resources

- [PostgreSQL Documentation](https://www.postgresql.org/docs/)
- [Django Database Documentation](https://docs.djangoproject.com/en/stable/ref/databases/#postgresql-notes)
- [psycopg2 Documentation](https://www.psycopg.org/docs/)
- [python-decouple Documentation](https://github.com/henriquebastos/python-decouple)
