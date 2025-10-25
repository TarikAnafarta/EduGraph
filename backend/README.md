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

### Graph Data
- `GET /api/graph/data/` - Get complete graph data (nodes + links)
- `GET /api/graph/nodes/` - Get graph nodes only
- `GET /api/graph/links/` - Get graph connections only
- `GET /api/graph/stats/` - Get graph statistics

### Views
- `/dashboard/` - Main dashboard
- `/graph/` - Interactive graph visualization
- `/api/graph/view/` - Interactive graph visualization (API route)
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

## 🧭 Git Flow & Merge Strategy

This section explains our **Git flow process** and the **merge strategy** our development team follows.

### 🌿 Environments Overview

We maintain **two main environments**:

- **`dev`** → The development branch where all new features are tested together. This branch is always **ahead** of production.
- **`production`** → The stable branch used for **live deployments**.

Every new feature must be developed in its **own branch**, which should be **created from the `dev` branch**.

### 🚀 Standard Git Flow

Follow the steps below when working on a new feature.

1. **Create a new feature branch** from `dev`  
   ```bash
   git checkout dev
   git pull origin dev
   git checkout -b <feature-name>
   ```

2. **Develop your feature**  
   Work on your implementation and commit regularly.  
   ```bash
   git add .
   git commit -m "Implement <feature-name>"
   ```

3. **Create a Pull Request (PR)**  
   Push your branch and open a PR **from your feature branch → `dev`**.  
   ```bash
   git push origin <feature-name>
   ```
   Then, request a **code review** from another developer.

4. **After approval**, follow the merge strategy below.

### ⚙️ Merge Strategy (Clean History Approach)

We care deeply about maintaining a **clear and linear commit history**.  
All developers must follow the same merge procedure.

> **Note:** Make sure your branch was originally created from `dev`.

#### Steps

1. Open your terminal in your project directory  
   ```bash
   cd <your-project-directory>
   ```

2. Switch to your feature branch  
   ```bash
   git checkout <your-branch-name>
   ```

3. Rebase your branch with the latest `dev` branch  
   ```bash
   git fetch origin
   git rebase origin/dev
   ```

4. Push the rebased branch (force push)  
   ```bash
   git push -f
   ```

5. Switch to the `dev` branch  
   ```bash
   git checkout dev
   ```

6. Merge your feature branch into `dev`  
   ```bash
   git merge <your-branch-name>
   ```

7. Push the updated `dev` branch  
   ```bash
   git push origin dev
   ```

After completing these steps, your PR will appear as **fast-forward merged** on GitHub, ensuring a clean project history.

## Related Documentation

- **[../README.md](../README.md)** - Project overview and quick start
- **[../DOCKER_SETUP.md](../DOCKER_SETUP.md)** - Docker setup, development tools, and production deployment
