import React, { useState } from 'react';
import { 
  Sparkles, 
  AlertTriangle, 
  ChevronUp, 
  ChevronDown, 
  FileText,
  ShieldCheck,
  Zap
} from 'lucide-react';

export default function QuickInsights({
  onGenerateReport,
  exchangeExposure = "The monitored wallet has interacted with a Binance-linked address within the last 24 hours.",
  keyRisks = [
    "Multi-hop fund flow detected",
    "Exchange-linked address identified",
    "Unusual transaction pattern"
  ]
}) {
  const [isRisksExpanded, setIsRisksExpanded] = useState(true);

  return (
    <div className="panel-card">
      <div className="panel-header">
        <div className="panel-title">
          <Sparkles size={15} color="#38bdf8" />
          <span>Quick Insights</span>
        </div>
        <button 
          className="btn-primary" 
          onClick={onGenerateReport}
          style={{ padding: '0.3rem 0.75rem', fontSize: '0.74rem', minHeight: '30px' }}
        >
          <FileText size={12} />
          <span>Generate Report</span>
        </button>
      </div>

      <div className="insights-body">
        {/* Potential Exchange Exposure Box */}
        <div className="exposure-alert-box">
          <div className="exposure-title">
            <AlertTriangle size={15} color="#fbbf24" />
            <span>Potential Exchange Exposure</span>
          </div>
          <p className="exposure-text">
            {exchangeExposure}
          </p>
        </div>

        {/* Key Risks Section */}
        <div className="key-risks-group">
          <div 
            className="key-risks-header"
            onClick={() => setIsRisksExpanded(!isRisksExpanded)}
            style={{ cursor: 'pointer' }}
          >
            <span>Key Risks</span>
            {isRisksExpanded ? <ChevronUp size={14} /> : <ChevronDown size={14} />}
          </div>

          {isRisksExpanded && (
            <div style={{ display: 'flex', flexDirection: 'column', gap: '0.4rem', marginTop: '0.2rem' }}>
              {keyRisks.map((risk, idx) => (
                <div key={idx} className="risk-bullet-item">
                  <span className="risk-bullet-dot"></span>
                  <span>{risk}</span>
                </div>
              ))}
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
