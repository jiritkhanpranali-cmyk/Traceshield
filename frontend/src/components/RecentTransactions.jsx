import React from 'react';
import { CheckCircle2, ArrowRight, ExternalLink } from 'lucide-react';

export default function RecentTransactions({
  transactions,
  onSelectTransaction,
  onViewAll
}) {
  return (
    <div className="panel-card">
      <div className="panel-header">
        <div className="panel-title">
          <span style={{ color: '#38bdf8' }}>⇄</span>
          <span>Recent Transactions</span>
        </div>
        <span 
          className="view-all-link"
          onClick={onViewAll}
        >
          View All →
        </span>
      </div>

      <div className="tx-table-wrapper">
        <table className="tx-table">
          <thead>
            <tr>
              <th>Time</th>
              <th>From → To</th>
              <th>Value</th>
              <th>Network</th>
              <th>Status</th>
            </tr>
          </thead>
          <tbody>
            {transactions.map((tx) => (
              <tr 
                key={tx.id}
                onClick={() => onSelectTransaction && onSelectTransaction(tx)}
                style={{ cursor: 'pointer' }}
              >
                <td className="font-mono" style={{ color: '#94a3b8' }}>{tx.time}</td>
                <td className="font-mono">
                  <span style={{ color: '#ffffff' }}>{tx.from}</span>
                  <span style={{ color: '#64748b', margin: '0 4px' }}>→</span>
                  <span style={{ color: tx.toIsEntity ? '#fbbf24' : '#38bdf8', fontWeight: tx.toIsEntity ? '600' : 'normal' }}>
                    {tx.to}
                  </span>
                </td>
                <td className="font-mono" style={{ color: '#f8fafc', fontWeight: '600' }}>
                  {tx.value}
                </td>
                <td>
                  <span style={{ display: 'inline-flex', alignItems: 'center', gap: '3px', color: '#94a3b8', fontSize: '0.72rem' }}>
                    <span style={{ color: '#38bdf8' }}>⟠</span> {tx.network}
                  </span>
                </td>
                <td>
                  <span className="tx-status-badge">
                    <CheckCircle2 size={10} />
                    <span>{tx.status}</span>
                  </span>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
