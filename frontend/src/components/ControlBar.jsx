import React from 'react';
import { Search, Play, RotateCcw, Copy, Check } from 'lucide-react';

export default function ControlBar({
  network,
  setNetwork,
  walletAddress,
  setWalletAddress,
  timeRange,
  setTimeRange,
  traceDepth,
  setTraceDepth,
  riskFilter,
  setRiskFilter,
  onApply,
  onReset,
  isLoading
}) {
  const [copied, setCopied] = React.useState(false);

  const handleCopy = () => {
    if (walletAddress) {
      navigator.clipboard.writeText(walletAddress);
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    }
  };

  return (
    <div className="control-bar-card">
      <div className="filter-fields-group">
        {/* Network Selector */}
        <div className="filter-item">
          <label className="filter-label">Network</label>
          <select 
            className="filter-select"
            value={network}
            onChange={(e) => setNetwork(e.target.value)}
          >
            <option value="Ethereum">⟠ Ethereum Mainnet</option>
            <option value="Sepolia">Sepolia Testnet</option>
            <option value="Arbitrum">Arbitrum One</option>
            <option value="Polygon">Polygon POS</option>
            <option value="BSC">BNB Smart Chain</option>
          </select>
        </div>

        {/* Wallet Address Input */}
        <div className="filter-item" style={{ flex: '1 1 280px' }}>
          <label className="filter-label">Wallet Address</label>
          <div className="filter-input-wallet-wrapper">
            <input
              type="text"
              className="filter-input filter-input-wallet"
              placeholder="Enter suspect wallet address (0x...)"
              value={walletAddress}
              onChange={(e) => setWalletAddress(e.target.value)}
            />
            <button 
              type="button" 
              onClick={handleCopy}
              className="input-suffix-icon"
              style={{ background: 'none', border: 'none' }}
              title="Copy Address"
            >
              {copied ? <Check size={14} color="#10b981" /> : <Copy size={14} />}
            </button>
          </div>
        </div>

        {/* Time Range */}
        <div className="filter-item">
          <label className="filter-label">Time Range</label>
          <select 
            className="filter-select"
            value={timeRange}
            onChange={(e) => setTimeRange(e.target.value)}
          >
            <option value="1h">Last 1 Hour</option>
            <option value="24h">Last 24 Hours</option>
            <option value="7d">Last 7 Days</option>
            <option value="30d">Last 30 Days</option>
            <option value="all">All Time</option>
          </select>
        </div>

        {/* Trace Depth */}
        <div className="filter-item">
          <label className="filter-label">Trace Depth</label>
          <select 
            className="filter-select"
            value={traceDepth}
            onChange={(e) => setTraceDepth(e.target.value)}
          >
            <option value="1">1 Hop (Direct Counterparties)</option>
            <option value="2">2 Hops (Intermediaries)</option>
            <option value="3">3 Hops (Extended Flow)</option>
            <option value="5">5 Hops (Deep Trace)</option>
          </select>
        </div>

        {/* Risk Level */}
        <div className="filter-item">
          <label className="filter-label">Risk Level</label>
          <select 
            className="filter-select"
            value={riskFilter}
            onChange={(e) => setRiskFilter(e.target.value)}
          >
            <option value="All">All Risk Levels</option>
            <option value="Low">Low Risk Only</option>
            <option value="Medium">Medium Risk</option>
            <option value="High">High Risk</option>
            <option value="Critical">Critical Risk</option>
          </select>
        </div>
      </div>

      {/* Action Buttons */}
      <div className="control-actions-group">
        <button 
          className="btn-primary" 
          onClick={onApply}
          disabled={isLoading}
        >
          {isLoading ? (
            <span>Analyzing...</span>
          ) : (
            <>
              <Play size={13} fill="currentColor" />
              <span>Apply</span>
            </>
          )}
        </button>

        <button 
          className="btn-secondary" 
          onClick={onReset}
          title="Reset parameters to initial state"
        >
          <RotateCcw size={13} style={{ marginRight: '4px' }} />
          <span>Reset</span>
        </button>
      </div>
    </div>
  );
}
