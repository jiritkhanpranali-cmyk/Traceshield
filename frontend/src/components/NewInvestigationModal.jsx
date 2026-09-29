import React, { useState } from 'react';
import { X, ShieldAlert, Plus, CheckCircle, AlertCircle } from 'lucide-react';

export default function NewInvestigationModal({ isOpen, onClose, onCreateCase }) {
  const [caseNumber, setCaseNumber] = useState(`TS-2026-00${Math.floor(Math.random() * 90 + 10)}`);
  const [wallet, setWallet] = useState('');
  const [network, setNetwork] = useState('Ethereum');
  const [victimRef, setVictimRef] = useState('');
  const [traceDepth, setTraceDepth] = useState('2');
  const [notes, setNotes] = useState('');
  const [validationError, setValidationError] = useState('');

  if (!isOpen) return null;

  const handleSubmit = (e) => {
    e.preventDefault();
    if (!wallet || !wallet.startsWith('0x') || wallet.length < 10) {
      setValidationError('Please enter a valid EVM-compatible wallet address starting with 0x (42 characters).');
      return;
    }
    setValidationError('');
    onCreateCase({
      caseId: caseNumber,
      walletAddress: wallet,
      network,
      victimRef,
      traceDepth,
      notes
    });
    onClose();
  };

  return (
    <div className="modal-backdrop" onClick={onClose}>
      <div className="modal-dialog" style={{ maxWidth: '600px' }} onClick={(e) => e.stopPropagation()}>
        <div className="modal-header">
          <div className="modal-title">
            <Plus size={18} color="#00d2ff" />
            <span>Initiate New Investigation Case</span>
          </div>
          <button className="icon-btn" onClick={onClose} style={{ width: '30px', height: '30px' }}>
            <X size={16} />
          </button>
        </div>

        <form onSubmit={handleSubmit}>
          <div className="modal-body">
            {/* Case Reference ID */}
            <div className="filter-item">
              <label className="filter-label">Case Reference ID</label>
              <input
                type="text"
                className="filter-input font-mono"
                value={caseNumber}
                onChange={(e) => setCaseNumber(e.target.value)}
                required
              />
            </div>

            {/* Victim-Reported Suspect Wallet */}
            <div className="filter-item">
              <label className="filter-label">Victim-Reported Suspect Wallet Address *</label>
              <input
                type="text"
                className="filter-input font-mono"
                placeholder="0x7fC765629da776A1bf0C35B9A42Ef791B7b8a3F2"
                value={wallet}
                onChange={(e) => {
                  setWallet(e.target.value);
                  if (validationError) setValidationError('');
                }}
                required
              />
              {validationError && (
                <div style={{ color: '#ef4444', fontSize: '0.72rem', display: 'flex', alignItems: 'center', gap: '4px', marginTop: '4px' }}>
                  <AlertCircle size={12} /> {validationError}
                </div>
              )}
            </div>

            {/* Blockchain Network & Trace Depth */}
            <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '1rem' }}>
              <div className="filter-item">
                <label className="filter-label">Blockchain Network</label>
                <select className="filter-select" value={network} onChange={(e) => setNetwork(e.target.value)}>
                  <option value="Ethereum">⟠ Ethereum Mainnet</option>
                  <option value="Sepolia">Sepolia Testnet</option>
                  <option value="Polygon">Polygon POS</option>
                  <option value="Arbitrum">Arbitrum One</option>
                  <option value="BSC">BNB Smart Chain</option>
                </select>
              </div>

              <div className="filter-item">
                <label className="filter-label">Initial Trace Depth</label>
                <select className="filter-select" value={traceDepth} onChange={(e) => setTraceDepth(e.target.value)}>
                  <option value="1">1 Hop (Direct Counterparties)</option>
                  <option value="2">2 Hops (Intermediaries)</option>
                  <option value="3">3 Hops (Extended Flow)</option>
                  <option value="5">5 Hops (Deep Trace)</option>
                </select>
              </div>
            </div>

            {/* Victim Complaint Reference */}
            <div className="filter-item">
              <label className="filter-label">Victim Complaint Reference / Portal Ack ID (Optional)</label>
              <input
                type="text"
                className="filter-input"
                placeholder="e.g. NCRP-2026-88192 / Cyber Helpline 1930"
                value={victimRef}
                onChange={(e) => setVictimRef(e.target.value)}
              />
            </div>

            {/* Preliminary Notes */}
            <div className="filter-item">
              <label className="filter-label">Investigation Notes</label>
              <textarea
                className="filter-input"
                rows={3}
                placeholder="Describe suspected fraud typology (e.g. pig butchering scam, fake exchange deposit, phishing)..."
                value={notes}
                onChange={(e) => setNotes(e.target.value)}
                style={{ resize: 'vertical' }}
              />
            </div>
          </div>

          <div className="modal-footer">
            <button type="button" className="btn-secondary" onClick={onClose}>
              Cancel
            </button>
            <button type="submit" className="btn-primary">
              <CheckCircle size={14} />
              <span>Start Live Investigation</span>
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}
