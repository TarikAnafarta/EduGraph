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
- **Frontend**: D3.js, Vis.js
- **Data Format**: JSON
- **Database**: SQLite (default)

For detailed setup instructions and API documentation:
- See `backend/README.md` for backend setup and API details
- Check `requirements.txt` for Python dependencies

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

### Third-Party Libraries
- D3.js (BSD License)
- Vis.js (Apache License 2.0)
- Django (BSD License)
