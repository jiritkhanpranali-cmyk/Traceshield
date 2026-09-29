import React from 'react';
import { 
  LayoutDashboard, 
  FolderArchive, 
  PlusCircle, 
  Activity, 
  Share2, 
  GitFork, 
  ShieldAlert, 
  Building2, 
  FileText, 
  Users, 
  Database, 
  Terminal, 
  Settings,
  Radio
} from 'lucide-react';

export default function Sidebar({ 
  currentTab, 
  setCurrentTab, 
  onOpenNewCase, 
  onOpenReport,
  isLiveMonitoring,
  toggleLiveMonitoring,
  onOpenRpcConfig,
  currentBlockNumber = 19602401,
  activeNetwork = 'Ethereum'
}) {
  return (
    <aside className="left-sidebar">
      <div className="sidebar-nav-group">
        {/* Top Actions */}
        <button 
          className={`nav-link-item ${currentTab === 'dashboard' ? 'active' : ''}`}
          onClick={() => setCurrentTab('dashboard')}
        >
          <LayoutDashboard size={16} />
          <span>Dashboard</span>
        </button>

        <button 
          className={`nav-link-item ${currentTab === 'investigations' ? 'active' : ''}`}
          onClick={() => setCurrentTab('investigations')}
        >
          <FolderArchive size={16} />
          <span>My Investigations</span>
        </button>

        <button 
          className="nav-link-item new-case-btn"
          onClick={onOpenNewCase}
        >
          <PlusCircle size={16} />
          <span>New Investigation</span>
        </button>

        {/* INVESTIGATION TOOLS */}
        <div className="sidebar-section-title">Investigation Tools</div>

        <button 
          className={`nav-link-item ${currentTab === 'live_monitoring' ? 'active' : ''}`}
          onClick={() => {
            setCurrentTab('dashboard');
            toggleLiveMonitoring();
          }}
        >
          <Activity size={16} />
          <span>Live Monitoring</span>
          <span className="live-dot" style={{ opacity: isLiveMonitoring ? 1 : 0.2 }}></span>
        </button>

        <button 
          className={`nav-link-item ${currentTab === 'graph' ? 'active' : ''}`}
          onClick={() => setCurrentTab('graph')}
        >
          <Share2 size={16} />
          <span>Transaction Graph</span>
        </button>

        <button 
          className={`nav-link-item ${currentTab === 'fund_flow' ? 'active' : ''}`}
          onClick={() => setCurrentTab('fund_flow')}
        >
          <GitFork size={16} />
          <span>Fund Flow Analysis</span>
        </button>

        <button 
          className={`nav-link-item ${currentTab === 'risk' ? 'active' : ''}`}
          onClick={() => setCurrentTab('risk')}
        >
          <ShieldAlert size={16} />
          <span>Risk & Pattern Analysis</span>
        </button>

        <button 
          className={`nav-link-item ${currentTab === 'entities' ? 'active' : ''}`}
          onClick={() => setCurrentTab('entities')}
        >
          <Building2 size={16} />
          <span>Entity Intelligence</span>
        </button>

        <button 
          className={`nav-link-item ${currentTab === 'reports' ? 'active' : ''}`}
          onClick={() => onOpenReport()}
        >
          <FileText size={16} />
          <span>Reports</span>
        </button>

        {/* ADMIN (EXPERT ONLY) */}
        <div className="sidebar-section-title">Admin (Expert Only)</div>

        <button 
          className={`nav-link-item ${currentTab === 'users' ? 'active' : ''}`}
          onClick={() => setCurrentTab('users')}
        >
          <Users size={16} />
          <span>Users & Access</span>
        </button>

        <button 
          className={`nav-link-item ${currentTab === 'intelligence' ? 'active' : ''}`}
          onClick={() => setCurrentTab('intelligence')}
        >
          <Database size={16} />
          <span>Intelligence Management</span>
        </button>

        <button 
          className={`nav-link-item ${currentTab === 'logs' ? 'active' : ''}`}
          onClick={() => setCurrentTab('logs')}
        >
          <Terminal size={16} />
          <span>System Logs</span>
        </button>

        <button 
          className={`nav-link-item ${currentTab === 'settings' ? 'active' : ''}`}
          onClick={() => onOpenRpcConfig ? onOpenRpcConfig() : setCurrentTab('settings')}
        >
          <Settings size={16} />
          <span>Settings</span>
        </button>
      </div>

      {/* Sidebar Footer with Live Connection Status */}
      <div className="sidebar-footer">
        <div 
          className="network-status-card"
          onClick={onOpenRpcConfig}
          style={{ cursor: 'pointer' }}
          title="Click to view or edit Ethereum RPC Endpoint"
        >
          <div className="network-pulse-dot"></div>
          <div className="network-status-text">
            <span className="network-name">{activeNetwork}</span>
            <span className="network-state">Connected (Block #{currentBlockNumber.toLocaleString()})</span>
          </div>
        </div>

        <div className="sidebar-copyright">
          TraceShield AI © 2026
        </div>
      </div>
    </aside>
  );
}
