# EduGraph - Curriculum Learning Graph Visualization

EduGraph visualizes curriculum learning graphs with a Django REST API and a React (Vite) frontend.

## Features

- React SPA (Vite) for UI: auth, dashboard, settings, graph
- Django + DRF API for graph data and user accounts
- PostgreSQL via Docker Compose

## Project Structure

- `backend/` - Django backend (API only)
- `frontend/` - React app (Vite)
- `shared/` - Curriculum data (JSON)
- `src/` - Core graph processing (Python)
- `nginx/` - Nginx config for prod/proxy

## Quick Start (Docker)

The easiest way to get started. Docker handles all dependencies and database setup automatically.

**Prerequisites:**
- Docker Desktop (Windows/Mac) or Docker Engine (Linux)
- Docker Compose v2.0+

**Quick Start:**

```powershell
# Copy environment file
Copy-Item .env.example .env

# Start all services (web + database)
docker-compose up

# Create a superuser for admin access
docker-compose exec web python manage.py createsuperuser
```

**Access the application:**
- API: http://localhost:8000/api/
- Admin: http://localhost:8000/admin/
- Frontend: run in frontend/ with npm run dev (or serve separately in prod)

## Documentation

- backend/README.md — Backend API and management notes
- frontend/README.md — Frontend setup (Vite) and project structure

## License

All rights reserved - see the [LICENSE](LICENSE) file for details.

### Third-Party Libraries
- React, React Router, Vite
- D3.js
- Django, Django REST Framework
- Cloudinary (django-cloudinary-storage)
