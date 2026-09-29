import React from 'react';
import { Clock, Plus, Check } from 'lucide-react';

export default function InvestigationTimeline({ 
  timelineSteps, 
  onAddNote,
  onViewAll 
}) {
  return (
    <div className="panel-card">
      <div className="panel-header">
        <div className="panel-title">
          <Clock size={15} color="#38bdf8" />
          <span>Investigation Timeline</span>
        </div>
        <span 
          className="view-all-link"
          onClick={onViewAll}
        >
          View All →
        </span>
      </div>

      <div className="timeline-body">
        {timelineSteps.map((step) => (
          <div key={step.id} className="timeline-step">
            <div className={`timeline-dot ${step.color}`}></div>
            <div className="timeline-content">
              <span className="timeline-title">{step.title}</span>
              <span className="timeline-time font-mono">{step.time}</span>
              {step.note && (
                <span style={{ fontSize: '0.68rem', color: '#94a3b8', marginTop: '0.1rem' }}>
                  {step.note}
                </span>
              )}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
