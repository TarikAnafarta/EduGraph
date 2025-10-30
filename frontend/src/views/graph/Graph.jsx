import React, { useEffect, useRef, useState } from 'react'
import * as d3 from 'd3'
import './graph.css'

function GraphVisualizer(container, nodes, links){
  const width = container.clientWidth
  const height = container.clientHeight

  const svg = d3.select(container).append('svg').attr('width', width).attr('height', height)
  const zoomLayer = svg.append('g')
  const linkLayer = zoomLayer.append('g').attr('stroke', '#2b3147').attr('stroke-opacity', 0.5)
  const nodeLayer = zoomLayer.append('g')
  const labelLayer = zoomLayer.append('g')

  const link = linkLayer.selectAll('line').data(links).enter().append('line').attr('stroke-width', 1)
  const node = nodeLayer.selectAll('circle').data(nodes, d=>d.id).enter().append('circle')
    .attr('r', d=>d.r).attr('fill', d=>d.color || '#90a4ae').attr('stroke','#0f111a').attr('stroke-width',1.2)

  const labelNodes = nodes.filter(d => ['konu','grup','alt_grup'].includes(d.type))
  const labels = labelLayer.selectAll('text').data(labelNodes, d=>d.id).enter().append('text')
    .text(d=>d.label || '').attr('font-size', d=>Math.max(12, d.r*0.52)).attr('fill','#c7d0e0')
    .attr('text-anchor','middle').attr('dy', d=>d.r+14)

  const simulation = d3.forceSimulation(nodes)
    .force('link', d3.forceLink(links).id(d=>d.id).distance(linkDistance).strength(0.12))
    .force('charge', d3.forceManyBody().strength(-1600))
    .force('center', d3.forceCenter(width/2, height/2))
    .force('x', d3.forceX(width/2).strength(0.03))
    .force('y', d3.forceY(height/2).strength(0.03))
    .force('collide', d3.forceCollide().radius(d=>d.r+4).iterations(2))

  simulation.on('tick', () => {
    link.attr('x1', d=>d.source.x).attr('y1', d=>d.source.y).attr('x2', d=>d.target.x).attr('y2', d=>d.target.y)
    node.attr('cx', d=>d.x).attr('cy', d=>d.y)
    labels.attr('x', d=>d.x).attr('y', d=>d.y)
  })

  const zoom = d3.zoom().scaleExtent([0.2,4]).on('zoom', (e)=> zoomLayer.attr('transform', e.transform))
  svg.call(zoom)

  function linkDistance(link){
    const s = link.source, t = link.target
    const radiusSum = (s.r||14) + (t.r||14)
    let d = 30 + radiusSum*0.9
    if (s.type==='konu' || t.type==='konu') d += 60
    if (t.type==='kazanım') d += 5
    return d
  }

  function fitToView(padding=60){
    const xs = nodes.map(n=>n.x), ys = nodes.map(n=>n.y)
    const minX=Math.min(...xs)-padding, maxX=Math.max(...xs)+padding
    const minY=Math.min(...ys)-padding, maxY=Math.max(...ys)+padding
    const w=maxX-minX, h=maxY-minY
    if (!(isFinite(w)&&isFinite(h)&&w>0&&h>0)) return
    const scale = Math.min(width/w, height/h, 1)*0.9
    const tx=(width-w*scale)/2 - minX*scale
    const ty=(height-h*scale)/2 - minY*scale
    svg.transition().duration(700).call(zoom.transform, d3.zoomIdentity.translate(tx,ty).scale(scale))
  }

  setTimeout(()=>fitToView(), 1200)
}

export default function GraphPage(){
  const ref = useRef(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')

  useEffect(()=>{
    async function load(){
      try {
        setLoading(true)
        setError('')
        const res = await fetch('http://localhost:8000/api/graph/data/')
        const json = await res.json()
        if (json.status !== 'success') throw new Error(json.message || 'API error')
        GraphVisualizer(ref.current, json.data.nodes, json.data.links)
      } catch (e) {
        setError(e.message)
      } finally {
        setLoading(false)
      }
    }
    load()
  }, [])

  return (
    <div style={{height:'100vh', background:'#0f111a', color:'#e6e6e6'}}>
      <div style={{position:'fixed', top:12, right:12, background:'#151826', border:'1px solid #2a3042', padding:'10px 12px', borderRadius:10, fontSize:13, zIndex:10}}>
        <div style={{display:'flex', gap:8, alignItems:'center', margin:'4px 0'}}><span style={{display:'inline-block', width:14, height:14, borderRadius:'50%', background:'#1976d2'}}></span> Konu (başlık)</div>
        <div style={{display:'flex', gap:8, alignItems:'center', margin:'4px 0'}}><span style={{display:'inline-block', width:14, height:14, borderRadius:'50%', background:'#8e24aa'}}></span> Grup (başlık)</div>
        <div style={{display:'flex', gap:8, alignItems:'center', margin:'4px 0'}}><span style={{display:'inline-block', width:14, height:14, borderRadius:'50%', background:'#00897b'}}></span> Alt Grup (başlık)</div>
        <div style={{display:'flex', gap:8, alignItems:'center', margin:'4px 0'}}><span style={{display:'inline-block', width:14, height:14, borderRadius:'50%', background:'linear-gradient(90deg,#e53935,#ffb300,#00c853)'}}></span> Kazanım (renk=başarı)</div>
        <div style={{color:'#96a0b5'}}>Büyüklük: hiyerarşi düzeyi / başarı</div>
      </div>

      {loading && <div style={{padding:20}}>Yükleniyor…</div>}
      {error && <div style={{color:'#f88', padding:20}}>Hata: {error}</div>}
      <div ref={ref} id="graph" style={{width:'100vw', height:'100vh'}}/>
    </div>
  )
}
