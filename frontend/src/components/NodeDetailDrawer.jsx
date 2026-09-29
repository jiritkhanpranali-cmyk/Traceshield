import React from 'react';
import { 
  X, 
  Copy, 
  ExternalLink, 
  ShieldAlert, 
  Activity, 
  Check, 
  ArrowUpRight, 
  Building2,
  TrendingUp,
  Radio
} from 'lucide-react';

export default function NodeDetailDrawer({
  node,
  onClose,
  onSetAsRoot
}) {
  const [copied, setCopied] = React.useState(false);

  if (!node) return null;

  const handleCopy = () => {
    navigator.clipboard.writeText(node.fullAddress || node.id);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  return (
    <div style={{
      position: 'absolute',
      top: '55px',
      right: '15px',
      width: '340px',
      maxHeight: 'calc(100% - 70px)',
      background: 'rgba(10, 15, 29, 0.94)',
      backdropFilter: 'blur(16px)',
      border: '1px solid rgba(59, 130, 246, 0.35)',
      borderRadius: '14px',
      boxShadow: '0 15px 35px rgba(0,0,0,0.8), 0 0 20px rgba(0, 210, 255, 0.15)',
      zIndex: 20,
      padding: '1.2rem',
      display: 'flex',
      flexDirection: 'column',
      gap: '0.9rem',
      overflowY: 'auto'
    }}>
      {/* Top Header */}
      <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', borderBottom: '1px solid rgba(255,255,255,0.08)', paddingBottom: '0.6rem' }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
          <span style={{
            width: '10px',
            height: '10px',
            borderRadius: '50%',
            background: node.color || '#00d2ff',
            boxShadow: `0 0 8px ${node.color || '#00d2ff'}`
          }}></span>
          <span style={{ fontFamily: 'var(--font-display)', fontWeight: 700, fontSize: '0.92rem', color: '#ffffff' }}>
            {node.label}
          </span>
        </div>
        <button 
          onClick={onClose}
          style={{ background: 'none', border: 'none', color: '#94a3b8', cursor: 'pointer' }}
        >
          <X size={16} />
        </button>
      </div>

      {/* Category Tag */}
      <div style={{
        background: 'rgba(59, 130, 246, 0.12)',
        border: '1px solid rgba(59, 130, 246, 0.25)',
        borderRadius: '6px',
        padding: '0.35rem 0.6rem',
        fontSize: '0.72rem',
        color: '#38bdf8',
        fontWeight: '600'
      }}>
        {node.category || 'Blockchain Counterparty'}
      </div>

      {/* Full Address with Copy */}
      <div>
        <div style={{ fontSize: '0.68rem', color: '#64748b', textTransform: 'uppercase', marginBottom: '0.25rem' }}>
          Full Wallet Address
        </div>
        <div style={{
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'space-between',
          background: 'rgba(7, 11, 20, 0.8)',
          border: '1px solid rgba(255, 255, 255, 0.08)',
          borderRadius: '6px',
          padding: '0.45rem 0.6rem'
        }}>
          <span className="font-mono" style={{ fontSize: '0.7rem', color: '#f8fafc', overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap', maxWidth: '240px' }}>
            {node.fullAddress || node.id}
          </span>
          <button 
            onClick={handleCopy}
            style={{ background: 'none', border: 'none', color: copied ? '#10b981' : '#94a3b8', cursor: 'pointer' }}
            title="Copy Full Address"
          >
            {copied ? <Check size={13} /> : <Copy size={13} />}
          </button>
        </div>
      </div>

      {/* Stats Grid */}
      <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '0.6rem' }}>
        <div style={{ background: 'rgba(14, 22, 41, 0.7)', padding: '0.55rem', borderRadius: '8px', border: '1px solid rgba(255,255,255,0.05)' }}>
          <div style={{ fontSize: '0.65rem', color: '#64748b' }}>Current Balance</div>
          <div className="font-mono" style={{ fontSize: '0.82rem', fontWeight: '700', color: '#10b981' }}>{node.balance || '0.00 ETH'}</div>
        </div>
        <div style={{ background: 'rgba(14, 22, 41, 0.7)', padding: '0.55rem', borderRadius: '8px', border: '1px solid rgba(255,255,255,0.05)' }}>
          <div style={{ fontSize: '0.65rem', color: '#64748b' }}>Total Tx Volume</div>
          <div className="font-mono" style={{ fontSize: '0.82rem', fontWeight: '700', color: '#ffffff' }}>{node.volume || '0.00 ETH'}</div>
        </div>
        <div style={{ background: 'rgba(14, 22, 41, 0.7)', padding: '0.55rem', borderRadius: '8px', border: '1px solid rgba(255,255,255,0.05)' }}>
          <div style={{ fontSize: '0.65rem', color: '#64748b' }}>Hop Distance</div>
          <div className="font-mono" style={{ fontSize: '0.82rem', fontWeight: '700', color: '#38bdf8' }}>Hop #{node.hop ?? 1}</div>
        </div>
        <div style={{ background: 'rgba(14, 22, 41, 0.7)', padding: '0.55rem', borderRadius: '8px', border: '1px solid rgba(255,255,255,0.05)' }}>
          <div style={{ fontSize: '0.65rem', color: '#64748b' }}>Interactions</div>
          <div className="font-mono" style={{ fontSize: '0.82rem', fontWeight: '700', color: '#c084fc' }}>{node.txCount || 1} TXs</div>
        </div>
      </div>

      {/* Assessed Risk Indicators */}
      <div style={{ background: 'rgba(245, 158, 11, 0.08)', border: '1px solid rgba(245, 158, 11, 0.25)', borderRadius: '8px', padding: '0.65rem' }}>
        <div style={{ fontSize: '0.68rem', color: '#fbbf24', fontWeight: '700', display: 'flex', alignItems: 'center', gap: '4px' }}>
          <ShieldAlert size={13} /> Assessed Risk Indicator
        </div>
        <div style={{ fontSize: '0.74rem', color: '#f8fafc', fontWeight: '600', marginTop: '0.2rem' }}>
          {node.riskScore || 'Standard Counterparty'}
        </div>
      </div>

      {/* Action Buttons */}
      <div style={{ display: 'flex', flexDirection: 'column', gap: '0.5rem', marginTop: '0.2rem' }}>
        <button 
          className="btn-primary"
          style={{ width: '100%', fontSize: '0.74rem', minHeight: '32px' }}
          onClick={() => {
            if (onSetAsRoot) onSetAsRoot(node.fullAddress || node.id);
            onClose();
          }}
        >
          <Radio size={13} />
          <span>Set as Active Monitored Wallet</span>
        </button>

        <a 
          href={`https://etherscan.io/address/${node.fullAddress || node.id}`}
          target="_blank"
          rel="noreferrer"
          className="btn-secondary"
          style={{ width: '100%', fontSize: '0.74rem', minHeight: '32px', textDecoration: 'none', textAlign: 'center' }}
        >
          <ExternalLink size={13} style={{ marginRight: '4px' }} />
          <span>View on Etherscan</span>
        </a>
      </div>
    </div>
  );
}
