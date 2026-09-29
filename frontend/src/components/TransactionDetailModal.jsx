import React, { useState } from 'react';
import { 
  X, 
  Copy, 
  ExternalLink, 
  CheckCircle2, 
  ShieldCheck, 
  ArrowRight,
  Check,
  Hash,
  Box,
  Coins
} from 'lucide-react';

export default function TransactionDetailModal({
  transaction,
  onClose
}) {
  const [copied, setCopied] = useState(false);

  if (!transaction) return null;

  const handleCopy = () => {
    navigator.clipboard.writeText(transaction.hash || '0x4f828190ba329154c5e39626b9e28e14675e21a7193c7d9910bf28e715ca4081');
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  return (
    <div className="modal-backdrop" onClick={onClose}>
      <div className="modal-dialog" style={{ maxWidth: '580px' }} onClick={(e) => e.stopPropagation()}>
        <div className="modal-header">
          <div className="modal-title">
            <Hash size={18} color="#00d2ff" />
            <span>Transaction Verification Details</span>
          </div>
          <button className="icon-btn" onClick={onClose} style={{ width: '30px', height: '30px' }}>
            <X size={16} />
          </button>
        </div>

        <div className="modal-body">
          {/* Status & Value Banner */}
          <div style={{
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'space-between',
            background: 'rgba(14, 22, 41, 0.8)',
            padding: '1rem',
            borderRadius: '10px',
            border: '1px solid rgba(59, 130, 246, 0.25)'
          }}>
            <div>
              <div style={{ fontSize: '0.68rem', color: '#64748b', textTransform: 'uppercase' }}>Transfer Value</div>
              <div className="font-mono" style={{ fontSize: '1.2rem', fontWeight: '700', color: '#ffffff' }}>
                {transaction.value} <span style={{ fontSize: '0.8rem', color: '#38bdf8' }}>ETH</span>
              </div>
            </div>
            <div className="tx-status-badge" style={{ padding: '0.35rem 0.75rem', fontSize: '0.78rem' }}>
              <CheckCircle2 size={12} />
              <span>{transaction.status || 'Confirmed (12 Block Confirmations)'}</span>
            </div>
          </div>

          {/* Transaction Hash */}
          <div className="filter-item">
            <label className="filter-label">Transaction Hash (TxID)</label>
            <div style={{
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'space-between',
              background: 'rgba(7, 11, 20, 0.8)',
              border: '1px solid rgba(255, 255, 255, 0.08)',
              borderRadius: '6px',
              padding: '0.5rem 0.7rem'
            }}>
              <span className="font-mono" style={{ fontSize: '0.74rem', color: '#38bdf8', overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap', maxWidth: '420px' }}>
                {transaction.hash || '0x4f828190ba329154c5e39626b9e28e14675e21a7193c7d9910bf28e715ca4081'}
              </span>
              <button onClick={handleCopy} style={{ background: 'none', border: 'none', color: copied ? '#10b981' : '#94a3b8', cursor: 'pointer' }}>
                {copied ? <Check size={14} /> : <Copy size={14} />}
              </button>
            </div>
          </div>

          {/* From -> To */}
          <div style={{ display: 'grid', gridTemplateColumns: '1fr auto 1fr', alignItems: 'center', gap: '0.75rem' }}>
            <div className="filter-item">
              <label className="filter-label">Sender (From)</label>
              <div className="font-mono" style={{ background: 'rgba(14, 22, 41, 0.6)', padding: '0.5rem', borderRadius: '6px', fontSize: '0.72rem', color: '#ffffff' }}>
                {transaction.from}
              </div>
            </div>
            <ArrowRight size={16} color="#38bdf8" style={{ marginTop: '14px' }} />
            <div className="filter-item">
              <label className="filter-label">Recipient (To)</label>
              <div className="font-mono" style={{ background: 'rgba(14, 22, 41, 0.6)', padding: '0.5rem', borderRadius: '6px', fontSize: '0.72rem', color: transaction.toIsEntity ? '#fbbf24' : '#38bdf8' }}>
                {transaction.to}
              </div>
            </div>
          </div>

          {/* Gas, Block & Network Specs */}
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(3, 1fr)', gap: '0.6rem' }}>
            <div style={{ background: 'rgba(14, 22, 41, 0.6)', padding: '0.6rem', borderRadius: '8px', border: '1px solid var(--border-subtle)' }}>
              <div style={{ fontSize: '0.65rem', color: '#64748b' }}>Block Number</div>
              <div className="font-mono" style={{ fontSize: '0.78rem', fontWeight: '600', color: '#ffffff' }}>
                #{transaction.blockNumber || '19,602,401'}
              </div>
            </div>
            <div style={{ background: 'rgba(14, 22, 41, 0.6)', padding: '0.6rem', borderRadius: '8px', border: '1px solid var(--border-subtle)' }}>
              <div style={{ fontSize: '0.65rem', color: '#64748b' }}>Network Fee</div>
              <div className="font-mono" style={{ fontSize: '0.78rem', fontWeight: '600', color: '#10b981' }}>
                0.0014 ETH ($4.85)
              </div>
            </div>
            <div style={{ background: 'rgba(14, 22, 41, 0.6)', padding: '0.6rem', borderRadius: '8px', border: '1px solid var(--border-subtle)' }}>
              <div style={{ fontSize: '0.65rem', color: '#64748b' }}>Timestamp</div>
              <div className="font-mono" style={{ fontSize: '0.78rem', fontWeight: '600', color: '#ffffff' }}>
                {transaction.time || '14:32:10 UTC'}
              </div>
            </div>
          </div>
        </div>

        <div className="modal-footer">
          <a
            href={`https://etherscan.io/tx/${transaction.hash || '0x4f828190ba329154c5e39626b9e28e14675e21a7193c7d9910bf28e715ca4081'}`}
            target="_blank"
            rel="noreferrer"
            className="btn-primary"
            style={{ textDecoration: 'none' }}
          >
            <ExternalLink size={13} />
            <span>Open on Etherscan</span>
          </a>
        </div>
      </div>
    </div>
  );
}
