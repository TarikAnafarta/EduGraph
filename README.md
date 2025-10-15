# EduGraph - Curriculum Learning Graph Visualization

A modular system for visualizing curriculum learning graphs with interactive D3.js visualizations.

## 📁 Project Structure

```
EduGraph/
├── src/                          # Core backend modules (canonical)
│   ├── __init__.py               # Package exports
│   ├── graph_utils.py            # Main GraphGenerator class
│   └── utils/                    # Utility modules
│       ├── __init__.py         
│       ├── colors.py            # Color utilities and mappings
│       ├── text.py              # Text processing utilities  
│       ├── data_loader.py       # JSON data loading
│       ├── graph_processor.py   # Graph node/link creation
│       └── template_manager.py  # HTML template rendering
├── templates/                    # HTML templates (canonical)
│   └── graph.html               # Main graph template
├── static/                      # Frontend assets (canonical)
│   ├── css/
│   │   └── graph.css           # Graph visualization styles
│   └── js/
│       └── graph.js            # D3.js graph implementation
├── frontend/                   # Development frontend assets (mirrors static/)
│   ├── static/
│   │   ├── css/
│   │   │   └── graph.css
│   │   └── js/
│   │       └── graph.js
│   └── templates/
│       └── graph.html
├── backend/                    # Examples and utility scripts
│   ├── generate.py             # Simple graph generation script
│   ├── examples.py             # Usage examples for web integration
│   └── src/                    # Re-exports for convenience
│       ├── __init__.py
│       ├── graph_utils.py
│       └── utils/
├── shared/                     # Shared data files
│   └── curriculum/
│       └── matematik/
│           └── matematik_kazanimlari_124_154.json
├── lib/                        # External JavaScript/CSS libraries
│   ├── bindings/
│   │   └── utils.js
│   ├── tom-select/
│   │   ├── tom-select.complete.min.js
│   │   └── tom-select.css
│   └── vis-9.1.2/
│       ├── vis-network.min.js
│       └── vis-network.css
├── main.py                     # Demo entry point
├── kazanim_graph.html          # Generated output file
└── README.md                   # This file
```

## 🏗️ Architecture Notes

- **Core Logic**: All business logic resides in `src/` - this is the canonical source
- **Frontend Assets**: Primary templates and static files are in root `templates/` and `static/`
- **Development Mirror**: `frontend/` contains development copies of frontend assets
- **Backend Utilities**: `backend/` provides convenience scripts and re-exports for web integration
- **External Libraries**: `lib/` contains vendor JavaScript and CSS files
- **Data Storage**: `shared/curriculum/` holds curriculum data files

## 🚀 Usage

### Quick Start

```python
# Generate a complete HTML visualization
python main.py
```

This creates `kazanim_graph.html` with an interactive curriculum graph visualization.

### Development Scripts

```python
# Simple generation using backend utilities
python backend/generate.py

# View integration examples
python backend/examples.py
```

### Programmatic Usage

```python
from src import GraphGenerator, get_graph_data

# Method 1: Complete generation with statistics
generator = GraphGenerator()
html_content, stats = generator.generate_from_file(
    "shared/curriculum/matematik/matematik_kazanimlari_124_154.json",
    "my_graph.html"
)
print(f"Generated {stats['nodes_count']} nodes, {stats['links_count']} links")

# Method 2: Extract data only (for APIs/custom frontends)
nodes, links = get_graph_data("shared/curriculum/matematik/matematik_kazanimlari_124_154.json")

# Method 3: Step-by-step processing for custom workflows
generator = GraphGenerator()
records = generator.load_data("shared/curriculum/matematik/matematik_kazanimlari_124_154.json")
nodes, links = generator.create_graph_data(records)
html = generator.generate_html(nodes, links)
generator.save(html, "custom_output.html")
```

## 🎯 Key Features

### Interactive Visualization
- **D3.js Force Layout**: Dynamic, physics-based node positioning
- **Responsive Design**: Adapts to different screen sizes and devices
- **Zoom & Pan**: Navigate large curriculum graphs easily
- **Keyboard Controls**: 
  - `F` to fit entire graph to view
  - `R` to reset zoom and position
- **Interactive Tooltips**: Hover for detailed node information
- **Type-based Styling**: Visual differentiation by node type (subject, topic, subtopic, learning outcome)

### Data Processing & Visualization
- **Flexible JSON Input**: Supports various curriculum data structures
- **Automatic Type Detection**: Categorizes nodes based on content
- **Score-based Color Coding**: Visual representation of success/performance scores
- **Smart Node Sizing**: Size reflects importance or difficulty level
- **Hierarchical Relationships**: Shows parent-child connections in curriculum

