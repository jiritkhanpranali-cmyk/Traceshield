from typing import List, Optional

from pydantic import BaseModel, Field


class CaseInformation(BaseModel):
    case_id: str
    network: str
    investigated_wallet: str


class TransactionReport(BaseModel):
    total_transactions: Optional[int] = None
    incoming_transactions: Optional[int] = None
    outgoing_transactions: Optional[int] = None
    total_value_received: Optional[float] = None
    total_value_sent: Optional[float] = None
    summary: Optional[str] = None


class FundFlowReport(BaseModel):
    source_address: Optional[str] = None
    destination_address: Optional[str] = None
    transaction_hash: Optional[str] = None
    value: Optional[float] = None
    timestamp: Optional[str] = None
    hop_number: Optional[int] = None
    explanation: Optional[str] = None


class WalletRelationshipReport(BaseModel):
    wallet_address: Optional[str] = None
    relationship_type: Optional[str] = None
    transaction_count: Optional[int] = None
    total_value: Optional[float] = None
    first_seen: Optional[str] = None
    last_seen: Optional[str] = None
    explanation: Optional[str] = None


class RiskIndicatorReport(BaseModel):
    indicator: str
    severity: Optional[str] = None
    description: Optional[str] = None
    explanation: Optional[str] = None
    evidence: List[str] = Field(default_factory=list)


class EntityIntelligenceReport(BaseModel):
    address: Optional[str] = None
    entity_name: Optional[str] = None
    entity_type: Optional[str] = None
    attribution: Optional[str] = None
    source: Optional[str] = None
    confidence: Optional[str] = None
    explanation: Optional[str] = None


class TimelineReport(BaseModel):
    timestamp: Optional[str] = None
    block_number: Optional[int] = None
    transaction_hash: Optional[str] = None
    event_type: Optional[str] = None
    description: Optional[str] = None
    evidence_reference: Optional[str] = None


class InvestigationReport(BaseModel):
    """
    Structured TraceShield AI investigation report.

    The report contains verified analytical information and
    AI-assisted explanations. It does not establish criminality,
    ownership, identity, or intent.
    """

    case_information: CaseInformation

    investigation_summary: str

    transaction_summary: TransactionReport

    major_fund_flows: List[FundFlowReport] = Field(
        default_factory=list
    )

    wallet_relationships: List[WalletRelationshipReport] = Field(
        default_factory=list
    )

    risk_indicators: List[RiskIndicatorReport] = Field(
        default_factory=list
    )

    entity_intelligence: List[EntityIntelligenceReport] = Field(
        default_factory=list
    )

    investigation_timeline: List[TimelineReport] = Field(
        default_factory=list
    )

    analytical_interpretation: Optional[str] = None

    evidence_references: List[str] = Field(
        default_factory=list
    )

    investigator_review_notes: Optional[str] = None

    limitations: List[str] = Field(
        default_factory=list
    )
    