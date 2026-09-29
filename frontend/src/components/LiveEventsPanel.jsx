import React, { useState } from 'react';
import { 
  ArrowRight, 
  Share2, 
  Building2, 
  Box, 
  ShieldAlert, 
  ExternalLink,
  Pause,
  Play,
  Filter
} from 'lucide-react';

export default function LiveEventsPanel({ 
  events, 
  isLive, 
  onToggleLive, 
  onSelectEvent,
  onViewAll 
}) {
  const [filterType, setFilterType] = useState('all');

  const getIcon = (type, color) => {
    switch (type) {
      case 'tx':
        return <ArrowRight size={15} />;
      case 'interaction':
        return <Share2 size={15} />;
      case 'exchange':
        return <Building2 size={15} />;
      case 'block':
        return <Box size={15} />;
      case 'risk':
        return <ShieldAlert size={15} />;
      default:
        return <ArrowRight size={15} />;
    }
  };

  const filteredEvents = events.filter(e => {
    if (filterType === 'all') return true;
    return e.type === filterType;
  });

  return (
    <div className="live-events-card">
      {/* Header */}
      <div className="live-events-header">
        <div className="live-title-badge">
          <span style={{ fontFamily: 'var(--font-display)', fontWeight: 700, fontSize: '0.92rem', color: '#ffffff' }}>
            Live Events
          </span>
          <span className="live-badge-mini">
            Live
          </span>
        </div>

        <div style={{ display: 'flex', alignItems: 'center', gap: '0.6rem' }}>
          <button 
            onClick={onToggleLive}
            style={{ 
              background: 'none', 
              border: 'none', 
              color: isLive ? '#10b981' : '#64748b', 
              cursor: 'pointer',
              display: 'flex',
              alignItems: 'center',
              gap: '0.2rem',
              fontSize: '0.68rem',
              fontWeight: '600'
            }}
            title={isLive ? "Pause Live Event Stream" : "Resume Live Stream"}
          >
            {isLive ? <Pause size={12} /> : <Play size={12} />}
            <span>{isLive ? 'STREAMING' : 'PAUSED'}</span>
          </button>

          <span 
            className="view-all-link"
            onClick={onViewAll}
          >
            View All →
          </span>
        </div>
      </div>

      {/* Events List */}
      <div className="events-list">
        {filteredEvents.map((evt) => (
          <div 
            key={evt.id} 
            className={`event-item ${evt.isNew ? 'highlight-new' : ''}`}
            onClick={() => onSelectEvent && onSelectEvent(evt)}
            style={{ cursor: 'pointer' }}
          >
            <div className={`event-icon-circle ${evt.color}`}>
              {getIcon(evt.type, evt.color)}
            </div>

            <div className="event-body">
              <div className="event-top-row">
                <span className="event-title">{evt.title}</span>
                <span className="event-time">{evt.time}</span>
              </div>

              {evt.fromTo && (
                <div className="event-desc">
                  {evt.fromTo}
                </div>
              )}

              {evt.detail && (
                <div style={{ fontSize: '0.7rem', color: '#94a3b8' }}>
                  {evt.detail}
                </div>
              )}

              {evt.amount && (
                <div className="event-meta">
                  {evt.amount}
                </div>
              )}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