### Technical Architecture
- **Modular Design**: Separate concerns for data loading, processing, and rendering
- **Template System**: HTML templates separate from business logic
- **Reusable Components**: Each utility module can be used independently
- **Asset Organization**: Clear separation of CSS, JavaScript, and template files
- **Cross-platform Compatibility**: Works on Windows, macOS, and Linux

## 🔧 API Reference

### Core Classes

#### GraphGenerator
Main class for generating curriculum graphs with full control over the process.

```python
from src import GraphGenerator

# Initialize with default template directory
generator = GraphGenerator(template_dir="templates")

# Load curriculum data
records = generator.load_data("shared/curriculum/matematik/matematik_kazanimlari_124_154.json")

# Process into graph structure
nodes, links = generator.create_graph_data(records)

# Generate complete HTML visualization
html = generator.generate_html(nodes, links)

# Save to file
generator.save(html, "my_graph.html")

# Or do everything in one step
html_content, stats = generator.generate_from_file(
    "shared/curriculum/matematik/matematik_kazanimlari_124_154.json",
    "output.html"
)
```

### Utility Functions

#### High-level Functions
```python
from src import generate_graph, get_graph_data

# Simple one-step generation (backward compatible)
stats = generate_graph(
    "shared/curriculum/matematik/matematik_kazanimlari_124_154.json",
    "output.html"
)

# Extract just the graph data (for APIs, custom frontends)
nodes, links = get_graph_data("shared/curriculum/matematik/matematik_kazanimlari_124_154.json")
```

#### Individual Utility Modules
```python
from src.utils import (
    load_curriculum_data, 
    create_graph_data,
    score_to_color,
    TemplateManager
)

# Load and validate curriculum data
records = load_curriculum_data("shared/curriculum/matematik/matematik_kazanimlari_124_154.json")

# Process records into graph format
nodes, links = create_graph_data(records)

# Get color for a performance score
color = score_to_color(0.75)  # Returns hex color

# Render HTML template
tm = TemplateManager("templates")
html = tm.render_graph_html(nodes, links)
```

### Return Values

#### Stats Dictionary
```python
{
    "nodes_count": 45,
    "links_count": 67,
    "records_processed": 50,
    "node_types": {
        "konu": 5,
        "grup": 12,
        "alt_grup": 15,
        "kazanım": 13
    }
}
```

## 🎨 Customization

### Custom Templates

Create your own HTML template in the `templates/` directory:

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>My Custom Curriculum Graph</title>
    <link rel="stylesheet" href="static/css/graph.css">
    <!-- Add your custom CSS -->
    <style>
        /* Custom styling */
        .custom-node { border: 2px solid #gold; }
    </style>
</head>
<body>
    <div id="graph-container">
        <div id="graph"></div>
        <div id="controls">
            <!-- Custom controls -->
            <button onclick="fitGraph()">Fit to Screen</button>
            <button onclick="resetView()">Reset View</button>
        </div>
    </div>
    
    <!-- Include libraries -->
    <script src="lib/vis-9.1.2/vis-network.min.js"></script>
    <script src="static/js/graph.js"></script>
    
    <script>
        // Your graph data will be injected here
        const nodes = {{NODES}};
        const links = {{LINKS}};
        
        // Initialize with custom options
        initializeGraph('graph', nodes, links, {
            physics: { enabled: true },
            interaction: { zoomView: true }
        });
    </script>
</body>
</html>
```

### Custom Styling

Modify `static/css/graph.css` or create your own CSS file:

```css
/* Custom background */
html, body {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    font-family: 'Arial', sans-serif;
}

/* Customize graph container */
#graph {
    border: 3px solid #333;
    border-radius: 10px;
    box-shadow: 0 4px 8px rgba(0,0,0,0.1);
}

/* Custom tooltip styling */
.tooltip {
    background: rgba(0, 0, 0, 0.9);
    color: #fff;
    border-radius: 8px;
    padding: 12px;
    font-size: 14px;
    box-shadow: 0 2px 10px rgba(0,0,0,0.3);
}

