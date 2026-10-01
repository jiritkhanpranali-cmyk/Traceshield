
"""
TraceShield Investigation Input Schemas.

These Pydantic models define the structured analytical
information accepted by the TraceShield investigation API.
"""

from typing import List, Optional

from pydantic import BaseModel, Field


class TransactionSummary(BaseModel):
    """Summary of blockchain transaction activity."""

    total_transactions: Optional[int] = None
    incoming_transactions: Optional[int] = None
    outgoing_transactions: Optional[int] = None
    total_value_received: Optional[float] = None
    total_value_sent: Optional[float] = None
    summary: Optional[str] = None


class FundFlow(BaseModel):
    """Represents one observed fund-flow record."""

    source_address: Optional[str] = None
    destination_address: Optional[str] = None
    transaction_hash: Optional[str] = None
    value: Optional[float] = None
    timestamp: Optional[str] = None
    hop_number: Optional[int] = None
    explanation: Optional[str] = None


class WalletRelationship(BaseModel):
    """Represents a relationship between wallets."""

    wallet_address: Optional[str] = None
    relationship_type: Optional[str] = None
    transaction_count: Optional[int] = None
    total_value: Optional[float] = None
    first_seen: Optional[str] = None
    last_seen: Optional[str] = None
    explanation: Optional[str] = None


class RiskIndicator(BaseModel):
    """Represents an analytical risk indicator."""

    indicator: str
    severity: Optional[str] = None
    description: Optional[str] = None
    explanation: Optional[str] = None
    evidence: List[str] = Field(default_factory=list)


class EntityIntelligence(BaseModel):
    """Represents external or supplied entity intelligence."""

    address: Optional[str] = None
    entity_name: Optional[str] = None
    entity_type: Optional[str] = None
    attribution: Optional[str] = None
    source: Optional[str] = None
    confidence: Optional[str] = None
    explanation: Optional[str] = None


class TimelineEvent(BaseModel):
    """Represents an investigation timeline event."""

    timestamp: Optional[str] = None
    block_number: Optional[int] = None
    transaction_hash: Optional[str] = None
    event_type: Optional[str] = None
    description: Optional[str] = None
    evidence_reference: Optional[str] = None


class InvestigationInput(BaseModel):
    """
    Complete input model for a TraceShield investigation.

    The information supplied here should originate from
    verified analytical or intelligence sources.
    """

    case_id: str
    wallet_address: str
    network: str

    transaction_summary: Optional[
        TransactionSummary
    ] = None

    fund_flows: List[FundFlow] = Field(
        default_factory=list
    )

    wallet_relationships: List[WalletRelationship] = Field(
        default_factory=list
    )

    risk_indicators: List[RiskIndicator] = Field(
        default_factory=list
    )

    entity_intelligence: List[EntityIntelligence] = Field(
        default_factory=list
    )

    timeline_events: List[TimelineEvent] = Field(
        default_factory=list
    )

