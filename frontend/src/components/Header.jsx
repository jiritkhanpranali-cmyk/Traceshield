import React, { useState } from 'react';
import { 
  Shield, 
  Search, 
  Bell, 
  ChevronDown, 
  ExternalLink,
  CheckCircle2,
  AlertTriangle,
  Cpu,
  X
} from 'lucide-react';

export default function Header({ 
  searchQuery, 
  setSearchQuery, 
  onSearch, 
  onOpenReport,
  onOpenNewCase,
  activeNetwork 
}) {
  const [showNotifications, setShowNotifications] = useState(false);
  const [showProfileMenu, setShowProfileMenu] = useState(false);

  const notifications = [
    {
      id: 1,
      title: 'High-Volume Exchange Transfer',
      desc: '3.5 ETH moved to Binance-linked deposit address',
      time: '14:24',
      unread: true,
      type: 'warning'
    },
    {
      id: 2,
      title: 'New Block Confirmed',
      desc: 'Block #19,602,401 processed by live listener',
      time: '14:18',
      unread: false,
      type: 'info'
    },
    {
      id: 3,
      title: 'Multi-Hop Pattern Detected',
      desc: 'Fund movement across 3 intermediate hops flagged for review',
      time: '14:12',
      unread: false,
      type: 'alert'
    }
  ];

  return (
    <header className="top-header">
      {/* Brand / Logo */}
      <div className="header-left">
        <div className="brand-logo-wrapper">
          <Shield size={20} strokeWidth={2.2} />
        </div>
        <div className="brand-text">
          <div className="brand-title">
            TraceShield <span className="highlight">AI</span>
          </div>
          <div className="brand-subtitle">
            Blockchain Investigation & Analytics Platform
          </div>
        </div>
      </div>

      {/* Global Investigation Search */}
      <div className="header-search">
        <form onSubmit={(e) => { e.preventDefault(); onSearch(searchQuery); }} className="search-input-wrapper">
          <Search size={15} className="search-icon" />
          <input
            type="text"
            className="search-input font-mono"
            placeholder="Search wallet address, transaction hash, block number, or case ID..."
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
          />
          {searchQuery && (
            <button 
              type="button" 
              onClick={() => setSearchQuery('')}
              style={{ background: 'none', border: 'none', color: '#64748b', cursor: 'pointer', marginRight: '6px' }}
            >
              <X size={13} />
            </button>
          )}
          <span className="search-shortcut">⌘K</span>
        </form>
      </div>

      {/* Header Actions & Profile */}
      <div className="header-right">
        {/* Notifications */}
        <div style={{ position: 'relative' }}>
          <button 
            className="icon-btn" 
            onClick={() => setShowNotifications(!showNotifications)}
            title="Investigation Alerts"
          >
            <Bell size={17} />
            <span className="notification-badge"></span>
          </button>

          {showNotifications && (
            <div style={{
              position: 'absolute',
              top: '46px',
              right: '0',
              width: '320px',
              background: '#0a0f1d',
              border: '1px solid rgba(59, 130, 246, 0.3)',
              borderRadius: '12px',
              boxShadow: '0 12px 30px rgba(0,0,0,0.7)',
              zIndex: 100,
              padding: '0.75rem',
              backdropFilter: 'blur(16px)'
            }}>
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '0.6rem', borderBottom: '1px solid rgba(255,255,255,0.06)', paddingBottom: '0.4rem' }}>
                <span style={{ fontSize: '0.78rem', fontWeight: '700', color: '#ffffff' }}>Investigation Alerts</span>
                <span style={{ fontSize: '0.68rem', color: '#38bdf8', cursor: 'pointer' }}>Mark all read</span>
              </div>
              <div style={{ display: 'flex', flexDirection: 'column', gap: '0.5rem' }}>
                {notifications.map(n => (
                  <div key={n.id} style={{
                    padding: '0.5rem 0.6rem',
                    borderRadius: '8px',
                    background: n.unread ? 'rgba(37, 99, 235, 0.12)' : 'rgba(255,255,255,0.02)',
                    borderLeft: n.type === 'warning' ? '3px solid #f59e0b' : '3px solid #3b82f6',
                    cursor: 'pointer'
                  }}>
                    <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '0.72rem', fontWeight: '600', color: '#f8fafc' }}>
                      <span>{n.title}</span>
                      <span style={{ color: '#64748b', fontSize: '0.65rem' }}>{n.time}</span>
                    </div>
                    <div style={{ fontSize: '0.68rem', color: '#94a3b8', marginTop: '0.15rem' }}>
                      {n.desc}
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>

        {/* Investigator Profile */}
        <div style={{ position: 'relative' }}>
          <div 
            className="user-profile-badge"
            onClick={() => setShowProfileMenu(!showProfileMenu)}
          >
            <div className="avatar-circle">JD</div>
            <div className="user-info">
              <span className="user-name">ADMIN NAME</span>
              <span className="user-role">Investigator</span>
            </div>
            <ChevronDown size={14} color="#64748b" />
          </div>

          {showProfileMenu && (
            <div style={{
              position: 'absolute',
              top: '46px',
              right: '0',
              width: '210px',
              background: '#0a0f1d',
              border: '1px solid rgba(59, 130, 246, 0.3)',
              borderRadius: '10px',
              boxShadow: '0 12px 30px rgba(0,0,0,0.7)',
              zIndex: 100,
              padding: '0.5rem',
              display: 'flex',
              flexDirection: 'column',
              gap: '0.2rem'
            }}>
              <div style={{ padding: '0.4rem 0.6rem', borderBottom: '1px solid rgba(255,255,255,0.06)', fontSize: '0.7rem', color: '#94a3b8' }}>
                Agency: <strong style={{ color: '#f8fafc' }}>Cyber Crime Unit</strong>
              </div>
              <button 
                onClick={() => { setShowProfileMenu(false); onOpenNewCase(); }}
                style={{ textAlign: 'left', background: 'none', border: 'none', padding: '0.45rem 0.6rem', color: '#38bdf8', fontSize: '0.75rem', cursor: 'pointer', borderRadius: '6px' }}
              >
                + New Case Reference
              </button>
              <button 
                onClick={() => { setShowProfileMenu(false); onOpenReport(); }}
                style={{ textAlign: 'left', background: 'none', border: 'none', padding: '0.45rem 0.6rem', color: '#f8fafc', fontSize: '0.75rem', cursor: 'pointer', borderRadius: '6px' }}
              >
                Generate Summary Report
              </button>
            </div>
          )}
        </div>
      </div>
    </header>
  );
}
