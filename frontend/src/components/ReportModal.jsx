import React, { useState } from 'react';
import { 
  X, 
  Printer, 
  Copy, 
  Download, 
  Check, 
  ShieldAlert, 
  FileCheck, 
  Building2, 
  Activity,
  Layers,
  Scale,
  Sparkles
} from 'lucide-react';

export default function ReportModal({
  isOpen,
  onClose,
  caseId = 'TS-2026-0047',
  walletAddress = '0x7fC765629da776A1bf0C35B9A42Ef791B7b8a3F2',
  network = 'Ethereum Mainnet',
  totalTx = 247,
  riskLevel = 'Medium',
  connectedWallets = 38,
  potentialExchanges = 7
}) {
  const [copied, setCopied] = useState(false);

  if (!isOpen) return null;

  const handlePrint = () => {
    window.print();
  };

  const handleCopyMarkdown = () => {
    const reportText = `
# TRACESHIELD AI — CYBER INVESTIGATION INTELLIGENCE REPORT
**Problem Statement:** Real-Time Identification of Fraud-Linked Cryptocurrency Exchanges from Victim-Reported Suspect Wallet Addresses through Automated Blockchain Analytics
**Case Reference ID:** ${caseId}
**Date of Report:** ${new Date().toLocaleDateString()} ${new Date().toLocaleTimeString()}
**Target Suspect Wallet:** \`${walletAddress}\`
**Network:** ${network}
**Investigation Status:** Active Live Monitoring
**Assessed Risk Level:** ${riskLevel}

---

## 1. INVESTIGATION SUMMARY
TraceShield AI performed automated multi-hop blockchain analytics beginning from the victim-reported suspect wallet address \`${walletAddress}\`. Historical and continuous live blockchain tracking retrieved ${totalTx} transactions across ${connectedWallets} connected counterparties.

## 2. POTENTIAL EXCHANGE & ENTITY ATTRIBUTIONS
- **Binance Exchange Cluster:** Potentially associated deposit address \`0x28C6...1d60\` received 3.50 ETH via direct transfer.
- **Coinbase Exchange Cluster:** Potentially associated deposit address \`0xA090...057e\` received 2.10 ETH.
- **High-Risk Mixer Interaction:** Intermediary wallet \`0x91ab...d45e\` subsequently routed 2.10 ETH into Tornado Cash contract (\`0xd90e...F31b\`).

## 3. MULTI-HOP FUND FLOW BREAKDOWN
1. **Hop 0 (Suspect Origin):** 12.10 ETH dispersed to 5 intermediary wallets within a 4-hour window.
2. **Hop 1 (Intermediary Layer):** Rapid peeling and fund fragmentation observed across addresses \`0x4e9e...21a7\`, \`0x8f3d...c9e2\`, and \`0x6a21...9b4c\`.
3. **Hop 2 (Terminal Endpoints):** Consolidation into centralized exchange deposit addresses and sanctioned privacy mixer pool.

## 4. REGULATORY & INVESTIGATION DISCLAIMER
*This document constitutes an AI-assisted investigation intelligence summary generated for law enforcement review under the Ministry of Home Affairs (MHA) framework. Public blockchain indicators do not automatically prove criminal intent or ownership; formal attribution requires statutory legal process and exchange verification.*
    `;
    navigator.clipboard.writeText(reportText.trim());
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  return (
    <div className="modal-backdrop" onClick={onClose}>
      <div className="modal-dialog" onClick={(e) => e.stopPropagation()}>
        {/* Modal Header */}
        <div className="modal-header">
          <div className="modal-title">
            <Sparkles size={18} color="#00d2ff" />
            <span>AI Investigation Report — Case {caseId}</span>
          </div>
          <button 
            className="icon-btn" 
            onClick={onClose}
            style={{ width: '30px', height: '30px' }}
          >
            <X size={16} />
          </button>
        </div>

        {/* Modal Body */}
        <div className="modal-body">
          {/* Top Metadata Banner */}
          <div style={{
            display: 'grid',
            gridTemplateColumns: 'repeat(4, 1fr)',
            gap: '0.75rem',
            background: 'rgba(14, 22, 41, 0.8)',
            padding: '1rem',
            borderRadius: '10px',
            border: '1px solid rgba(59, 130, 246, 0.25)'
          }}>
            <div>
              <div style={{ fontSize: '0.68rem', color: '#64748b', textTransform: 'uppercase' }}>Case Reference</div>
              <div className="font-mono" style={{ fontSize: '0.85rem', fontWeight: '700', color: '#38bdf8' }}>{caseId}</div>
            </div>
            <div>
              <div style={{ fontSize: '0.68rem', color: '#64748b', textTransform: 'uppercase' }}>Network</div>
              <div style={{ fontSize: '0.85rem', fontWeight: '600', color: '#ffffff' }}>{network}</div>
            </div>
            <div>
              <div style={{ fontSize: '0.68rem', color: '#64748b', textTransform: 'uppercase' }}>Risk Level</div>
              <div style={{ fontSize: '0.85rem', fontWeight: '700', color: '#fbbf24' }}>{riskLevel} Risk</div>
            </div>
            <div>
              <div style={{ fontSize: '0.68rem', color: '#64748b', textTransform: 'uppercase' }}>Counterparties</div>
              <div style={{ fontSize: '0.85rem', fontWeight: '600', color: '#ffffff' }}>{connectedWallets} Wallets</div>
            </div>
          </div>

          {/* Suspect Target Address */}
          <div className="report-section">
            <div className="report-section-title">Investigated Suspect Address</div>
            <div className="font-mono" style={{ background: 'rgba(7, 11, 20, 0.8)', padding: '0.6rem 0.8rem', borderRadius: '6px', border: '1px solid rgba(59, 130, 246, 0.2)', color: '#00d2ff', fontSize: '0.82rem', wordBreak: 'break-all' }}>
              {walletAddress}
            </div>
          </div>

          {/* Key Findings Section */}
          <div className="report-section">
            <div className="report-section-title">Analytical Findings & Exchange Intelligence</div>
            <ul style={{ display: 'flex', flexDirection: 'column', gap: '0.55rem', paddingLeft: '1.2rem', color: '#94a3b8', fontSize: '0.78rem' }}>
              <li>
                <strong style={{ color: '#ffffff' }}>Direct Exchange Liquidation Path:</strong> 3.50 ETH transferred to a deposit cluster potentially associated with <strong style={{ color: '#fbbf24' }}>Binance</strong> (TX: 0x8a91...bc34).
              </li>
              <li>
                <strong style={{ color: '#ffffff' }}>Secondary Exchange Endpoint:</strong> 2.10 ETH transferred to a cluster potentially associated with <strong style={{ color: '#38bdf8' }}>Coinbase Prime</strong>.
              </li>
              <li>
                <strong style={{ color: '#ffffff' }}>Obfuscation & Mixer Layer:</strong> Intermediary wallet <code className="font-mono" style={{ color: '#38bdf8' }}>0x91ab...d45e</code> channeled 2.10 ETH into Tornado Cash mixing contract.
              </li>
              <li>
                <strong style={{ color: '#ffffff' }}>Velocity Analysis:</strong> 82% of suspect wallet outflows occurred within 4 hours of victim fund receipt.
              </li>
            </ul>
          </div>

          {/* Fund Flow Path Table */}
          <div className="report-section">
            <div className="report-section-title">Multi-Hop Fund Trace Matrix</div>
            <table style={{ width: '100%', borderCollapse: 'collapse', fontSize: '0.72rem' }}>
              <thead>
                <tr style={{ color: '#64748b', textAlign: 'left', borderBottom: '1px solid rgba(255,255,255,0.06)' }}>
                  <th style={{ padding: '0.4rem' }}>Hop</th>
                  <th style={{ padding: '0.4rem' }}>Source Address</th>
                  <th style={{ padding: '0.4rem' }}>Destination</th>
                  <th style={{ padding: '0.4rem' }}>Amount</th>
                  <th style={{ padding: '0.4rem' }}>Classification</th>
                </tr>
              </thead>
              <tbody style={{ color: '#cbd5e1' }}>
                <tr style={{ borderBottom: '1px solid rgba(255,255,255,0.03)' }}>
                  <td className="font-mono" style={{ padding: '0.4rem', color: '#00d2ff' }}>Hop 0</td>
                  <td className="font-mono" style={{ padding: '0.4rem' }}>0x7fC7...a3F2</td>
                  <td className="font-mono" style={{ padding: '0.4rem', color: '#fbbf24' }}>Binance</td>
                  <td className="font-mono" style={{ padding: '0.4rem', color: '#10b981' }}>3.50 ETH</td>
                  <td style={{ padding: '0.4rem' }}>Potential Exchange Exposure</td>
                </tr>
                <tr style={{ borderBottom: '1px solid rgba(255,255,255,0.03)' }}>
                  <td className="font-mono" style={{ padding: '0.4rem', color: '#a855f7' }}>Hop 1</td>
                  <td className="font-mono" style={{ padding: '0.4rem' }}>0x7fC7...a3F2</td>
                  <td className="font-mono" style={{ padding: '0.4rem' }}>0x91ab...d45e</td>
                  <td className="font-mono" style={{ padding: '0.4rem', color: '#10b981' }}>2.10 ETH</td>
                  <td style={{ padding: '0.4rem' }}>Intermediary Peeling</td>
                </tr>
                <tr>
                  <td className="font-mono" style={{ padding: '0.4rem', color: '#ef4444' }}>Hop 2</td>
                  <td className="font-mono" style={{ padding: '0.4rem' }}>0x91ab...d45e</td>
                  <td className="font-mono" style={{ padding: '0.4rem', color: '#10b981' }}>Tornado Cash</td>
                  <td className="font-mono" style={{ padding: '0.4rem', color: '#10b981' }}>2.10 ETH</td>
                  <td style={{ padding: '0.4rem', color: '#ef4444' }}>Mixer Obfuscation</td>
                </tr>
              </tbody>
            </table>
          </div>

          {/* Legal / MHA / FATF Compliance Notice */}
          <div style={{
            background: 'rgba(37, 99, 235, 0.08)',
            border: '1px solid rgba(37, 99, 235, 0.25)',
            borderRadius: '8px',
            padding: '0.85rem',
            display: 'flex',
            alignItems: 'flex-start',
            gap: '0.65rem'
          }}>
            <Scale size={18} color="#38bdf8" style={{ flexShrink: 0, marginTop: '2px' }} />
            <div style={{ fontSize: '0.71rem', color: '#94a3b8', lineHeight: '1.4' }}>
              <strong style={{ color: '#ffffff' }}>Human-in-the-Loop Investigation Notice:</strong> TraceShield AI generates investigative indicators and evidence-oriented correlation from public blockchain transactions. Blockchain data alone does not establish criminal intent or confirm identity ownership. Legal subpoena to identified exchange compliance units is recommended for KYC attribution.
            </div>
          </div>
        </div>

        {/* Modal Footer Actions */}
        <div className="modal-footer">
          <button 
            className="btn-secondary" 
            onClick={handleCopyMarkdown}
          >
            {copied ? <Check size={13} color="#10b981" /> : <Copy size={13} />}
            <span>{copied ? 'Copied Markdown' : 'Copy Markdown'}</span>
          </button>
          <button 
            className="btn-primary" 
            onClick={handlePrint}
          >
            <Printer size={13} />
            <span>Print / Export PDF</span>
          </button>
        </div>
      </div>
    </div>
  );
}
