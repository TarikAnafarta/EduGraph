# EduGraph Backend

Django-based backend for the EduGraph curriculum visualization project.

## Quick Start

This project uses Docker for easy setup. See the main [README.md](../README.md) and [DOCKER_SETUP.md](../DOCKER_SETUP.md) for complete setup instructions.

**Quick command:**
```powershell
docker-compose up -d
```

## API Endpoints

### Authentication
- `POST /api/users/login/` - User login
- `POST /api/users/register/` - User registration
- `GET /api/users/verify/` - Email verification

### Graph Data
- `GET /api/graph/data/` - Get complete graph data (nodes + links)
- `GET /api/graph/nodes/` - Get graph nodes only
- `GET /api/graph/links/` - Get graph connections only
- `GET /api/graph/stats/` - Get graph statistics

### Views
- `/dashboard/` - Main dashboard
- `/api/graph/view/` - Interactive graph visualization
- `/admin/` - Admin interface (requires superuser)

## Django Management Commands

Useful commands when working with Docker:

```powershell
# Run any Django management command
docker-compose exec web python manage.py <command>

# Examples:
docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py createsuperuser
docker-compose exec web python manage.py collectstatic
```

## Django Shell Commands

Access the Django shell:
```powershell
docker-compose exec web python manage.py shell
```

### Useful User Model Queries

```python
from users.models import User
from django.utils import timezone
from datetime import timedelta

# Get all users
User.objects.all()

# Get active users
User.objects.filter(is_active=True)

# Search users by email
User.objects.filter(email__contains='example.com')

# Get superusers
User.objects.filter(is_superuser=True)

# Get user by email
User.objects.get(email='user@example.com')

# Count total users
User.objects.count()

# Get unverified users
User.objects.filter(verification_code__isnull=False)

# Get users created in last 7 days
one_week_ago = timezone.now() - timedelta(days=7)
User.objects.filter(date_joined__gte=one_week_ago)

# Create a new user
User.objects.create_user(
    email='newuser@example.com',
    password='secure_password',
    name='New User'
)
```

## Development Notes

- This project uses Docker for containerized development
- Database is automatically configured via docker-compose
- Static files are collected automatically on container startup
- For production deployment, see [../DOCKER_SETUP.md](../DOCKER_SETUP.md)

## Related Documentation

- **[../README.md](../README.md)** - Project overview and quick start
- **[../DOCKER_SETUP.md](../DOCKER_SETUP.md)** - Docker setup, development tools, and production deployment
