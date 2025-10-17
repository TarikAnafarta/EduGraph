# EduGraph - Curriculum Learning Graph Visualization

EduGraph is a modular system for visualizing curriculum learning graphs with interactive D3.js visualizations. It processes curriculum data from JSON files and creates interactive force-directed graphs showing the relationships between subjects, topics, and learning outcomes.

## Quick Start

### Option 1: API Server (Recommended)

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Start the API server:**
   ```bash
   python run_api.py
   ```

3. **View the visualization:**
   Open your browser to: http://localhost:8000/api/graph/view/

### Option 2: Generate Static HTML File

```bash
python main.py
```

This creates `kazanim_graph.html` which you can open in any browser.

## How to Use

### Interactive Visualization
Once you have the visualization running, you can:
- **Zoom**: Use mouse wheel to zoom in/out
- **Pan**: Drag to move around the graph
- **Hover**: Move mouse over nodes to see details
- **Keyboard shortcuts**: Press `F` to fit graph to view, `R` to reset

### API Endpoints

The API server provides several endpoints for accessing graph data:

| Endpoint | Description |
|----------|-------------|
| `/api/graph/view/` | Interactive HTML visualization |
| `/api/graph/data/` | Complete graph data (JSON) |
| `/api/graph/nodes/` | Graph nodes only |
| `/api/graph/links/` | Graph connections only |
| `/api/graph/stats/` | Graph statistics |

### Using the API

#### Get complete graph data:
```bash
curl http://localhost:8000/api/graph/data/
```

#### Filter nodes by type:
```bash
curl http://localhost:8000/api/graph/nodes/?type=kazanım
```

#### Using Python:
```python
import requests

response = requests.get('http://localhost:8000/api/graph/data/')
data = response.json()
nodes = data['data']['nodes']
links = data['data']['links']
```

### Testing the API

Run the automated test suite:
```bash
python test_api.py
```

## Programmatic Usage

### Basic Usage
```python
from src import GraphGenerator, get_graph_data

# Method 1: Complete generation with statistics
generator = GraphGenerator()
html_content, stats = generator.generate_from_file(
    "shared/curriculum/matematik/matematik_kazanimlari_124_154.json",
    "my_graph.html"
)
print(f"Generated {stats['nodes_count']} nodes, {stats['links_count']} links")

# Method 2: Get data only (for APIs/custom processing)
nodes, links = get_graph_data("shared/curriculum/matematik/matematik_kazanimlari_124_154.json")

# Method 3: Step-by-step processing
generator = GraphGenerator()
records = generator.load_data("data.json")
nodes, links = generator.create_graph_data(records)
html = generator.generate_html(nodes, links)
generator.save(html, "output.html")
```

### Integration Examples

#### Flask Web API
```python
from flask import Flask, jsonify
from src import get_graph_data

app = Flask(__name__)

@app.route('/api/curriculum/<subject>')
def get_curriculum(subject):
    nodes, links = get_graph_data(f"shared/curriculum/{subject}.json")
    return jsonify({"nodes": nodes, "links": links})
```

#### Data Analysis
```python
# Find learning outcomes with low success rates
nodes, links = get_graph_data("data.json")
low_performers = [n for n in nodes if n.get('basari_puani', 1) < 0.5]
print(f"Found {len(low_performers)} outcomes needing attention")
```

## Data Format

EduGraph expects JSON files with curriculum data in the following structure:

### Basic Structure
```json
{
  "Matematik Kazanımları": [
    {
      "id": "mat_9_1_001",
      "node_type": "kazanım",
      "baslik": "Kümelerde Temel Kavramlar",
      "kazanim_kodu": "9.1.1.1", 
      "konu": "Kümeler",
      "sinif": 9,
      "test": "TYT",
      "basari_puani": 0.75,
      "node_size": 4,
      "parent_id": "mat_9_1"
    }
  ]
}
```

### Node Types
- **`konu`**: Subject/Topic (e.g., "Matematik", "Geometri")
- **`grup`**: Major group within a subject (e.g., "Sayılar ve Cebir")
- **`alt_grup`**: Subgroup or chapter (e.g., "Rasyonel Sayılar")
- **`kazanım`**: Learning outcome/objective (specific skills or knowledge)

### Required Fields
- `id`: Unique identifier
- `node_type`: Type of curriculum element
- `baslik`: Display title

### Optional Fields
- `kazanim_kodu`: Curriculum code
- `basari_puani`: Success score (0.0 to 1.0) - affects node color
- `parent_id`: ID of parent node for hierarchical relationships

## Features

### Interactive Visualization
- D3.js force-directed layout with physics simulation
- Zoom and pan navigation
- Interactive tooltips with detailed information
- Color coding based on performance scores
- Responsive design for different screen sizes

### Technical Features
- RESTful API for data access
- CORS support for cross-origin requests
- Modular architecture with reusable components
- Static HTML generation for offline use
- Comprehensive test suite

## Installation & Setup

### Prerequisites
- Python 3.8 or higher
- Modern web browser

### Installation
```bash
# Clone or download the project
cd EduGraph

# Install dependencies
pip install -r requirements.txt

# Initialize database (for API server)
python manage.py migrate
```

### Running
```bash
# Option 1: API server
python run_api.py

# Option 2: Static HTML generation
python main.py
```

## Configuration

### CORS Settings
For production, edit `backend/settings.py`:
```python
CORS_ALLOWED_ORIGINS = [
    "https://yourdomain.com",
]
```

### Custom Templates
Create custom HTML templates in the `templates/` directory and modify CSS in `static/css/graph.css`.

## Troubleshooting

### Common Issues

**Server won't start:**
```bash
# Check if port 8000 is in use
netstat -an | findstr :8000  # Windows
# Use a different port
python manage.py runserver 8080
```

**Import errors:**
```bash
pip install -r requirements.txt --force-reinstall
```

**Database errors:**
```bash
rm db.sqlite3
python manage.py migrate
```

**Graph visualization not loading:**
- Clear browser cache: `Ctrl+Shift+R` (Windows/Linux) or `Cmd+Shift+R` (Mac)
- Check browser console (F12) for JavaScript errors
- Verify static files are served correctly: `python check_config.py`

**Static files (CSS/JS) not loading:**
- Ensure server is running in debug mode (default)
- Check that all files exist in `static/` and `lib/` directories
- Restart the server if static files were modified

## Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/your-feature`
3. Make your changes
4. Test your changes: `python test_api.py`
5. Commit and push: `git commit -m "Add feature"`
6. Create a pull request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

### Third-Party Libraries
- D3.js: Data visualization (BSD License)
- Vis.js: Network visualization (Apache License 2.0)
- Django: Web framework (BSD License)

---

**EduGraph helps visualize the complex relationships in educational curricula, making it easier to understand learning pathways and identify areas for improvement.**
