/**
 * Graph visualization using D3.js
 * Renders curriculum data as an interactive force-directed graph
 */

class GraphVisualizer {
  constructor(containerId, nodes, links) {
    this.containerId = containerId;
    this.nodes = nodes;
    this.links = links;
    this.width = 0;
    this.height = 0;
    this.svg = null;
    this.simulation = null;
    this.tooltip = null;
    
    this.init();
  }
  
  init() {
    const container = document.getElementById(this.containerId);
    this.width = container.clientWidth;
    this.height = container.clientHeight;
    
    this.createSVG();
    this.createTooltip();
    this.createGraph();
    this.setupSimulation();
    this.setupZoom();
    this.setupKeyboardControls();
  }
  
  createSVG() {
    this.svg = d3.select(`#${this.containerId}`)
      .append('svg')
      .attr('width', this.width)
      .attr('height', this.height);
      
    this.zoomLayer = this.svg.append('g');
    this.linkLayer = this.zoomLayer.append('g')
      .attr('stroke', '#2b3147')
      .attr('stroke-opacity', 0.5);
    this.nodeLayer = this.zoomLayer.append('g');
    this.labelLayer = this.zoomLayer.append('g');
  }
  
  createTooltip() {
    this.tooltip = d3.select('body')
      .append('div')
      .attr('class', 'tooltip')
      .style('opacity', 0);
  }
  
  createGraph() {
    // Create links
    this.link = this.linkLayer
      .selectAll('line')
      .data(this.links)
      .enter()
      .append('line')
      .attr('stroke-width', 1);
    
    // Create nodes
    this.node = this.nodeLayer
      .selectAll('circle')
      .data(this.nodes, d => d.id)
      .enter()
      .append('circle')
      .attr('r', d => d.r)
      .attr('fill', d => d.color || '#90a4ae')
      .attr('stroke', '#0f111a')
      .attr('stroke-width', 1.2)
      .style('cursor', 'pointer');
    
    // Create labels (only for konu, grup, alt_grup)
    const labelNodes = this.nodes.filter(d => 
      d.type === 'konu' || d.type === 'grup' || d.type === 'alt_grup'
    );
    
    this.labels = this.labelLayer
      .selectAll('text')
      .data(labelNodes, d => d.id)
      .enter()
      .append('text')
      .text(d => d.label || '')
      .attr('font-size', d => Math.max(12, d.r * 0.52))
      .attr('fill', '#c7d0e0')
      .attr('text-anchor', 'middle')
      .attr('dy', d => d.r + 14);
    
    // Setup tooltip events
    this.node
      .on('mouseover', (event, d) => {
        this.tooltip.html(d.title).style('opacity', 1);
      })
      .on('mousemove', (event) => {
        this.tooltip
          .style('left', (event.pageX + 12) + 'px')
          .style('top', (event.pageY + 12) + 'px');
      })
      .on('mouseout', () => {
        this.tooltip.style('opacity', 0);
      });
  }
  
  linkDistance(link) {
    const source = link.source;
    const target = link.target;
    const radiusSum = (source.r || 14) + (target.r || 14);
    let baseDistance = 30 + radiusSum * 0.9;
    
    if (source.type === 'konu' || target.type === 'konu') {
      baseDistance += 60;
    }
    if (target.type === 'kazanım') {
      baseDistance += 5;
    }
    
    return baseDistance;
  }
  
  setupSimulation() {
    this.simulation = d3.forceSimulation(this.nodes)
      .force('link', d3.forceLink(this.links)
        .id(d => d.id)
        .distance(this.linkDistance.bind(this))
        .strength(0.12)
      )
      .force('charge', d3.forceManyBody().strength(-1600))
      .force('center', d3.forceCenter(this.width / 2, this.height / 2))
      .force('x', d3.forceX(this.width / 2).strength(0.03))
      .force('y', d3.forceY(this.height / 2).strength(0.03))
      .force('collide', d3.forceCollide()
        .radius(d => d.r + 4)
        .iterations(2)
      );
    
    this.simulation.on('tick', () => {
      this.link
        .attr('x1', d => d.source.x)
        .attr('y1', d => d.source.y)
        .attr('x2', d => d.target.x)
        .attr('y2', d => d.target.y);
      
      this.node
        .attr('cx', d => d.x)
        .attr('cy', d => d.y);
      
      this.labels
        .attr('x', d => d.x)
        .attr('y', d => d.y);
    });
    
    this.simulation.on('end', () => {
      setTimeout(() => this.fitToView(), 100);
    });
    
    // Initial fit after a delay
    setTimeout(() => this.fitToView(), 1200);
  }
  
  setupZoom() {
    this.zoom = d3.zoom()
      .scaleExtent([0.2, 4])
      .on('zoom', (event) => {
        this.zoomLayer.attr('transform', event.transform);
      });
    
    this.svg.call(this.zoom);
  }
  
  setupKeyboardControls() {
    window.addEventListener('keydown', (event) => {
      const key = event.key.toLowerCase();
      if (key === 'r') {
        this.resetView();
      } else if (key === 'f') {
        this.fitToView();
      }
    });
  }
  
  fitToView(padding = 60) {
    const xs = this.nodes.map(n => n.x);
    const ys = this.nodes.map(n => n.y);
    const minX = Math.min(...xs) - padding;
    const maxX = Math.max(...xs) + padding;
    const minY = Math.min(...ys) - padding;
    const maxY = Math.max(...ys) + padding;
    const width = maxX - minX;
    const height = maxY - minY;
    
    if (!(isFinite(width) && isFinite(height) && width > 0 && height > 0)) {
      return;
    }
    
    const scale = Math.min(this.width / width, this.height / height, 1) * 0.9;
    const translateX = (this.width - width * scale) / 2 - minX * scale;
    const translateY = (this.height - height * scale) / 2 - minY * scale;
    
    this.svg.transition()
      .duration(700)
      .call(this.zoom.transform, 
        d3.zoomIdentity.translate(translateX, translateY).scale(scale)
      );
  }
  
  resetView() {
    this.svg.transition()
      .duration(600)
      .call(this.zoom.transform, d3.zoomIdentity);
  }
}

// Utility function to initialize the graph
function initializeGraph(containerId, nodes, links) {
  return new GraphVisualizer(containerId, nodes, links);
}
