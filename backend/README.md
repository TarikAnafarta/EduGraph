# EduGraph Backend

Django-based backend for the EduGraph curriculum visualization project.

## Setup

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run migrations:
```bash
python manage.py migrate
```

4. Create a superuser (optional):
```bash
python manage.py createsuperuser
```

## Running the Server

Start the development server:
```bash
python manage.py runserver
```

The server will start at http://localhost:8000

## API Endpoints

### Authentication
- `POST /api/users/login/` - User login
- `POST /api/users/register/` - User registration
- `GET /api/users/verify/` - Email verification

### Graph Data
- `GET /api/graph/data/` - Get complete graph data
- `GET /api/graph/nodes/` - Get graph nodes
- `GET /api/graph/links/` - Get graph connections
- `GET /api/graph/stats/` - Get graph statistics

### Views
- `/dashboard/` - Main dashboard
- `/graph/view/` - Graph visualization
- `/admin/` - Admin interface (requires superuser)

## Project Structure

- `artifacts/` - Graph data models and API views
- `users/` - User management and authentication
- `common/` - Shared utilities and serializers
- `src/` - Core graph processing logic
- `templates/` - HTML templates

## Note

This is a development setup. For production, make sure to:
- Configure proper security settings
- Use a production-grade server (e.g., Gunicorn)
- Set up proper static file serving
- Configure a proper database (default is SQLite)
