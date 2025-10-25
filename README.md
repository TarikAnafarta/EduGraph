# EduGraph - Curriculum Learning Graph Visualization

EduGraph is a modular system for visualizing curriculum learning graphs with interactive visualizations. It processes curriculum data from JSON files and creates interactive force-directed graphs showing the relationships between subjects, topics, and learning outcomes.

## Features

- Interactive D3.js-based graph visualization
- RESTful API for data access
- Dynamic force-directed layout with zoom and pan
- Color coding based on performance scores
- Support for hierarchical curriculum data
- Both static HTML and server-based visualization options

## Project Structure

- `backend/` - Django backend with REST API
- `frontend/` - Static files and templates
- `shared/` - Curriculum data files
- `src/` - Core graph processing logic
- `lib/` - Third-party libraries

## Technology Stack

- **Backend**: Django, Django REST Framework
- **Frontend**: D3.js
- **Data Format**: JSON
- **Database**: PostgreSQL

## Getting Started

### Docker Setup (Recommended)

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
- Web Application: http://localhost:8000
- API Endpoints: http://localhost:8000/api/
- Admin Panel: http://localhost:8000/admin/

For detailed Docker instructions, troubleshooting, and production setup, see **[DOCKER_SETUP.md](DOCKER_SETUP.md)**.

## Documentation

- **[DOCKER_SETUP.md](DOCKER_SETUP.md)** - Complete Docker setup, development tools, production deployment, and troubleshooting
- **[backend/README.md](backend/README.md)** - Backend API endpoints, Django shell commands, and database queries

## API Endpoints

Once the application is running, you can access:

### Graph Data
- `GET /api/graph/data/` - Complete graph data (nodes + links)
- `GET /api/graph/nodes/` - Graph nodes only
- `GET /api/graph/links/` - Graph connections only
- `GET /api/graph/stats/` - Graph statistics

### Authentication
- `POST /api/users/login/` - User login
- `POST /api/users/register/` - User registration
- `POST /api/users/verify/` - Email verification

### Views
- `/dashboard/` - Main dashboard
- `/graph/` - Interactive graph visualization (also available at `/api/graph/view/`)
- `/admin/` - Django admin panel (requires superuser)

## License

All rights reserved - see the [LICENSE](LICENSE) file for details.

### Third-Party Libraries
- D3.js (BSD License)
- Django (BSD License)
