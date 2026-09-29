import React, { useRef, useEffect, useState } from 'react';
import { 
  Network, 
  Plus, 
  Minus, 
  Maximize2, 
  RotateCcw, 
  Sliders, 
  ExternalLink,
  Shield,
  Layers,
  ArrowRight,
  GitCommit
} from 'lucide-react';

export default function TransactionNetworkGraph({
  onSelectNode,
  selectedNodeId,
  viewMode = 'graph',
  setViewMode
}) {
  const canvasRef = useRef(null);
  const containerRef = useRef(null);
  const [zoom, setZoom] = useState(1);
  const [offset, setOffset] = useState({ x: 0, y: 0 });
  const [isDragging, setIsDragging] = useState(false);
  const [dragNode, setDragNode] = useState(null);
  const [mousePos, setMousePos] = useState({ x: 0, y: 0 });
  const [hoveredNode, setHoveredNode] = useState(null);

  // Graph Data strictly modeling the image & real multi-hop fund flow
  const nodes = [
    {
      id: '0x7fC7...a3F2',
      fullAddress: '0x7fC765629da776A1bf0C35B9A42Ef791B7b8a3F2',
      label: '0x7fC7...a3F2',
      sublabel: '(Monitored)',
      type: 'monitored',
      color: '#00d2ff',
      haloColor: 'rgba(0, 210, 255, 0.4)',
      size: 26,
      x: 0,
      y: 10,
      balance: '14.85 ETH',
      volume: '142.30 ETH',
      txCount: 84,
      riskScore: 'Medium (64/100)',
      hop: 0,
      category: 'Victim-Reported Suspect Wallet'
    },
    {
      id: '0x4e9e...21a7',
      fullAddress: '0x4e9e51c888d36154c5e39626b9e28e14675e21a7',
      label: '0x4e9e...21a7',
      type: 'entity',
      color: '#a855f7',
      size: 19,
      x: -60,
      y: -140,
      balance: '3.12 ETH',
      volume: '18.45 ETH',
      txCount: 14,
      riskScore: 'Low (22/100)',
      hop: 1,
      category: 'Intermediary Entity'
    },
    {
      id: 'Binance',
      fullAddress: '0x28C6c06298d514Db089934071355E5743bf21d60',
      label: 'Binance',
      sublabel: '(Exchange)',
      type: 'exchange',
      color: '#f59e0b',
      haloColor: 'rgba(245, 158, 11, 0.35)',
      size: 24,
      x: 140,
      y: -150,
      balance: '4,520.10 ETH',
      volume: '890,200 ETH',
      txCount: 42019,
      riskScore: 'Low / Identified Exchange',
      hop: 1,
      category: 'Exchange-Linked Cluster (Binance 8)'
    },
    {
      id: '0x8f3d...c9e2',
      fullAddress: '0x8f3d44bc2a9154ec5a7e6c9e2b1094892c90c9e2',
      label: '0x8f3d...c9e2',
      type: 'connected',
      color: '#38bdf8',
      size: 19,
      x: -160,
      y: -5,
      balance: '0.95 ETH',
      volume: '8.20 ETH',
      txCount: 9,
      riskScore: 'Medium (48/100)',
      hop: 1,
      category: 'Direct Counterparty'
    },
    {
      id: '0x3c7d...e8f1',
      fullAddress: '0x3c7d9910bf28e715ca4081ef72c091bc382ce8f1',
      label: '0x3c7d...e8f1',
      type: 'connected',
      color: '#38bdf8',
      size: 19,
      x: -100,
      y: 130,
      balance: '2.40 ETH',
      volume: '15.60 ETH',
      txCount: 18,
      riskScore: 'Low (18/100)',
      hop: 1,
      category: 'Connected Counterparty'
    },
    {
      id: '0x6a21...9b4c',
      fullAddress: '0x6a218193ac4efb8893c52e46b9a87cd831f29b4c',
      label: '0x6a21...9b4c',
      type: 'entity',
      color: '#a855f7',
      size: 19,
      x: 15,
      y: 145,
      balance: '5.80 ETH',
      volume: '34.10 ETH',
      txCount: 29,
      riskScore: 'High (76/100)',
      hop: 1,
      category: 'Suspicious Aggregator Wallet'
    },
    {
      id: 'Coinbase',
      fullAddress: '0xA090e606E30bD747d4E6245a1517EbE430F0057e',
      label: 'Coinbase',
      sublabel: '(Exchange)',
      type: 'exchange',
      color: '#3b82f6',
      haloColor: 'rgba(59, 130, 246, 0.35)',
      size: 22,
      x: 135,
      y: 110,
      balance: '2,890.00 ETH',
      volume: '450,100 ETH',
      txCount: 18902,
      riskScore: 'Low / Identified Exchange',
      hop: 1,
      category: 'Exchange-Linked Cluster (Coinbase Prime)'
    },
    {
      id: '0x91ab...d45e',
      fullAddress: '0x91ab87ca991054321bcde45f882194a20b7ed45e',
      label: '0x91ab...d45e',
      type: 'tornado',
      color: '#10b981',
      size: 19,
      x: 180,
      y: -20,
      balance: '1.10 ETH',
      volume: '42.80 ETH',
      txCount: 31,
      riskScore: 'Critical (88/100)',
      hop: 1,
      category: 'Intermediary to Mixer'
    },
    {
      id: 'Tornado Cash',
      fullAddress: '0xd90e2f925DA726b50C4Ed8D0Fb90Ad053324F31b',
      label: 'Tornado Cash',
      sublabel: '(Mixer)',
      type: 'tornado',
      color: '#10b981',
      haloColor: 'rgba(16, 185, 129, 0.35)',
      size: 21,
      x: 280,
      y: -20,
      balance: '120.50 ETH',
      volume: '150,000 ETH',
      txCount: 9400,
      riskScore: 'Critical / Sanctioned Mixer',
      hop: 2,
      category: 'Privacy Mixer Contract'
    }
  ];

  const edges = [
    { from: '0x7fC7...a3F2', to: '0x4e9e...21a7', value: '0.45 ETH', txHash: '0x4f82...19a2', speed: 0.008 },
    { from: '0x7fC7...a3F2', to: 'Binance', value: '3.50 ETH', isDashed: true, color: '#ef4444', txHash: '0x8a91...bc34', speed: 0.012 },
    { from: '0x7fC7...a3F2', to: '0x8f3d...c9e2', value: '1.20 ETH', txHash: '0x2b10...9e87', speed: 0.009 },
    { from: '0x7fC7...a3F2', to: '0x3c7d...e8f1', value: '0.80 ETH', txHash: '0x93ac...2241', speed: 0.007 },
    { from: '0x7fC7...a3F2', to: '0x6a21...9b4c', value: '1.95 ETH', txHash: '0x17fa...cc09', speed: 0.010 },
    { from: '0x7fC7...a3F2', to: 'Coinbase', value: '2.10 ETH', txHash: '0x66be...aa11', speed: 0.008 },
    { from: '0x7fC7...a3F2', to: '0x91ab...d45e', value: '2.10 ETH', txHash: '0x54e2...88f3', speed: 0.011 },
    { from: '0x91ab...d45e', to: 'Tornado Cash', value: '2.10 ETH', isDashed: true, color: '#10b981', txHash: '0x77fa...dd41', speed: 0.014 }
  ];

  // Particle simulation for active fund flow
  const particlesRef = useRef(
    edges.map((e, idx) => ({
      edgeIndex: idx,
      progress: Math.random(),
      speed: e.speed || 0.008
    }))
  );

  // Interactive Drag & Physics Animation Loop
  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;
    const ctx = canvas.getContext('2d');
    let animationFrameId;

    const render = () => {
      // Handle canvas resize
      const rect = containerRef.current.getBoundingClientRect();
      if (canvas.width !== rect.width || canvas.height !== rect.height) {
        canvas.width = rect.width;
        canvas.height = rect.height;
      }

      ctx.clearRect(0, 0, canvas.width, canvas.height);
      const centerX = canvas.width / 2 + offset.x;
      const centerY = canvas.height / 2 + offset.y;

      ctx.save();
      ctx.translate(centerX, centerY);
      ctx.scale(zoom, zoom);

      // 1. Draw Background Grid Dots
      ctx.fillStyle = 'rgba(59, 130, 246, 0.08)';
      const step = 35;
      for (let gx = -canvas.width; gx < canvas.width; gx += step) {
        for (let gy = -canvas.height; gy < canvas.height; gy += step) {
          ctx.beginPath();
          ctx.arc(gx, gy, 1, 0, Math.PI * 2);
          ctx.fill();
        }
      }

      // 2. Draw Edges
      edges.forEach((edge, idx) => {
        const source = nodes.find(n => n.id === edge.from);
        const target = nodes.find(n => n.id === edge.to);
        if (!source || !target) return;

        ctx.beginPath();
        ctx.moveTo(source.x, source.y);
        ctx.lineTo(target.x, target.y);

        if (edge.isDashed) {
          ctx.setLineDash([5, 4]);
          ctx.strokeStyle = edge.color || 'rgba(239, 68, 68, 0.7)';
          ctx.lineWidth = 2;
        } else {
          ctx.setLineDash([]);
          ctx.strokeStyle = 'rgba(59, 130, 246, 0.35)';
          ctx.lineWidth = 1.5;
        }
        ctx.stroke();
        ctx.setLineDash([]);

        // Draw animated fund flow particle along edge
        const p = particlesRef.current[idx];
        if (p) {
          p.progress += p.speed;
          if (p.progress > 1) p.progress = 0;

          const px = source.x + (target.x - source.x) * p.progress;
          const py = source.y + (target.y - source.y) * p.progress;

          ctx.beginPath();
          ctx.arc(px, py, 3.5, 0, Math.PI * 2);
          ctx.fillStyle = edge.color || '#00d2ff';
          ctx.shadowColor = edge.color || '#00d2ff';
          ctx.shadowBlur = 8;
          ctx.fill();
          ctx.shadowBlur = 0;
        }

        // Draw Edge Value Label at Midpoint on hover
        const midX = (source.x + target.x) / 2;
        const midY = (source.y + target.y) / 2;
        ctx.fillStyle = 'rgba(10, 15, 29, 0.85)';
        ctx.fillRect(midX - 22, midY - 9, 44, 16);
        ctx.strokeStyle = 'rgba(59, 130, 246, 0.3)';
        ctx.strokeRect(midX - 22, midY - 9, 44, 16);
        ctx.fillStyle = '#94a3b8';
        ctx.font = '9px "JetBrains Mono", monospace';
        ctx.textAlign = 'center';
        ctx.textBaseline = 'middle';
        ctx.fillText(edge.value, midX, midY);
      });

      // 3. Draw Nodes
      nodes.forEach((node) => {
        const isHovered = hoveredNode && hoveredNode.id === node.id;
        const isSelected = selectedNodeId === node.id;

        // Halo / Outer Pulse
        if (node.type === 'monitored' || node.haloColor || isHovered || isSelected) {
          ctx.beginPath();
          ctx.arc(node.x, node.y, node.size + (isHovered ? 10 : 7), 0, Math.PI * 2);
          ctx.fillStyle = node.haloColor || 'rgba(0, 210, 255, 0.25)';
          ctx.fill();

          ctx.beginPath();
          ctx.arc(node.x, node.y, node.size + 4, 0, Math.PI * 2);
          ctx.strokeStyle = node.color;
          ctx.lineWidth = 1.5;
          ctx.stroke();
        }

        // Inner Circle
        ctx.beginPath();
        ctx.arc(node.x, node.y, node.size, 0, Math.PI * 2);
        ctx.fillStyle = node.color;
        ctx.shadowColor = node.color;
        ctx.shadowBlur = isHovered ? 16 : 10;
        ctx.fill();
        ctx.shadowBlur = 0;

        // Inner Core icon/dot
        ctx.beginPath();
        ctx.arc(node.x, node.y, node.size * 0.45, 0, Math.PI * 2);
        ctx.fillStyle = '#070b14';
        ctx.fill();

        // Node Label
        ctx.font = '11px "Inter", sans-serif';
        ctx.fillStyle = '#ffffff';
        ctx.textAlign = 'center';
        ctx.textBaseline = 'top';
        ctx.fillText(node.label, node.x, node.y + node.size + 6);

        if (node.sublabel) {
          ctx.font = '10px "Inter", sans-serif';
          ctx.fillStyle = node.type === 'monitored' ? '#38bdf8' : '#94a3b8';
          ctx.fillText(node.sublabel, node.x, node.y + node.size + 20);
        }
      });

      ctx.restore();
      animationFrameId = requestAnimationFrame(render);
    };

    render();
    return () => cancelAnimationFrame(animationFrameId);
  }, [zoom, offset, hoveredNode, selectedNodeId]);

  // Mouse interaction handlers for Pan & Node Drag
  const handleMouseDown = (e) => {
    const rect = canvasRef.current.getBoundingClientRect();
    const clientX = e.clientX - rect.left;
    const clientY = e.clientY - rect.top;
    const centerX = rect.width / 2 + offset.x;
    const centerY = rect.height / 2 + offset.y;

    const graphX = (clientX - centerX) / zoom;
    const graphY = (clientY - centerY) / zoom;

    // Check if clicked a node
    const clickedNode = nodes.find(n => {
      const dist = Math.sqrt((n.x - graphX) ** 2 + (n.y - graphY) ** 2);
      return dist <= n.size + 8;
    });

    if (clickedNode) {
      setDragNode(clickedNode);
      if (onSelectNode) onSelectNode(clickedNode);
    } else {
      setIsDragging(true);
      setMousePos({ x: e.clientX, y: e.clientY });
    }
  };

  const handleMouseMove = (e) => {
    const rect = canvasRef.current?.getBoundingClientRect();
    if (!rect) return;
    const clientX = e.clientX - rect.left;
    const clientY = e.clientY - rect.top;
    const centerX = rect.width / 2 + offset.x;
    const centerY = rect.height / 2 + offset.y;

    const graphX = (clientX - centerX) / zoom;
    const graphY = (clientY - centerY) / zoom;

    // Detect Hover
    const hovered = nodes.find(n => {
      const dist = Math.sqrt((n.x - graphX) ** 2 + (n.y - graphY) ** 2);
      return dist <= n.size + 6;
    });
    setHoveredNode(hovered || null);

    if (dragNode) {
      dragNode.x = graphX;
      dragNode.y = graphY;
    } else if (isDragging) {
      const dx = e.clientX - mousePos.x;
      const dy = e.clientY - mousePos.y;
      setOffset(prev => ({ x: prev.x + dx, y: prev.y + dy }));
      setMousePos({ x: e.clientX, y: e.clientY });
    }
  };

  const handleMouseUp = () => {
    setIsDragging(false);
    setDragNode(null);
  };

  const handleZoom = (delta) => {
    setZoom(prev => Math.min(Math.max(prev + delta, 0.4), 2.5));
  };

  const resetView = () => {
    setZoom(1);
    setOffset({ x: 0, y: 0 });
  };

  return (
    <div className="graph-card">
      {/* Header with View Tabs */}
      <div className="graph-card-header">
        <div className="card-title-group">
          <Network size={17} color="#00d2ff" />
          <span>Transaction Network Graph</span>
        </div>

        <div className="graph-view-tabs">
          <button 
            className={`tab-btn ${viewMode === 'graph' ? 'active' : ''}`}
            onClick={() => setViewMode('graph')}
          >
            Graph View
          </button>
          <button 
            className={`tab-btn ${viewMode === 'timeline' ? 'active' : ''}`}
            onClick={() => setViewMode('timeline')}
          >
            Timeline
          </button>
          <button 
            className={`tab-btn ${viewMode === 'flow' ? 'active' : ''}`}
            onClick={() => setViewMode('flow')}
          >
            Flow
          </button>
        </div>
      </div>

      {/* Main Canvas Viewport or Alternative Views */}
      <div 
        className="graph-canvas-container" 
        ref={containerRef}
        style={{ cursor: dragNode ? 'grabbing' : isDragging ? 'move' : hoveredNode ? 'pointer' : 'default' }}
      >
        {viewMode === 'graph' && (
          <>
            <canvas
              ref={canvasRef}
              onMouseDown={handleMouseDown}
              onMouseMove={handleMouseMove}
              onMouseUp={handleMouseUp}
              onMouseLeave={handleMouseUp}
              style={{ width: '100%', height: '100%', display: 'block' }}
            />

            {/* Floating Navigation Controls */}
            <div className="graph-floating-controls">
              <button 
                className="graph-tool-btn" 
                onClick={() => handleZoom(0.15)}
                title="Zoom In"
              >
                <Plus size={15} />
              </button>
              <button 
                className="graph-tool-btn" 
                onClick={() => handleZoom(-0.15)}
                title="Zoom Out"
              >
                <Minus size={15} />
              </button>
              <button 
                className="graph-tool-btn" 
                onClick={resetView}
                title="Center & Reset View"
              >
                <RotateCcw size={14} />
              </button>
              <button 
                className="graph-tool-btn" 
                onClick={() => {
                  if (containerRef.current.requestFullscreen) {
                    containerRef.current.requestFullscreen();
                  }
                }}
                title="Fullscreen"
              >
                <Maximize2 size={14} />
              </button>
            </div>

            {/* Floating Legend */}
            <div className="graph-floating-legend">
              <div className="legend-item">
                <span className="legend-dot monitored"></span>
                <span>Monitored Wallet</span>
              </div>
              <div className="legend-item">
                <span className="legend-dot connected"></span>
                <span>Connected Wallet</span>
              </div>
              <div className="legend-item">
                <span className="legend-dot exchange"></span>
                <span>Exchange</span>
              </div>
              <div className="legend-item">
                <span className="legend-dot suspicious"></span>
                <span>Suspicious</span>
              </div>
              <div className="legend-item">
                <span className="legend-dot entity"></span>
                <span>Entity</span>
              </div>
              <div className="legend-item">
                <span className="legend-dot tornado"></span>
                <span>Tornado Cash</span>
              </div>
            </div>
          </>
        )}

        {/* Alternate Timeline View */}
        {viewMode === 'timeline' && (
          <div style={{ padding: '2rem', height: '100%', overflowY: 'auto' }}>
            <h4 style={{ color: '#ffffff', marginBottom: '1rem', fontSize: '0.9rem', display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
              <GitCommit size={16} color="#00d2ff" /> Chronological Transaction Trace Stream
            </h4>
            <div style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
              {edges.map((e, i) => (
                <div key={i} style={{
                  display: 'flex',
                  alignItems: 'center',
                  gap: '1rem',
                  padding: '0.75rem 1rem',
                  background: 'rgba(14, 22, 41, 0.7)',
                  borderRadius: '10px',
                  border: '1px solid rgba(59, 130, 246, 0.2)'
                }}>
                  <span className="font-mono" style={{ color: '#38bdf8', fontSize: '0.78rem' }}>{e.from}</span>
                  <ArrowRight size={14} color="#64748b" />
                  <span className="font-mono" style={{ color: e.color || '#f8fafc', fontWeight: '600', fontSize: '0.78rem' }}>{e.to}</span>
                  <span className="font-mono" style={{ marginLeft: 'auto', color: '#10b981', fontWeight: '700' }}>{e.value}</span>
                  <span className="font-mono" style={{ color: '#64748b', fontSize: '0.7rem' }}>Tx: {e.txHash}</span>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* Alternate Flow (Sankey/Waterfall) View */}
        {viewMode === 'flow' && (
          <div style={{ padding: '2rem', height: '100%', overflowY: 'auto' }}>
            <h4 style={{ color: '#ffffff', marginBottom: '1.2rem', fontSize: '0.9rem', display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
              <Layers size={16} color="#00d2ff" /> Multi-Hop Fund Distribution Waterfall
            </h4>
            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(3, 1fr)', gap: '1.5rem' }}>
              {/* Hop 0 */}
              <div style={{ background: 'rgba(14, 22, 41, 0.6)', padding: '1rem', borderRadius: '10px', border: '1px solid rgba(0, 210, 255, 0.3)' }}>
                <div style={{ fontSize: '0.72rem', color: '#38bdf8', fontWeight: '700', marginBottom: '0.6rem' }}>ORIGIN (HOP 0)</div>
                <div style={{ padding: '0.6rem', background: 'rgba(0, 210, 255, 0.1)', borderRadius: '6px', border: '1px solid #00d2ff' }}>
                  <div className="font-mono" style={{ color: '#ffffff', fontWeight: '700', fontSize: '0.8rem' }}>0x7fC7...a3F2</div>
                  <div style={{ fontSize: '0.68rem', color: '#94a3b8' }}>Total Dispersed: 12.10 ETH</div>
                </div>
              </div>

              {/* Hop 1 */}
              <div style={{ background: 'rgba(14, 22, 41, 0.6)', padding: '1rem', borderRadius: '10px', border: '1px solid rgba(59, 130, 246, 0.2)' }}>
                <div style={{ fontSize: '0.72rem', color: '#a855f7', fontWeight: '700', marginBottom: '0.6rem' }}>INTERMEDIARIES (HOP 1)</div>
                <div style={{ display: 'flex', flexDirection: 'column', gap: '0.5rem' }}>
                  <div style={{ padding: '0.4rem', background: 'rgba(255,255,255,0.03)', borderRadius: '4px', fontSize: '0.72rem' }}>
                    0x4e9e...21a7: 0.45 ETH
                  </div>
                  <div style={{ padding: '0.4rem', background: 'rgba(255,255,255,0.03)', borderRadius: '4px', fontSize: '0.72rem' }}>
                    0x8f3d...c9e2: 1.20 ETH
                  </div>
                  <div style={{ padding: '0.4rem', background: 'rgba(255,255,255,0.03)', borderRadius: '4px', fontSize: '0.72rem' }}>
                    0x6a21...9b4c: 1.95 ETH
                  </div>
                  <div style={{ padding: '0.4rem', background: 'rgba(255,255,255,0.03)', borderRadius: '4px', fontSize: '0.72rem' }}>
                    0x91ab...d45e: 2.10 ETH
                  </div>
                </div>
              </div>

              {/* Hop 2 / Terminals */}
              <div style={{ background: 'rgba(14, 22, 41, 0.6)', padding: '1rem', borderRadius: '10px', border: '1px solid rgba(245, 158, 11, 0.3)' }}>
                <div style={{ fontSize: '0.72rem', color: '#fbbf24', fontWeight: '700', marginBottom: '0.6rem' }}>DESTINATIONS / EXCHANGES</div>
                <div style={{ display: 'flex', flexDirection: 'column', gap: '0.5rem' }}>
                  <div style={{ padding: '0.5rem', background: 'rgba(245, 158, 11, 0.12)', border: '1px solid #f59e0b', borderRadius: '6px', fontSize: '0.72rem', color: '#fbbf24', fontWeight: '600' }}>
                    Binance Deposit (3.50 ETH)
                  </div>
                  <div style={{ padding: '0.5rem', background: 'rgba(59, 130, 246, 0.12)', border: '1px solid #3b82f6', borderRadius: '6px', fontSize: '0.72rem', color: '#93c5fd', fontWeight: '600' }}>
                    Coinbase Deposit (2.10 ETH)
                  </div>
                  <div style={{ padding: '0.5rem', background: 'rgba(16, 185, 129, 0.12)', border: '1px solid #10b981', borderRadius: '6px', fontSize: '0.72rem', color: '#6ee7b7', fontWeight: '600' }}>
                    Tornado Cash Pool (2.10 ETH)
                  </div>
                </div>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
