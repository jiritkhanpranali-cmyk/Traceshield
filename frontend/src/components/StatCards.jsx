import React from 'react';
import { 
  ArrowRightLeft, 
  Wallet, 
  Building, 
  AlertTriangle, 
  Clock,
  TrendingUp
} from 'lucide-react';

export default function StatCards({
  totalTx = 247,
  txTrend = '+ 12% (last 24h)',
  connectedWallets = 38,
  walletTrend = '+ 8% (last 24h)',
  potentialExchanges = 7,
  exchangeTrend = '+ 2 new (last 24h)',
  riskLevel = 'Medium',
  lastActivityTime = '14:32',
  lastActivityDate = 'Apr 26, 2025'
}) {
  return (
    <div className="stats-grid">
      {/* 1. Total Transactions */}
      <div className="stat-card">
        <div className="stat-icon-box blue">
          <ArrowRightLeft size={20} />
        </div>
        <div className="stat-content">
          <span className="stat-title">Total Transactions</span>
          <div className="stat-value">{totalTx}</div>
          <div className="stat-trend positive">
            <TrendingUp size={11} />
            <span>{txTrend}</span>
          </div>
        </div>
      </div>

      {/* 2. Connected Wallets */}
      <div className="stat-card">
        <div className="stat-icon-box green">
          <Wallet size={20} />
        </div>
        <div className="stat-content">
          <span className="stat-title">Connected Wallets</span>
          <div className="stat-value">{connectedWallets}</div>
          <div className="stat-trend positive">
            <TrendingUp size={11} />
            <span>{walletTrend}</span>
          </div>
        </div>
      </div>

      {/* 3. Potential Exchanges */}
      <div className="stat-card">
        <div className="stat-icon-box purple">
          <Building size={20} />
        </div>
        <div className="stat-content">
          <span className="stat-title">Potential Exchanges</span>
          <div className="stat-value">{potentialExchanges}</div>
          <div className="stat-trend positive">
            <TrendingUp size={11} />
            <span>{exchangeTrend}</span>
          </div>
        </div>
      </div>

      {/* 4. Risk Level */}
      <div className="stat-card">
        <div className="stat-icon-box amber">
          <AlertTriangle size={20} />
        </div>
        <div className="stat-content">
          <span className="stat-title">Risk Level</span>
          <div className="stat-value" style={{ color: '#fbbf24' }}>
            {riskLevel}
          </div>
          <div className="risk-meter-bar">
            <div 
              className="risk-meter-fill" 
              style={{ 
                width: riskLevel === 'Low' ? '30%' : riskLevel === 'Medium' ? '65%' : '90%',
                background: riskLevel === 'Low' ? '#10b981' : riskLevel === 'Medium' ? 'linear-gradient(90deg, #10b981, #f59e0b)' : 'linear-gradient(90deg, #f59e0b, #ef4444)'
              }}
            ></div>
          </div>
        </div>
      </div>

      {/* 5. Last Activity */}
      <div className="stat-card">
        <div className="stat-icon-box teal">
          <Clock size={20} />
        </div>
        <div className="stat-content">
          <span className="stat-title">Last Activity</span>
          <div className="stat-value font-mono" style={{ fontSize: '1.25rem' }}>
            {lastActivityTime}
          </div>
          <div className="stat-subtext font-mono">
            {lastActivityDate}
          </div>
        </div>
      </div>
    </div>
  );
}
