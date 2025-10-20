# Docker Setup Guide for EduGraph

This guide explains how to run EduGraph using Docker and Docker Compose.

## Prerequisites

- Docker Desktop (Windows/Mac) or Docker Engine (Linux)
- Docker Compose v2.0+

## Quick Start

### 1. Environment Setup

Copy the example environment file and configure it:

```powershell
# Windows PowerShell
Copy-Item .env.example .env
```

Edit `.env` file with your preferred settings (optional - defaults work fine for development).

### 2. Start the Application

```powershell
# Start all services (web + database)
docker-compose up -d

# View logs
docker-compose logs -f

# View logs for specific service
docker-compose logs -f web
docker-compose logs -f db
```

### 3. Access the Application

- **Web Application**: http://localhost:8000
- **API Endpoints**:
  - Graph Data: http://localhost:8000/api/graph/data/
  - Visualization: http://localhost:8000/api/graph/view/
  - Admin Panel: http://localhost:8000/admin/

### 4. Initial Setup

Create a superuser for Django admin:

```powershell
docker-compose exec web python manage.py createsuperuser
```

## Development Mode

### Start with Development Tools

```powershell
# Start with pgAdmin for database management
docker-compose --profile dev up -d

# Access pgAdmin at http://localhost:5050
# Email: admin@edugraph.com
# Password: admin (or your configured PGADMIN_PASSWORD)
```

### Useful Commands

```powershell
# Run Django management commands
docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py createsuperuser
docker-compose exec web python manage.py collectstatic

# Access Django shell
docker-compose exec web python manage.py shell

# Access PostgreSQL shell
docker-compose exec db psql -U postgres -d edugraph

# View running containers
docker-compose ps

# Stop all services
docker-compose down

# Stop and remove volumes (WARNING: deletes database data)
docker-compose down -v
```

## Production Mode

### Start with Nginx Reverse Proxy

```powershell
# Start with nginx
docker-compose --profile production up -d

# Access application through Nginx at http://localhost:80
```

### Production Checklist

Before deploying to production:

1. **Update Environment Variables** in `.env`:
   ```ini
   DEBUG=False
   SECRET_KEY=<generate-a-strong-random-key>
   DB_PASSWORD=<strong-database-password>
   ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
   ```

2. **Generate a Secret Key**:
   ```powershell
   docker-compose exec web python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
   ```

3. **Collect Static Files**:
   ```powershell
   docker-compose exec web python manage.py collectstatic --noinput
   ```

4. **Run Migrations**:
   ```powershell
   docker-compose exec web python manage.py migrate
   ```

## Database Management

### Backup Database

```powershell
# Create backup
docker-compose exec db pg_dump -U postgres edugraph > backups/backup_$(Get-Date -Format "yyyyMMdd_HHmmss").sql

# Or using docker-compose
docker-compose exec -T db pg_dump -U postgres edugraph > backups/backup.sql
```

### Restore Database

```powershell
# Restore from backup
Get-Content backups/backup.sql | docker-compose exec -T db psql -U postgres edugraph
```

### Access Database Directly

```powershell
# PostgreSQL shell
docker-compose exec db psql -U postgres -d edugraph

# List databases
docker-compose exec db psql -U postgres -c "\l"

# List tables
docker-compose exec db psql -U postgres -d edugraph -c "\dt"
```

## Troubleshooting

### Port Already in Use

If port 8000 or 5432 is already in use, change it in `.env`:

```ini
WEB_PORT=8001
DB_PORT=5433
```

### Database Connection Issues

Check if database is healthy:

```powershell
docker-compose exec db pg_isready -U postgres -d edugraph
```

View database logs:

```powershell
docker-compose logs db
```

### Reset Everything

```powershell
# Stop and remove all containers, networks, and volumes
docker-compose down -v

# Rebuild and start
docker-compose up -d --build
```

### View Container Resources

```powershell
# View container stats
docker stats

# View specific container logs
docker logs edugraph_web
docker logs edugraph_db
```

## Docker Compose Profiles

The `docker-compose.yml` supports different profiles:

- **Default**: Web + Database (minimal setup)
- **dev**: Adds pgAdmin for database management
- **production**: Adds Nginx reverse proxy

```powershell
# Development with pgAdmin
docker-compose --profile dev up -d

# Production with Nginx
docker-compose --profile production up -d

# Both profiles
docker-compose --profile dev --profile production up -d
```

## Volume Management

Data is persisted in Docker volumes:

- `postgres_data`: PostgreSQL database files
- `static_volume`: Django static files
- `media_volume`: User uploaded media files
- `pgadmin_data`: pgAdmin configuration

```powershell
# List volumes
docker volume ls

# Inspect volume
docker volume inspect edugraph_postgres_data

# Remove all volumes (WARNING: deletes all data)
docker-compose down -v
```

## Building and Updating

### Rebuild After Code Changes

```powershell
# Rebuild web service
docker-compose build web

# Rebuild and restart
docker-compose up -d --build web
```

### Update Dependencies

After changing `requirements.txt`:

```powershell
docker-compose build --no-cache web
docker-compose up -d web
```

## Performance Optimization

### Production Settings

For production, use gunicorn instead of runserver. Update docker-compose.yml:

```yaml
web:
  command: >
    sh -c "python manage.py migrate &&
           python manage.py collectstatic --noinput &&
           gunicorn backend.wsgi:application --bind 0.0.0.0:8000 --workers 4"
```

Add to `requirements.txt`:
```
gunicorn>=21.2.0
```

## Security Notes

- Never commit `.env` file to version control
- Use strong passwords in production
- Set `DEBUG=False` in production
- Configure `ALLOWED_HOSTS` properly
- Use HTTPS in production (configure SSL in nginx)
- Regularly update Docker images

## Additional Resources

- [Docker Documentation](https://docs.docker.com/)
- [Docker Compose Documentation](https://docs.docker.com/compose/)
- [Django Deployment Checklist](https://docs.djangoproject.com/en/stable/howto/deployment/checklist/)
