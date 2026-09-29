import React, { useState, useEffect } from 'react';
import Header from './components/Header';
import Sidebar from './components/Sidebar';
import ControlBar from './components/ControlBar';
import StatCards from './components/StatCards';
import TransactionNetworkGraph from './components/TransactionNetworkGraph';
import LiveEventsPanel from './components/LiveEventsPanel';
import RecentTransactions from './components/RecentTransactions';
import InvestigationTimeline from './components/InvestigationTimeline';
import QuickInsights from './components/QuickInsights';
import ReportModal from './components/ReportModal';
import NewInvestigationModal from './components/NewInvestigationModal';
import NodeDetailDrawer from './components/NodeDetailDrawer';
import TransactionDetailModal from './components/TransactionDetailModal';
import RpcConfigModal from './components/RpcConfigModal';
import { 
  FolderArchive, 
  Share2, 
  GitFork, 
  ShieldAlert, 
  Building2, 
  FileText, 
  Users, 
  Database, 
  Terminal, 
  Settings,
  Sparkles,
  Search,
  CheckCircle2,
  ExternalLink,
  Shield,
  Layers
} from 'lucide-react';

export default function App() {
  // Navigation State
  const [currentTab, setCurrentTab] = useState('dashboard');
  const [graphViewMode, setGraphViewMode] = useState('graph');

  // Investigation Parameters
  const [caseId, setCaseId] = useState('TS-2026-0047');
  const [walletAddress, setWalletAddress] = useState('0x7fC765629da776A1bf0C35B9A42Ef791B7b8a3F2');
  const [network, setNetwork] = useState('Ethereum');
  const [timeRange, setTimeRange] = useState('24h');
  const [traceDepth, setTraceDepth] = useState('2');
  const [riskFilter, setRiskFilter] = useState('All');
  const [searchQuery, setSearchQuery] = useState('');
  const [isLoading, setIsLoading] = useState(false);

  // Live Blockchain & Monitoring State
  const [isLiveMonitoring, setIsLiveMonitoring] = useState(true);
  const [currentBlockNumber, setCurrentBlockNumber] = useState(19602401);
  const [lastActivityTime, setLastActivityTime] = useState('14:32');
  const [lastActivityDate, setLastActivityDate] = useState('Apr 26, 2025');

  // Selected Items for Drawers/Modals
  const [selectedNode, setSelectedNode] = useState(null);
  const [selectedTransaction, setSelectedTransaction] = useState(null);
  const [isReportModalOpen, setIsReportModalOpen] = useState(false);
  const [isNewCaseModalOpen, setIsNewCaseModalOpen] = useState(false);
  const [isRpcModalOpen, setIsRpcModalOpen] = useState(false);

  // Initial Events Stream matching screenshot
  const [events, setEvents] = useState([
    {
      id: 1,
      type: 'tx',
      title: 'New transaction detected',
      time: '14:32',
      fromTo: '0x7fC7...a3F2 → 0x4e9e...21a7',
      amount: '0.45 ETH',
      color: 'green'
    },
    {
      id: 2,
      type: 'interaction',
      title: 'Wallet interaction',
      time: '14:28',
      fromTo: '0x8f3d...c9e2 → 0x2b1...776a',
      amount: '1.2 ETH',
      color: 'blue'
    },
    {
      id: 3,
      type: 'exchange',
      title: 'Exchange link detected',
      time: '14:24',
      detail: 'Address linked to Binance (potentially associated)',
      color: 'amber'
    },
    {
      id: 4,
      type: 'block',
      title: 'New block mined',
      time: '14:18',
      detail: 'Block #19,602,401',
      color: 'teal'
    },
    {
      id: 5,
      type: 'risk',
      title: 'Risk indicator updated',
      time: '14:12',
      detail: 'Multi-hop pattern detected',
      color: 'red'
    }
  ]);

  // Recent Transactions Table matching screenshot
  const [transactions, setTransactions] = useState([
    {
      id: 1,
      time: '14:32',
      from: '0x7fC7...a3F2',
      to: '0x4e9e...21a7',
      toIsEntity: false,
      value: '0.45 ETH',
      network: 'Ethereum',
      status: 'Confirmed',
      blockNumber: '19,602,401',
      hash: '0x4f828190ba329154c5e39626b9e28e14675e21a7193c7d9910bf28e715ca4081'
    },
    {
      id: 2,
      time: '14:28',
      from: '0x8f3d...c9e2',
      to: '0x2b1...776a',
      toIsEntity: false,
      value: '1.2 ETH',
      network: 'Ethereum',
      status: 'Confirmed',
      blockNumber: '19,602,398',
      hash: '0x2b109e8790ba329154c5e39626b9e28e14675e21a7193c7d9910bf28e715ca40'
    },
    {
      id: 3,
      time: '14:24',
      from: '0x6a21...9b4c',
      to: 'Binance',
      toIsEntity: true,
      value: '3.5 ETH',
      network: 'Ethereum',
      status: 'Confirmed',
      blockNumber: '19,602,394',
      hash: '0x8a91bc34ba329154c5e39626b9e28e14675e21a7193c7d9910bf28e715ca4081'
    },
    {
      id: 4,
      time: '14:17',
      from: '0x3c7d...e8f1',
      to: '0x91ab...d45e',
      toIsEntity: false,
      value: '0.8 ETH',
      network: 'Ethereum',
      status: 'Confirmed',
      blockNumber: '19,602,390',
      hash: '0x93ac2241ba329154c5e39626b9e28e14675e21a7193c7d9910bf28e715ca4081'
    },
    {
      id: 5,
      time: '14:12',
      from: '0x91ab...d45e',
      to: 'Tornado Cash',
      toIsEntity: true,
      value: '2.1 ETH',
      network: 'Ethereum',
      status: 'Confirmed',
      blockNumber: '19,602,385',
      hash: '0x77fadd41ba329154c5e39626b9e28e14675e21a7193c7d9910bf28e715ca4081'
    }
  ]);

  // Timeline Steps matching screenshot
  const [timelineSteps, setTimelineSteps] = useState([
    {
      id: 1,
      title: 'Case Created',
      time: 'Apr 26, 12:15 PM',
      color: 'blue',
      note: 'Victim complaint received via National Cyber Crime Reporting Portal'
    },
    {
      id: 2,
      title: 'Initial Analysis',
      time: 'Apr 26, 12:29 PM',
      color: 'purple',
      note: 'Retrieved 84 historical blocks; 1st hop counterparties mapped'
    },
    {
      id: 3,
      title: 'Live Monitoring Started',
      time: 'Apr 26, 12:45 PM',
      color: 'green',
      note: 'Checkpoint at block #19,602,300 with active listener'
    },
    {
      id: 4,
      title: 'Latest Event',
      time: 'Apr 26, 14:32 PM',
      color: 'gold',
      note: '0.45 ETH transfer to 0x4e9e...21a7 detected'
    }
  ]);

  // Live Blockchain Block Heartbeat (Simulates real continuous block stream)
  useEffect(() => {
    if (!isLiveMonitoring) return;

    const interval = setInterval(() => {
      setCurrentBlockNumber(prev => {
        const nextBlock = prev + 1;
        const now = new Date();
        const timeStr = `${String(now.getHours()).padStart(2, '0')}:${String(now.getMinutes()).padStart(2, '0')}`;
        
        // Randomly add a live block or micro-transaction
        if (Math.random() > 0.45) {
          const newEvt = {
            id: Date.now(),
            type: 'block',
            title: 'New block mined',
            time: timeStr,
            detail: `Block #${nextBlock.toLocaleString()}`,
            color: 'teal',
            isNew: true
          };
          setEvents(prevEvents => [newEvt, ...prevEvents.slice(0, 7)]);
        }
        return nextBlock;
      });
    }, 14000); // Ethereum ~12s block time

    return () => clearInterval(interval);
  }, [isLiveMonitoring]);

  // Apply Filter Action
  const handleApplyFilter = () => {
    setIsLoading(true);
    setTimeout(() => {
      setIsLoading(false);
      const now = new Date();
      setLastActivityTime(`${String(now.getHours()).padStart(2, '0')}:${String(now.getMinutes()).padStart(2, '0')}`);
    }, 600);
  };

  // Reset Filter Action
  const handleResetFilter = () => {
    setWalletAddress('0x7fC765629da776A1bf0C35B9A42Ef791B7b8a3F2');
    setNetwork('Ethereum');
    setTimeRange('24h');
    setTraceDepth('2');
    setRiskFilter('All');
  };

  // Create New Case Handler
  const handleCreateNewCase = (caseData) => {
    setCaseId(caseData.caseId);
    setWalletAddress(caseData.walletAddress);
    setNetwork(caseData.network);
    setTraceDepth(caseData.traceDepth);
    setTimelineSteps([
      {
        id: 1,
        title: 'Case Created',
        time: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
        color: 'blue',
        note: `New investigation ${caseData.caseId} initialized`
      },
      {
        id: 2,
        title: 'Live Monitoring Started',
        time: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
        color: 'green',
        note: `Monitoring wallet ${caseData.walletAddress.substring(0, 8)}...`
      }
    ]);
  };

  return (
    <div className="app-container">
      {/* Top Sticky Header */}
      <Header
        searchQuery={searchQuery}
        setSearchQuery={setSearchQuery}
        onSearch={(q) => {
          if (q.startsWith('0x')) {
            setWalletAddress(q);
          }
        }}
        onOpenReport={() => setIsReportModalOpen(true)}
        onOpenNewCase={() => setIsNewCaseModalOpen(true)}
        activeNetwork={network}
      />

      {/* Main Layout Area */}
      <div className="main-layout">
        {/* Left Navigation Sidebar */}
        <Sidebar
          currentTab={currentTab}
          setCurrentTab={setCurrentTab}
          onOpenNewCase={() => setIsNewCaseModalOpen(true)}
          onOpenReport={() => setIsReportModalOpen(true)}
          isLiveMonitoring={isLiveMonitoring}
          toggleLiveMonitoring={() => setIsLiveMonitoring(!isLiveMonitoring)}
          onOpenRpcConfig={() => setIsRpcModalOpen(true)}
          currentBlockNumber={currentBlockNumber}
          activeNetwork={network}
        />

        {/* Workspace Main Area */}
        <main className="main-content">
          {/* Main Dashboard View */}
          {currentTab === 'dashboard' && (
            <>
              {/* Dashboard Page Title Row */}
              <div className="dashboard-title-row">
                <div className="title-badge-wrapper">
                  <div>
                    <h1 className="page-title">
                      <span style={{ color: '#00d2ff', fontSize: '1.2rem' }}>❖</span>
                      <span>Investigation Dashboard</span>
                    </h1>
                    <p className="page-subtitle">
                      Track, analyze and investigate cryptocurrency activity in real-time
                    </p>
                  </div>
                </div>

                <div className="case-id-badges">
                  <div className="case-pill">
                    <span>Case ID: {caseId}</span>
                  </div>
                  <div className="live-indicator-pill">
                    <span className="pulse-dot"></span>
                    <span>Live Monitoring</span>
                  </div>
                </div>
              </div>

              {/* Filter & Control Bar */}
              <ControlBar
                network={network}
                setNetwork={setNetwork}
                walletAddress={walletAddress}
                setWalletAddress={setWalletAddress}
                timeRange={timeRange}
                setTimeRange={setTimeRange}
                traceDepth={traceDepth}
                setTraceDepth={setTraceDepth}
                riskFilter={riskFilter}
                setRiskFilter={setRiskFilter}
                onApply={handleApplyFilter}
                onReset={handleResetFilter}
                isLoading={isLoading}
              />

              {/* 5 Stat Summary Cards */}
              <StatCards
                totalTx={247}
                connectedWallets={38}
                potentialExchanges={7}
                riskLevel="Medium"
                lastActivityTime={lastActivityTime}
                lastActivityDate={lastActivityDate}
              />

              {/* Middle Row: Transaction Network Graph & Live Events */}
              <div className="middle-grid">
                <TransactionNetworkGraph
                  onSelectNode={(node) => setSelectedNode(node)}
                  selectedNodeId={selectedNode?.id}
                  viewMode={graphViewMode}
                  setViewMode={setGraphViewMode}
                />

                <LiveEventsPanel
                  events={events}
                  isLive={isLiveMonitoring}
                  onToggleLive={() => setIsLiveMonitoring(!isLiveMonitoring)}
                  onSelectEvent={(evt) => {
                    // Quick inspect
                  }}
                  onViewAll={() => setCurrentTab('logs')}
                />
              </div>

              {/* Bottom Row: Recent Transactions, Investigation Timeline, Quick Insights */}
              <div className="bottom-grid">
                <RecentTransactions
                  transactions={transactions}
                  onSelectTransaction={(tx) => setSelectedTransaction(tx)}
                  onViewAll={() => setGraphViewMode('timeline')}
                />

                <InvestigationTimeline
                  timelineSteps={timelineSteps}
                  onAddNote={() => {}}
                  onViewAll={() => {}}
                />

                <QuickInsights
                  onGenerateReport={() => setIsReportModalOpen(true)}
                  exchangeExposure="The monitored wallet has interacted with a Binance-linked address within the last 24 hours."
                  keyRisks={[
                    "Multi-hop fund flow detected",
                    "Exchange-linked address identified",
                    "Unusual transaction pattern"
                  ]}
                />
              </div>
            </>
          )}

          {/* Alternate Sub-Pages for Sidebar Sections */}
          {currentTab === 'investigations' && (
            <div className="panel-card" style={{ padding: '2rem' }}>
              <h2 style={{ color: '#ffffff', display: 'flex', alignItems: 'center', gap: '0.6rem', fontSize: '1.2rem', marginBottom: '1.2rem' }}>
                <FolderArchive size={20} color="#00d2ff" />
                <span>My Active Investigations & Cases</span>
              </h2>
              <div style={{ display: 'flex', flexDirection: 'column', gap: '0.75rem' }}>
                <div style={{ padding: '1rem', background: 'rgba(14, 22, 41, 0.8)', border: '1px solid rgba(59, 130, 246, 0.3)', borderRadius: '10px', display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                  <div>
                    <div style={{ color: '#38bdf8', fontWeight: '700', fontSize: '0.85rem' }}>Case ID: TS-2026-0047</div>
                    <div className="font-mono" style={{ color: '#ffffff', fontSize: '0.78rem' }}>Target: 0x7fC765629da776A1bf0C35B9A42Ef791B7b8a3F2</div>
                    <div style={{ color: '#94a3b8', fontSize: '0.72rem' }}>Network: Ethereum • Risk: Medium • Active Live Listener</div>
                  </div>
                  <button className="btn-primary" onClick={() => setCurrentTab('dashboard')}>Resume Case</button>
                </div>
              </div>
            </div>
          )}

          {currentTab === 'graph' && (
            <div style={{ minHeight: '650px', display: 'flex', flexDirection: 'column', gap: '1rem' }}>
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                <h2 style={{ color: '#ffffff', fontSize: '1.2rem', display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                  <Share2 size={20} color="#00d2ff" /> Dedicated Transaction Graph Explorer
                </h2>
                <button className="btn-primary" onClick={() => setIsReportModalOpen(true)}>Generate Case Report</button>
              </div>
              <TransactionNetworkGraph
                onSelectNode={(node) => setSelectedNode(node)}
                selectedNodeId={selectedNode?.id}
                viewMode={graphViewMode}
                setViewMode={setGraphViewMode}
              />
            </div>
          )}

          {currentTab === 'fund_flow' && (
            <div style={{ minHeight: '650px', display: 'flex', flexDirection: 'column', gap: '1rem' }}>
              <h2 style={{ color: '#ffffff', fontSize: '1.2rem', display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                <GitFork size={20} color="#00d2ff" /> Multi-Hop Fund Flow & Peel Chain Tracing
              </h2>
              <TransactionNetworkGraph
                onSelectNode={(node) => setSelectedNode(node)}
                selectedNodeId={selectedNode?.id}
                viewMode="flow"
                setViewMode={setGraphViewMode}
              />
            </div>
          )}

          {currentTab === 'risk' && (
            <div className="panel-card" style={{ padding: '2rem' }}>
              <h2 style={{ color: '#ffffff', display: 'flex', alignItems: 'center', gap: '0.6rem', fontSize: '1.2rem', marginBottom: '1.2rem' }}>
                <ShieldAlert size={20} color="#f59e0b" />
                <span>Risk & Behavioral Pattern Matrix</span>
              </h2>
              <div style={{ display: 'grid', gridTemplateColumns: 'repeat(3, 1fr)', gap: '1rem' }}>
                <div style={{ background: 'rgba(239, 68, 68, 0.1)', border: '1px solid rgba(239, 68, 68, 0.3)', padding: '1rem', borderRadius: '10px' }}>
                  <div style={{ color: '#ef4444', fontWeight: '700', fontSize: '0.85rem' }}>Sanctioned Mixer Exposure</div>
                  <div style={{ color: '#94a3b8', fontSize: '0.74rem', marginTop: '0.4rem' }}>2.10 ETH routed to Tornado Cash contract via intermediary 0x91ab...d45e</div>
                </div>
                <div style={{ background: 'rgba(245, 158, 11, 0.1)', border: '1px solid rgba(245, 158, 11, 0.3)', padding: '1rem', borderRadius: '10px' }}>
                  <div style={{ color: '#fbbf24', fontWeight: '700', fontSize: '0.85rem' }}>Exchange Deposit Link</div>
                  <div style={{ color: '#94a3b8', fontSize: '0.74rem', marginTop: '0.4rem' }}>3.50 ETH transferred to Binance-attributed deposit cluster</div>
                </div>
                <div style={{ background: 'rgba(59, 130, 246, 0.1)', border: '1px solid rgba(59, 130, 246, 0.3)', padding: '1rem', borderRadius: '10px' }}>
                  <div style={{ color: '#38bdf8', fontWeight: '700', fontSize: '0.85rem' }}>High-Velocity Peeling</div>
                  <div style={{ color: '#94a3b8', fontSize: '0.74rem', marginTop: '0.4rem' }}>5 rapid outbound transfers completed within 4 hours of wallet activation</div>
                </div>
              </div>
            </div>
          )}

          {currentTab === 'entities' && (
            <div className="panel-card" style={{ padding: '2rem' }}>
              <h2 style={{ color: '#ffffff', display: 'flex', alignItems: 'center', gap: '0.6rem', fontSize: '1.2rem', marginBottom: '1.2rem' }}>
                <Building2 size={20} color="#00d2ff" />
                <span>Identified Entity & Exchange Intelligence Database</span>
              </h2>
              <div style={{ display: 'grid', gridTemplateColumns: 'repeat(2, 1fr)', gap: '1rem' }}>
                <div style={{ padding: '1rem', background: 'rgba(14, 22, 41, 0.8)', borderRadius: '10px', border: '1px solid rgba(245, 158, 11, 0.3)' }}>
                  <div style={{ color: '#fbbf24', fontWeight: '700', fontSize: '0.9rem' }}>Binance Centralized Exchange</div>
                  <div className="font-mono" style={{ color: '#94a3b8', fontSize: '0.74rem', marginTop: '0.3rem' }}>Known Cluster: 0x28C6c06298d514Db089934071355E5743bf21d60</div>
                  <div style={{ color: '#10b981', fontSize: '0.72rem', marginTop: '0.3rem' }}>Attribution Confidence: 99.4% (Verified Hot/Deposit Cluster)</div>
                </div>
                <div style={{ padding: '1rem', background: 'rgba(14, 22, 41, 0.8)', borderRadius: '10px', border: '1px solid rgba(59, 130, 246, 0.3)' }}>
                  <div style={{ color: '#38bdf8', fontWeight: '700', fontSize: '0.9rem' }}>Coinbase Prime Custody</div>
                  <div className="font-mono" style={{ color: '#94a3b8', fontSize: '0.74rem', marginTop: '0.3rem' }}>Known Cluster: 0xA090e606E30bD747d4E6245a1517EbE430F0057e</div>
                  <div style={{ color: '#10b981', fontSize: '0.72rem', marginTop: '0.3rem' }}>Attribution Confidence: 99.1% (Verified Institutional Cluster)</div>
                </div>
              </div>
            </div>
          )}

          {currentTab === 'logs' && (
            <div className="panel-card" style={{ padding: '2rem' }}>
              <h2 style={{ color: '#ffffff', display: 'flex', alignItems: 'center', gap: '0.6rem', fontSize: '1.2rem', marginBottom: '1.2rem' }}>
                <Terminal size={20} color="#00d2ff" />
                <span>Live Blockchain Listener Event Logs</span>
              </h2>
              <div style={{ background: '#070b14', padding: '1rem', borderRadius: '8px', border: '1px solid rgba(255,255,255,0.08)', fontFamily: 'var(--font-mono)', fontSize: '0.74rem', color: '#34d399', maxHeight: '400px', overflowY: 'auto' }}>
                <div>[2026-09-28 14:32:10] [ETH_WS_LISTENER] Incoming transfer detected: 0x7fC7...a3F2 → 0x4e9e...21a7 (0.45 ETH) Block #19602401</div>
                <div>[2026-09-28 14:28:44] [CHECKPOINT_ENGINE] Saved state at block #19602398 (0 missed blocks)</div>
                <div>[2026-09-28 14:24:19] [ENTITY_RESOLVER] Address 0x28C6...1d60 attributed to Binance Cluster (tag: exchange_deposit)</div>
                <div>[2026-09-28 14:18:02] [RPC_CLIENT] Ping Cloudflare Ethereum Node: latency=42ms, status=HEALTHY</div>
              </div>
            </div>
          )}
        </main>
      </div>

      {/* Slide-over Node Detail Drawer */}
      <NodeDetailDrawer
        node={selectedNode}
        onClose={() => setSelectedNode(null)}
        onSetAsRoot={(newAddr) => {
          setWalletAddress(newAddr);
          handleApplyFilter();
        }}
      />

      {/* Transaction Inspection Modal */}
      <TransactionDetailModal
        transaction={selectedTransaction}
        onClose={() => setSelectedTransaction(null)}
      />

      {/* AI Investigation Report Modal */}
      <ReportModal
        isOpen={isReportModalOpen}
        onClose={() => setIsReportModalOpen(false)}
        caseId={caseId}
        walletAddress={walletAddress}
        network={network}
        totalTx={247}
        riskLevel="Medium"
        connectedWallets={38}
        potentialExchanges={7}
      />

      {/* New Investigation Case Modal */}
      <NewInvestigationModal
        isOpen={isNewCaseModalOpen}
        onClose={() => setIsNewCaseModalOpen(false)}
        onCreateCase={handleCreateNewCase}
      />

      {/* RPC Node Connection Test Modal */}
      <RpcConfigModal
        isOpen={isRpcModalOpen}
        onClose={() => setIsRpcModalOpen(false)}
        onBlockHeightFetched={(block) => setCurrentBlockNumber(block)}
      />
    </div>
  );
}
