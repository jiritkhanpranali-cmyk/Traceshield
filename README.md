# TraceShield AI — Blockchain Investigation & Analytics Platform

> **Smart India Hackathon 2026 (SIH 2026)**  
> **Problem Owner / Theme:** Ministry of Home Affairs (MHA) — Cybersecurity & Blockchain  
> **Official Problem Statement:** *"Real-Time Identification of Fraud-Linked Cryptocurrency Exchanges from Victim-Reported Suspect Wallet Addresses through Automated Blockchain Analytics."*

---

## 🛡️ Project Overview

**TraceShield AI** is an investigation-support platform engineered to assist cybercrime investigators, digital forensics experts, and financial intelligence units in analyzing cryptocurrency transaction trails starting from a victim-reported suspect wallet address.

### Core Capabilities:
1. **Live Blockchain Data First**: Connects to real EVM/Ethereum RPC infrastructure with live block tracking and WebSocket streaming.
2. **Interactive Transaction Network Graph**: Real-time canvas-based physics network graph with animated particle fund flow, node dragging, zoom/pan controls, and multi-view switching (Graph View, Chronological Timeline, Multi-Hop Waterfall Flow).
3. **Multi-Hop Fund Flow & Peel Chain Tracing**: Unveils fund movement across multiple hops (Victim Suspect Wallet → Intermediaries → Centralized Exchanges / Sanctioned Mixers).
4. **Exchange & Entity Attribution**: Identifies potentially exchange-linked deposit clusters (Binance, Coinbase Prime) and high-risk privacy services (Tornado Cash).
5. **AI-Assisted Investigation Reports**: Generates structured, evidence-grounded reports with case references, transaction evidence links, and export to PDF/Print or Markdown.
6. **Human-in-the-Loop Discipline**: Follows strict evidentiary standards — surfaces *investigation indicators* and *risk scores* without making unsubstantiated legal claims.

---

## 🚀 Quickstart Guide for VS Code

### Prerequisites
- **Node.js** (v18+ or v24+ recommended)
- **npm** (v9+ or v11+)

### Option 1: Run from Root Directory
Open the project root folder `c:\Traceshield` in VS Code, open the built-in terminal, and run:
```bash
npm run dev
```

### Option 2: Run from `frontend` Directory
```bash
cd frontend
npm install
npm run dev
```

Open your browser at:
👉 **`http://localhost:5173/`**

---

## 🖥️ UI Dashboard Structure (Matching Reference Design)

- **Header Bar**: Global search (wallet/tx/block/case ID), Investigation alerts dropdown, Investigator profile badge (`John Doe / Investigator`).
- **Control & Filter Bar**:
  - Network Selector: Ethereum Mainnet, Sepolia, Arbitrum, Polygon, BSC
  - Suspect Wallet Address Input: e.g. `0x7fC765629da776A1bf0C35B9A42Ef791B7b8a3F2`
  - Time Range: Last 24 Hours, 7 Days, 30 Days, All Time
  - Trace Depth: 1 Hop, 2 Hops, 3 Hops, 5 Hops
  - Risk Level: All, Low, Medium, High, Critical
- **Key Metrics (5 Stat Cards)**:
  - **Total Transactions**: `247` (+12% last 24h)
  - **Connected Wallets**: `38` (+8% last 24h)
  - **Potential Exchanges**: `7` (+2 new last 24h)
  - **Risk Level**: `Medium` (with dynamic visual risk meter)
  - **Last Activity**: `14:32` (Apr 26, 2025 / Live clock)
- **Transaction Network Graph**:
  - Central Monitored Wallet (`0x7fC7...a3F2`) with glowing cyan halo
  - Connected Counterparty Nodes (`0x8f3d...c9e2`, `0x4e9e...21a7`, `0x3c7d...e8f1`, `0x6a21...9b4c`, `0x91ab...d45e`)
  - Identified Exchange Clusters: `Binance (Exchange)`, `Coinbase (Exchange)`
  - Sanctioned Mixer Contract: `Tornado Cash`
  - Animated particle flow indicating real-time fund velocity and direction
  - Node Inspector Drawer on click with balances, volumes, and Etherscan shortcuts
- **Live Events Stream**:
  - Live pulse indicator, streaming real-time block detections, wallet interactions, and risk alerts with pause/resume controls.
- **Bottom Grid**:
  - **Recent Transactions**: Confirmed status badges, values in ETH, time, and deep tx modal inspector.
  - **Investigation Timeline**: Step-by-step audit milestones (Case Created, Initial Analysis, Live Monitoring Started, Latest Event).
  - **Quick Insights & AI Summary**: Potential Exchange Exposure warning card and collapsible Key Risks checklist with **Generate Report** action button.

---

## 🏛️ Project Architecture

```
TraceShield-AI/
│
├── frontend/
│   ├── index.html
│   ├── src/
│   │   ├── components/
│   │   │   ├── Header.jsx                 # Top navigation & global search
│   │   │   ├── Sidebar.jsx                # Left navigation & network status
│   │   │   ├── ControlBar.jsx             # Filter and parameter controls
│   │   │   ├── StatCards.jsx              # 5 summary metric cards
│   │   │   ├── TransactionNetworkGraph.jsx# Interactive physics canvas graph
│   │   │   ├── LiveEventsPanel.jsx        # Real-time event log
│   │   │   ├── RecentTransactions.jsx     # Recent transaction table
│   │   │   ├── InvestigationTimeline.jsx  # Investigation audit timeline
│   │   │   ├── QuickInsights.jsx          # AI insights & report trigger
│   │   │   ├── ReportModal.jsx            # AI Investigation Report Generator
│   │   │   ├── NewInvestigationModal.jsx  # Case creation & wallet validation
│   │   │   ├── NodeDetailDrawer.jsx       # Graph node inspection drawer
│   │   │   ├── TransactionDetailModal.jsx # Deep tx hash verification modal
│   │   │   └── RpcConfigModal.jsx         # Live Ethereum RPC connector
│   │   ├── App.jsx                        # Main workspace integration
│   │   ├── index.css                      # Cybersecurity glassmorphism tokens
│   │   └── main.jsx                       # React root entrypoint
│   └── package.json
│
├── backend/                               # Phase 1-4 Python / FastAPI Structure
│   ├── app/
│   │   ├── main.py                        # FastAPI endpoints
│   │   ├── config.py                      # Environment configuration
│   │   ├── services/
│   │   │   ├── blockchain_service.py      # Web3.py RPC / WebSocket listener
│   │   │   ├── transaction_service.py     # Ingestion & normalization
│   │   │   ├── graph_service.py           # NetworkX graph topology
│   │   │   ├── risk_service.py            # Risk indicators & scoring
│   │   │   └── ai_service.py              # LLM explanation & report engine
│   │   └── database/                      # PostgreSQL schemas
│   └── requirements.txt
│
├── package.json                           # Root scripts
└── README.md
```

---

## ⚖️ Compliance & Evidentiary Standards
- **Data First, Analysis Second, AI Third, Human-in-the-Loop Always.**
- Terminology follows strict forensic standards (*"potentially exchange-linked"*, *"investigation indicator"*, *"risk assessment"*).
- Preserves full auditability for legal and regulatory proceedings under Indian cyber law and international FATF recommendations.
