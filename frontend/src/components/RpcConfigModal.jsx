import React, { useState } from 'react';
import { 
  X, 
  Radio, 
  CheckCircle, 
  AlertCircle, 
  RefreshCw, 
  Server, 
  Cpu, 
  Activity,
  Zap
} from 'lucide-react';

export default function RpcConfigModal({
  isOpen,
  onClose,
  currentRpcUrl = 'https://cloudflare-eth.com',
  onUpdateRpc,
  onBlockHeightFetched
}) {
  const [rpcUrl, setRpcUrl] = useState(currentRpcUrl);
  const [testing, setTesting] = useState(false);
  const [testResult, setTestResult] = useState(null);

  if (!isOpen) return null;

  const testConnection = async () => {
    setTesting(true);
    setTestResult(null);
    const startTime = performance.now();

    try {
      const response = await fetch(rpcUrl, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          jsonrpc: '2.0',
          method: 'eth_blockNumber',
          params: [],
          id: 1
        })
      });

      const data = await response.json();
      const endTime = performance.now();
      const latency = Math.round(endTime - startTime);

      if (data && data.result) {
        const blockHeight = parseInt(data.result, 16);
        setTestResult({
          success: true,
          blockHeight,
          latency,
          message: `Successfully connected to Ethereum Node. Current Block Height: #${blockHeight.toLocaleString()} (${latency}ms)`
        });
        if (onBlockHeightFetched) onBlockHeightFetched(blockHeight);
      } else {
        throw new Error(data.error?.message || 'Invalid RPC response');
      }
    } catch (err) {
      setTestResult({
        success: false,
        message: `Connection failed: ${err.message}. Using high-fidelity local cache checkpoint.`
      });
    } finally {
      setTesting(false);
    }
  };

  const handleSave = () => {
    if (onUpdateRpc) onUpdateRpc(rpcUrl);
    onClose();
  };

  return (
    <div className="modal-backdrop" onClick={onClose}>
      <div className="modal-dialog" style={{ maxWidth: '580px' }} onClick={(e) => e.stopPropagation()}>
        <div className="modal-header">
          <div className="modal-title">
            <Server size={18} color="#00d2ff" />
            <span>Ethereum Blockchain RPC Configuration</span>
          </div>
          <button className="icon-btn" onClick={onClose} style={{ width: '30px', height: '30px' }}>
            <X size={16} />
          </button>
        </div>

        <div className="modal-body">
          <div style={{ fontSize: '0.78rem', color: '#94a3b8' }}>
            TraceShield AI communicates directly with live Ethereum JSON-RPC nodes to fetch realtime blocks, transactions, and verify counterparty states.
          </div>

          <div className="filter-item">
            <label className="filter-label">Active Ethereum RPC Endpoint (HTTP/HTTPS)</label>
            <input
              type="text"
              className="filter-input font-mono"
              value={rpcUrl}
              onChange={(e) => setRpcUrl(e.target.value)}
              placeholder="https://cloudflare-eth.com or https://mainnet.infura.io/v3/..."
            />
          </div>

          {/* Quick preset endpoints */}
          <div style={{ display: 'flex', gap: '0.5rem', flexWrap: 'wrap' }}>
            <button 
              type="button" 
              className="btn-secondary" 
              style={{ fontSize: '0.7rem', padding: '0.3rem 0.6rem' }}
              onClick={() => setRpcUrl('https://cloudflare-eth.com')}
            >
              Cloudflare Public RPC
            </button>
            <button 
              type="button" 
              className="btn-secondary" 
              style={{ fontSize: '0.7rem', padding: '0.3rem 0.6rem' }}
              onClick={() => setRpcUrl('https://eth.llamarpc.com')}
            >
              LlamaRPC Mainnet
            </button>
            <button 
              type="button" 
              className="btn-secondary" 
              style={{ fontSize: '0.7rem', padding: '0.3rem 0.6rem' }}
              onClick={() => setRpcUrl('https://rpc.ankr.com/eth')}
            >
              Ankr Public Node
            </button>
          </div>

          {/* Test Status Box */}
          {testResult && (
            <div style={{
              background: testResult.success ? 'rgba(16, 185, 129, 0.1)' : 'rgba(239, 68, 68, 0.1)',
              border: `1px solid ${testResult.success ? 'rgba(16, 185, 129, 0.3)' : 'rgba(239, 68, 68, 0.3)'}`,
              borderRadius: '8px',
              padding: '0.75rem',
              display: 'flex',
              alignItems: 'flex-start',
              gap: '0.5rem'
            }}>
              {testResult.success ? (
                <CheckCircle size={16} color="#10b981" style={{ flexShrink: 0, marginTop: '2px' }} />
              ) : (
                <AlertCircle size={16} color="#ef4444" style={{ flexShrink: 0, marginTop: '2px' }} />
              )}
              <div style={{ fontSize: '0.74rem', color: testResult.success ? '#34d399' : '#f87171' }}>
                {testResult.message}
              </div>
            </div>
          )}
        </div>

        <div className="modal-footer">
          <button 
            type="button" 
            className="btn-secondary" 
            onClick={testConnection}
            disabled={testing}
          >
            <RefreshCw size={13} className={testing ? 'spin' : ''} />
            <span>{testing ? 'Pinging Node...' : 'Test Live Connection'}</span>
          </button>
          <button 
            type="button" 
            className="btn-primary" 
            onClick={handleSave}
          >
            <CheckCircle size={13} />
            <span>Save & Apply RPC</span>
          </button>
        </div>
      </div>
    </div>
  );
}
