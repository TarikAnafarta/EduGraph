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
- `POST /api/users/verify/` - Email verification
- `POST /api/users/resend-verification/` - Resend email verification
- `POST /api/users/forgot-password/` - Request password reset
- `POST /api/users/reset-password/` - Reset password
- `POST /api/users/reset-password/validate/` - Validate password reset token
- `GET/PUT/PATCH /api/users/me/` - Retrieve or update current user

### Graph Data
- `GET /api/graph/data/` - Get complete graph data (nodes + links)
- `GET /api/graph/nodes/` - Get graph nodes only
- `GET /api/graph/links/` - Get graph connections only
- `GET /api/graph/stats/` - Get graph statistics

## Notes

- React SPA handles all UI under `frontend/`. No Django templates are used.
- Static files are collected for admin via `collectstatic`. Nginx serves `/static` and `/media` in Docker.
- Use `docker-compose exec web python manage.py <command>` for management tasks.

## More docs

- See project README at [../README.md](../README.md)