/* Node type specific styles */
.node-konu { fill: #ff6b6b; }
.node-grup { fill: #4ecdc4; }
.node-kazanım { fill: #45b7d1; }
```

### Custom Data Processing

Extend the processing pipeline by creating custom processors:

```python
from src.utils.graph_processor import GraphProcessor

class CustomGraphProcessor(GraphProcessor):
    def _create_node(self, record):
        """Override node creation with custom logic."""
        node = super()._create_node(record)
        
        # Add custom fields
        node['difficulty_level'] = self._calculate_difficulty(record)
        node['prerequisites'] = record.get('onkoşullar', [])
        node['learning_time'] = record.get('öğrenme_süresi', 60)
        
        # Custom sizing based on importance
        if record.get('kritik_kazanım'):
            node['size'] = node['size'] * 1.5
            
        return node
    
    def _calculate_difficulty(self, record):
        """Custom difficulty calculation."""
        score = record.get('başarı_puanı', 0.5)
        return "Hard" if score < 0.3 else "Medium" if score < 0.7 else "Easy"

# Use custom processor
from src.utils.data_loader import load_curriculum_data

processor = CustomGraphProcessor()
records = load_curriculum_data("my_data.json")
nodes, links = processor.create_graph_data(records)
```

### Environment Configuration

Create different configurations for development and production:

```python
# config.py
import os

class Config:
    TEMPLATE_DIR = "templates"
    STATIC_DIR = "static"
    OUTPUT_DIR = "output"
    
class DevelopmentConfig(Config):
    DEBUG = True
    TEMPLATE_DIR = "frontend/templates"
    STATIC_DIR = "frontend/static"
    
class ProductionConfig(Config):
    DEBUG = False
    OUTPUT_DIR = "/var/www/graphs"

# Use in your application
config = DevelopmentConfig() if os.getenv('DEV') else ProductionConfig()
generator = GraphGenerator(template_dir=config.TEMPLATE_DIR)
```

## � Data Format

The system expects JSON files with curriculum data in the following structure:

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

### Required Fields
- `id`: Unique identifier for the node
- `node_type`: Type of curriculum element (`konu`, `grup`, `alt_grup`, `kazanım`)
- `baslik`: Display title for the node

### Optional Fields
- `kazanim_kodu`: Curriculum code (e.g., "9.1.1.1")
- `konu`: Subject area
- `sinif`: Grade level (integer)
- `test`: Test type (e.g., "TYT", "AYT")
- `basari_puani`: Success score (0.0 to 1.0) - affects node color
- `node_size`: Visual size of the node (1-10)
- `parent_id`: ID of parent node for hierarchical relationships

### Node Types
- **`konu`**: Subject/Topic (e.g., "Matematik", "Geometri")
- **`grup`**: Major group within a subject (e.g., "Sayılar ve Cebir")
- **`alt_grup`**: Subgroup or chapter (e.g., "Rasyonel Sayılar")
- **`kazanım`**: Learning outcome/objective (specific skills or knowledge)

### Example with Hierarchy
```json
{
  "Matematik Kazanımları": [
    {
      "id": "mat_9",
      "node_type": "konu",
      "baslik": "9. Sınıf Matematik",
      "sinif": 9
    },
    {
      "id": "mat_9_kumeler",
      "node_type": "grup", 
      "baslik": "Kümeler",
      "parent_id": "mat_9",
      "sinif": 9
    },
    {
      "id": "mat_9_kumeler_temel",
      "node_type": "alt_grup",
      "baslik": "Temel Kavramlar", 
      "parent_id": "mat_9_kumeler",
      "sinif": 9
    },
    {
      "id": "mat_9_kumeler_temel_001",
      "node_type": "kazanım",
      "baslik": "Küme kavramını açıklar",
      "kazanim_kodu": "9.1.1.1",
      "parent_id": "mat_9_kumeler_temel",
      "basari_puani": 0.85,
      "node_size": 3,
      "sinif": 9,
      "test": "TYT"
    }
  ]
}
```

### Color Coding by Success Score
- **Red (0.0 - 0.3)**: Low success rate, needs attention
- **Orange (0.3 - 0.5)**: Below average performance
- **Yellow (0.5 - 0.7)**: Average performance  
- **Light Green (0.7 - 0.85)**: Good performance
- **Dark Green (0.85 - 1.0)**: Excellent performance

## �️ Installation & Setup

### Prerequisites
- Python 3.8 or higher
- Modern web browser (Chrome, Firefox, Safari, Edge)

### Quick Setup
```bash
# Clone or download the project
cd EduGraph

# Install Python dependencies (if any)
pip install -r requirements.txt  # if requirements.txt exists

# Run the demo
python main.py
```

### Development Setup
```bash
# Set up virtual environment (recommended)
python -m venv .venv
.venv\Scripts\activate  # Windows
# or
source .venv/bin/activate  # macOS/Linux

# Install development dependencies
pip install -r requirements-dev.txt  # if exists

# Run examples
python backend/examples.py
python backend/generate.py
```

### Using in Your Project
```python
# Add the src directory to your Python path
import sys
sys.path.append('path/to/EduGraph')

from src import GraphGenerator, get_graph_data

# Now you can use the library
nodes, links = get_graph_data("your_data.json")
```

## 🔬 Examples & Use Cases

### Web API Integration
```python
# Flask example
from flask import Flask, jsonify
from src import get_graph_data

app = Flask(__name__)

@app.route('/api/graph/<curriculum>')
def get_curriculum_graph(curriculum):
    try:
        nodes, links = get_graph_data(f"shared/curriculum/{curriculum}.json")
        return jsonify({
            "success": True,
            "data": {"nodes": nodes, "links": links}
        })
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500
```

### Data Analysis
```python
from src import GraphGenerator

# Analyze curriculum structure
generator = GraphGenerator()
records = generator.load_data("shared/curriculum/matematik/matematik_kazanimlari_124_154.json")
nodes, links = generator.create_graph_data(records)

# Find learning outcomes with low success rates
low_performers = [n for n in nodes if n.get('basari_puani', 1) < 0.5]
print(f"Found {len(low_performers)} learning outcomes needing attention")

# Analyze connectivity
avg_connections = len(links) / len(nodes)
print(f"Average connections per node: {avg_connections:.2f}")
```

### Batch Processing
```python
import os
from src import generate_graph

# Process multiple curriculum files
curriculum_dir = "shared/curriculum"
output_dir = "generated_graphs"

for subject_dir in os.listdir(curriculum_dir):
    subject_path = os.path.join(curriculum_dir, subject_dir)
    if os.path.isdir(subject_path):
        for file in os.listdir(subject_path):
            if file.endswith('.json'):
                input_path = os.path.join(subject_path, file)
                output_path = os.path.join(output_dir, f"{subject_dir}_{file.replace('.json', '.html')}")
                
                stats = generate_graph(input_path, output_path)
                print(f"Generated {output_path}: {stats['nodes_count']} nodes")
```

## 🚀 Roadmap & Future Enhancements

### Near Term (v2.0)
- [ ] **Enhanced Interactivity**: Node selection, multi-select, drag-and-drop
- [ ] **Filtering System**: Filter by grade level, subject, performance score
- [ ] **Search Functionality**: Find specific learning outcomes or topics
- [ ] **Export Options**: Save as PNG, SVG, or PDF
- [ ] **Performance Optimization**: Better handling of large curriculum datasets

### Medium Term (v3.0)
- [ ] **REST API**: Dynamic data loading and real-time updates
- [ ] **Multiple Layout Options**: Hierarchical tree, circular, force-directed variants
- [ ] **Analytics Dashboard**: Performance metrics and insights
- [ ] **Collaborative Features**: Comments, annotations, sharing
- [ ] **Mobile App**: Native mobile visualization

### Long Term (v4.0+)
- [ ] **AI-Powered Insights**: Automatic curriculum gap analysis
- [ ] **Plugin Architecture**: Custom visualization types and data sources
- [ ] **Real-time Collaboration**: Multi-user editing and viewing
- [ ] **Integration APIs**: Connect with LMS platforms, assessment tools
- [ ] **Accessibility Features**: Screen reader support, keyboard navigation

### Community Contributions Welcome
- 📝 Documentation improvements
- 🐛 Bug fixes and testing
- 🎨 New visualization themes
- 🔌 Plugin development
- 🌍 Internationalization support

## 🤝 Contributing

### Development Guidelines
1. **Code Style**: Follow PEP 8 for Python code
2. **Architecture**: Maintain separation between data processing (`src/`) and presentation layers
3. **Documentation**: Add docstrings to all public methods and classes
4. **Testing**: Write tests for new functionality
5. **Backwards Compatibility**: Avoid breaking existing APIs

### Getting Started
```bash
# Fork the repository
git clone https://github.com/yourusername/EduGraph.git
cd EduGraph

# Create a feature branch
git checkout -b feature/your-feature-name

# Make your changes
# ... edit files ...

# Test your changes
python main.py
python backend/examples.py

# Commit and push
git add .
git commit -m "Add: your feature description"
git push origin feature/your-feature-name

# Create a pull request
```

### Code Structure Guidelines
- **Core Logic**: Keep all business logic in `src/`
- **Examples**: Add usage examples to `backend/examples.py`
- **Templates**: HTML templates go in `templates/`
- **Assets**: CSS/JS files go in `static/`
- **Data**: Sample data files go in `shared/curriculum/`

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

### Third-Party Libraries
- **D3.js**: Data visualization (BSD License)
- **Vis.js**: Network visualization (Apache License 2.0)
- **Tom Select**: Enhanced select controls (Apache License 2.0)

## 📞 Support & Contact

- **Issues**: Report bugs and request features via GitHub Issues
- **Documentation**: Check the README and inline code documentation
- **Examples**: See `backend/examples.py` for integration patterns
- **Community**: Join discussions in GitHub Discussions

---

**Made with ❤️ for educators and curriculum designers**

*EduGraph helps visualize the complex relationships in educational curricula, making it easier to understand learning pathways and identify areas for improvement.*
