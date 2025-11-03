"""
Order 5 Module: Amicable Resolution
Legal Advisory System v8.0

This module implements the 6D logic tree for Singapore Rules of Court Order 5
(Amicable Resolution).

Coverage:
- Rule 1: Duty to consider amicable resolution
- Rule 2: Terms of amicable resolution
- Rule 3: Powers of Court

Expert Validation: Required
Authority Weight: 0.8 (Rules of Court)
Effective Date: 1 Dec 2021
"""

from typing import Dict, List, Optional
import sys
import os

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from six_dimensions import (
    LegalLogicNode, Proposition, Conditional, Modality,
    ModalityType, SourceType
)
from logic_tree_module import (
    LogicTreeModule, ModuleMetadata, ModuleCoverage, SearchResult, ReasoningResult,
    ReasoningStep
)


class Order5Module(LogicTreeModule):
    """
    Order 5: Amicable Resolution Module

    Covers the duty to attempt settlement and court's ADR powers.

    Key Topics:
    - Amicable resolution duty
    - Settlement offers
    - ADR procedures
    - Court's power to order mediation
    """

    def __init__(self):
        """Initialize Order 5 module."""
        super().__init__()
        self.module_id = "order_5"
        self._initialized = False

    def get_metadata(self) -> ModuleMetadata:
        """Get module metadata for routing."""
        from datetime import datetime
        return ModuleMetadata(
            module_id="order_5",
            name="Order 5 - Amicable Resolution",
            version="1.0.0",
            coverage=ModuleCoverage(
                statute="Rules of Court - Order 5",
                sections=[
                    "Order 5 Rule 1 - Duty to consider amicable resolution",
                    "Order 5 Rule 2 - Terms of amicable resolution",
                    "Order 5 Rule 3 - Powers of Court"
                ],
                topics=[
                    "amicable_resolution",
                    "adr",
                    "settlement",
                    "mediation",
                    "offer_to_settle",
                    "without_prejudice"
                ],
                keywords=[
                    "amicable resolution", "settle", "settlement", "ADR",
                    "alternative dispute resolution", "mediation", "offer",
                    "without prejudice", "reasonable grounds", "sealed document"
                ]
            ),
            authority_weight=0.8,
            effective_date=datetime(2021, 12, 1),
            description="Duty to consider amicable resolution and ADR procedures"
        )

    def load_nodes(self) -> Dict[str, LegalLogicNode]:
        """
        Load all Order 5 nodes in 6D format.

        Returns:
            Dict mapping node_id to LegalLogicNode
        """

        nodes = {}

        # ==================== ROOT NODE ====================
        nodes["order5_root"] = LegalLogicNode(
            node_id="order5_root",
            citation="Order 5 - Amicable Resolution",
            source_type=SourceType.RULE,

            what=[
                Proposition(
                    text="Order 5 governs the duty to consider amicable resolution of disputes",
                    confidence=1.0,
                    source_line="Order 5"
                )
            ],

            which=[
                Proposition(
                    text="Applies to all parties to any proceedings (actions or appeals)",
                    confidence=1.0,
                    source_line="Order 5, r. 1(1)"
                )
            ],

            if_then=[
                Conditional(
                    condition="party to any proceedings",
                    consequence="duty to consider amicable resolution applies",
                    confidence=1.0,
                    source_line="Order 5, r. 1(1)"
                )
            ],

            can_must=[
                Modality(
                    action="consider amicable resolution before and during proceedings",
                    modality_type=ModalityType.MUST,
                    conditions=["party to any proceedings"],
                    confidence=1.0,
                    source_line="Order 5, r. 1(1)"
                )
            ],

            given=[
                Proposition(
                    text="Dispute exists between parties",
                    confidence=1.0
                )
            ],

            why=[
                Proposition(
                    text="To promote early settlement and reduce litigation costs",
                    confidence=0.95
                ),
                Proposition(
                    text="To encourage parties to resolve disputes amicably",
                    confidence=0.95
                )
            ],

            parent_id=None,
            children_ids=["order5_rule1", "order5_rule2", "order5_rule3"],
            module_id="order_5",
            version="1.0.0"
        )

        # ==================== RULE 1: DUTY ====================
        nodes["order5_rule1"] = LegalLogicNode(
            node_id="order5_rule1",
            citation="Order 5 Rule 1 - Duty to consider amicable resolution",
            source_type=SourceType.RULE,

            what=[
                Proposition(
                    text="Party to any proceedings has duty to consider amicable resolution before commencement and during course of action or appeal",
                    confidence=1.0,
                    source_line="Order 5, r. 1(1)"
                ),
                Proposition(
                    text="Offer of amicable resolution means offer to settle or resolve dispute other than by litigation",
                    confidence=1.0,
                    source_line="Order 5, r. 1(3)"
                )
            ],

            which=[
                Proposition(
                    text="Applies to all parties to any proceedings (actions and appeals)",
                    confidence=1.0,
                    source_line="Order 5, r. 1(1)"
                ),
                Proposition(
                    text="Applies whether dispute resolved in whole or in part",
                    confidence=1.0,
                    source_line="Order 5, r. 1(3)"
                )
            ],

            if_then=[
                Conditional(
                    condition="party is commencing action",
                    consequence="party is to make offer of amicable resolution",
                    confidence=1.0,
                    source_line="Order 5, r. 1(2)"
                ),
                Conditional(
                    condition="party receives offer of amicable resolution",
                    consequence="party must not reject offer",
                    confidence=1.0,
                    source_line="Order 5, r. 1(4)"
                )
            ],

            can_must=[
                Modality(
                    action="consider amicable resolution before commencement and during proceedings",
                    modality_type=ModalityType.MUST,
                    conditions=["party to any proceedings"],
                    confidence=1.0,
                    source_line="Order 5, r. 1(1)"
                ),
                Modality(
                    action="make offer of amicable resolution before commencing action",
                    modality_type=ModalityType.SHOULD,
                    conditions=["commencing action"],
                    confidence=1.0,
                    source_line="Order 5, r. 1(2)"
                ),
                Modality(
                    action="reject offer of amicable resolution",
                    modality_type=ModalityType.MUST_NOT,
                    conditions=["received offer"],
                    confidence=1.0,
                    source_line="Order 5, r. 1(4)"
                )
            ],

            given=[
                Proposition(
                    text="Dispute exists between parties",
                    confidence=1.0
                ),
                Proposition(
                    text="Proceedings are being commenced or are ongoing",
                    confidence=1.0
                )
            ],

            why=[
                Proposition(
                    text="To encourage early settlement before costly litigation",
                    confidence=0.95
                ),
                Proposition(
                    text="To reduce court caseload and promote access to justice",
                    confidence=0.9
                ),
                Proposition(
                    text="To preserve business relationships through amicable resolution",
                    confidence=0.9
                )
            ],

            parent_id="order5_root",
            children_ids=[],
            module_id="order_5",
            version="1.0.0"
        )

        # ==================== RULE 2: TERMS ====================
        nodes["order5_rule2"] = LegalLogicNode(
            node_id="order5_rule2",
            citation="Order 5 Rule 2 - Terms of amicable resolution",
            source_type=SourceType.RULE,

            what=[
                Proposition(
                    text="Offer of amicable resolution and rejection must be in writing",
                    confidence=1.0,
                    source_line="Order 5, r. 2(1)"
                ),
                Proposition(
                    text="Offer must be open for acceptance for reasonable period, at least 14 days",
                    confidence=1.0,
                    source_line="Order 5, r. 2(2)"
                ),
                Proposition(
                    text="Terms of unaccepted offer must not be disclosed until after merits determined",
                    confidence=1.0,
                    source_line="Order 5, r. 2(3)"
                ),
                Proposition(
                    text="Offer without expiry date expires when court determines merits",
                    confidence=1.0,
                    source_line="Order 5, r. 2(4)"
                )
            ],

            which=[
                Proposition(
                    text="Applies to all offers of amicable resolution under this Order",
                    confidence=1.0,
                    source_line="Order 5, r. 2"
                )
            ],

            if_then=[
                Conditional(
                    condition="offer of amicable resolution is made",
                    consequence="offer must be in writing",
                    confidence=1.0,
                    source_line="Order 5, r. 2(1)"
                ),
                Conditional(
                    condition="offer of amicable resolution is made",
                    consequence="offer must be open for at least 14 days",
                    confidence=1.0,
                    source_line="Order 5, r. 2(2)"
                ),
                Conditional(
                    condition="offer made and not accepted",
                    consequence="terms must not be made known to Court until after merits determined",
                    confidence=1.0,
                    source_line="Order 5, r. 2(3)"
                ),
                Conditional(
                    condition="offer does not state expiry date",
                    consequence="offer expires when Court determines merits",
                    confidence=1.0,
                    source_line="Order 5, r. 2(4)"
                )
            ],

            can_must=[
                Modality(
                    action="make offer in writing",
                    modality_type=ModalityType.MUST,
                    conditions=["making offer of amicable resolution"],
                    confidence=1.0,
                    source_line="Order 5, r. 2(1)"
                ),
                Modality(
                    action="make rejection in writing",
                    modality_type=ModalityType.MUST,
                    conditions=["rejecting offer of amicable resolution"],
                    confidence=1.0,
                    source_line="Order 5, r. 2(1)"
                ),
                Modality(
                    action="keep offer open for at least 14 days",
                    modality_type=ModalityType.MUST,
                    conditions=["making offer"],
                    confidence=1.0,
                    source_line="Order 5, r. 2(2)"
                ),
                Modality(
                    action="disclose terms of unaccepted offer to Court before merits determined",
                    modality_type=ModalityType.MUST_NOT,
                    conditions=["offer not accepted"],
                    confidence=1.0,
                    source_line="Order 5, r. 2(3)"
                ),
                Modality(
                    action="rely on terms of unaccepted offer at trial",
                    modality_type=ModalityType.MUST_NOT,
                    conditions=["merits not yet determined"],
                    confidence=1.0,
                    source_line="Order 5, r. 2(3)"
                )
            ],

            given=[
                Proposition(
                    text="Offer of amicable resolution has been made",
                    confidence=1.0
                )
            ],

            why=[
                Proposition(
                    text="To protect confidentiality of settlement negotiations",
                    confidence=0.95
                ),
                Proposition(
                    text="To prevent prejudice if court learns of settlement offers before deciding merits",
                    confidence=0.95
                ),
                Proposition(
                    text="To encourage frank settlement discussions without fear of disclosure",
                    confidence=0.9
                ),
                Proposition(
                    text="To ensure parties have adequate time to consider offers",
                    confidence=0.9
                )
            ],

            parent_id="order5_root",
            children_ids=[],
            module_id="order_5",
            version="1.0.0"
        )

        # ==================== RULE 3: POWERS ====================
        nodes["order5_rule3"] = LegalLogicNode(
            node_id="order5_rule3",
            citation="Order 5 Rule 3 - Powers of Court",
            source_type=SourceType.RULE,

            what=[
                Proposition(
                    text="Court may order parties to attempt amicable resolution",
                    confidence=1.0,
                    source_line="Order 5, r. 3(1)"
                ),
                Proposition(
                    text="Court may order party refusing ADR to submit sealed document with reasons",
                    confidence=1.0,
                    source_line="Order 5, r. 3(3)"
                ),
                Proposition(
                    text="Sealed document opened only after merits determined, may be referred to on costs",
                    confidence=1.0,
                    source_line="Order 5, r. 3(4)"
                ),
                Proposition(
                    text="Court may suggest solutions for amicable resolution at any time",
                    confidence=1.0,
                    source_line="Order 5, r. 3(5)"
                )
            ],

            which=[
                Proposition(
                    text="Applies to any proceedings before the Court",
                    confidence=1.0,
                    source_line="Order 5, r. 3"
                )
            ],

            if_then=[
                Conditional(
                    condition="Court decides to exercise power to order ADR",
                    consequence="Court must have regard to Ideals and all relevant circumstances",
                    confidence=1.0,
                    source_line="Order 5, r. 3(2)"
                ),
                Conditional(
                    condition="party refuses to attempt amicable resolution",
                    consequence="Court considers this when deciding whether to order ADR",
                    confidence=1.0,
                    source_line="Order 5, r. 3(2)"
                ),
                Conditional(
                    condition="party informs Court they do not wish to attempt ADR",
                    consequence="Court may order sealed document setting out reasons",
                    confidence=1.0,
                    source_line="Order 5, r. 3(3)"
                ),
                Conditional(
                    condition="sealed document ordered",
                    consequence="document opened only after merits determined",
                    confidence=1.0,
                    source_line="Order 5, r. 3(4)"
                ),
                Conditional(
                    condition="sealed document is opened",
                    consequence="contents may be referred to on issue of costs",
                    confidence=1.0,
                    source_line="Order 5, r. 3(4)"
                )
            ],

            can_must=[
                Modality(
                    action="order parties to attempt amicable resolution",
                    modality_type=ModalityType.MAY,
                    conditions=["Court's discretion"],
                    confidence=1.0,
                    source_line="Order 5, r. 3(1)"
                ),
                Modality(
                    action="have regard to Ideals and relevant circumstances",
                    modality_type=ModalityType.MUST,
                    conditions=["deciding whether to order ADR"],
                    confidence=1.0,
                    source_line="Order 5, r. 3(2)"
                ),
                Modality(
                    action="consider whether parties refused to attempt ADR",
                    modality_type=ModalityType.MUST,
                    conditions=["deciding whether to order ADR"],
                    confidence=1.0,
                    source_line="Order 5, r. 3(2)"
                ),
                Modality(
                    action="order party to submit sealed document with reasons for refusal",
                    modality_type=ModalityType.MAY,
                    conditions=["party refuses to attempt ADR"],
                    confidence=1.0,
                    source_line="Order 5, r. 3(3)"
                ),
                Modality(
                    action="suggest solutions for amicable resolution",
                    modality_type=ModalityType.MAY,
                    conditions=["at any time as Court thinks fit"],
                    confidence=1.0,
                    source_line="Order 5, r. 3(5)"
                )
            ],

            given=[
                Proposition(
                    text="Proceedings are before the Court",
                    confidence=1.0
                ),
                Proposition(
                    text="Court has case management powers",
                    confidence=1.0
                )
            ],

            why=[
                Proposition(
                    text="To enable Court to actively manage cases and promote settlement",
                    confidence=0.95
                ),
                Proposition(
                    text="To create consequences for unreasonable refusal to attempt ADR (costs)",
                    confidence=0.95
                ),
                Proposition(
                    text="To protect confidentiality while preserving Court's ability to consider refusal on costs",
                    confidence=0.9
                ),
                Proposition(
                    text="To give Court flexibility to facilitate settlement at appropriate times",
                    confidence=0.9
                )
            ],

            parent_id="order5_root",
            children_ids=[],
            module_id="order_5",
            version="1.0.0"
        )

        return nodes

    def search(
        self,
        query: str,
        filters: Optional[Dict] = None,
        top_k: int = 10
    ) -> List[SearchResult]:
        """
        Search for nodes matching query.

        Args:
            query: Search query
            filters: Optional filters
            top_k: Number of results

        Returns:
            List of SearchResult objects
        """

        if not self._initialized:
            self.initialize()

        results = []
        query_lower = query.lower()

        # Search keywords
        for node_id, node in self.nodes.items():
            score = 0.0

            # Match against citation
            if any(term in node.citation.lower() for term in query_lower.split()):
                score += 0.3

            # Match against WHAT dimension
            for what in node.what:
                if any(term in what.text.lower() for term in query_lower.split()):
                    score += 0.4

            # Match against keywords
            keywords = [
                "amicable", "resolution", "adr", "settlement", "mediation",
                "offer", "sealed", "document", "reasonable", "grounds"
            ]
            for keyword in keywords:
                if keyword in query_lower and keyword in node.citation.lower():
                    score += 0.2

            if score > 0:
                results.append(SearchResult(
                    node_id=node_id,
                    node=node,
                    score=score,
                    matched_text=node.citation
                ))

        # Sort by score
        results.sort(key=lambda x: x.score, reverse=True)

        return results[:top_k]

    def reason(self, question: str) -> ReasoningResult:
        """
        Answer question using logic tree.

        Args:
            question: Natural language question

        Returns:
            ReasoningResult with conclusion and chain
        """

        if not self._initialized:
            self.initialize()

        question_lower = question.lower()

        # Determine which rule applies
        target_node_id = None

        # Rule 1: Duty questions
        if any(term in question_lower for term in ["duty", "must make", "must offer", "reject", "reasonable grounds"]):
            target_node_id = "order5_rule1"

        # Rule 2: Terms/requirements questions
        elif any(term in question_lower for term in ["writing", "14 days", "open for", "disclose", "confidential", "without prejudice"]):
            target_node_id = "order5_rule2"

        # Rule 3: Court powers questions
        elif any(term in question_lower for term in ["court order", "court may", "sealed document", "suggest", "court power"]):
            target_node_id = "order5_rule3"

        # General amicable resolution
        else:
            target_node_id = "order5_root"

        if not target_node_id or target_node_id not in self.nodes:
            return ReasoningResult(
                conclusion="Unable to determine applicable rule",
                confidence=0.0,
                reasoning_chain=[],
                source_nodes=[]
            )

        node = self.nodes[target_node_id]
        chain = []

        # Build reasoning chain from 6D dimensions

        # GIVEN (prerequisites)
        for given in node.given:
            chain.append(ReasoningStep(
                dimension="GIVEN",
                text=given.text,
                confidence=given.confidence,
                source_citation=node.citation
            ))

        # WHICH (scope)
        for which in node.which:
            chain.append(ReasoningStep(
                dimension="WHICH",
                text=which.text,
                confidence=which.confidence,
                source_citation=node.citation
            ))

        # IF-THEN (conditions)
        for if_then in node.if_then:
            text = f"IF {if_then.condition} THEN {if_then.consequence}"
            if if_then.exceptions:
                text += f" (EXCEPT: {', '.join(if_then.exceptions)})"

            chain.append(ReasoningStep(
                dimension="IF-THEN",
                text=text,
                confidence=if_then.confidence,
                source_citation=node.citation
            ))

        # WHAT (holdings)
        for what in node.what:
            chain.append(ReasoningStep(
                dimension="WHAT",
                text=what.text,
                confidence=what.confidence,
                source_citation=node.citation
            ))

        # CAN/MUST (obligations)
        for can_must in node.can_must:
            text = f"{can_must.modality_type.value} {can_must.action}"
            if can_must.conditions:
                text += f" (when: {', '.join(can_must.conditions)})"
            if can_must.exceptions:
                text += f" (except: {', '.join(can_must.exceptions)})"

            chain.append(ReasoningStep(
                dimension="CAN/MUST",
                text=text,
                confidence=can_must.confidence,
                source_citation=node.citation
            ))

        # WHY (rationale)
        for why in node.why:
            chain.append(ReasoningStep(
                dimension="WHY",
                text=why.text,
                confidence=why.confidence,
                source_citation=node.citation
            ))

        # Generate conclusion
        conclusion = self._generate_conclusion(question, node)

        return ReasoningResult(
            conclusion=conclusion,
            confidence=0.9,  # High confidence for rules-based reasoning
            reasoning_chain=chain,
            source_nodes=[node.node_id]
        )

    def _generate_conclusion(self, question: str, node: LegalLogicNode) -> str:
        """Generate natural language conclusion."""

        question_lower = question.lower()

        # Obligation questions
        if "must" in question_lower or "have to" in question_lower:
            obligations = [cm for cm in node.can_must if cm.modality_type in [ModalityType.MUST, ModalityType.SHALL]]
            if obligations:
                conclusion = obligations[0].action
                if obligations[0].conditions:
                    conclusion += f" (when: {', '.join(obligations[0].conditions)})"
                if obligations[0].exceptions:
                    conclusion += f" (except: {', '.join(obligations[0].exceptions)})"
                return conclusion.capitalize()

        # Permission questions
        elif "can" in question_lower or "may" in question_lower:
            permissions = [cm for cm in node.can_must if cm.modality_type in [ModalityType.MAY, ModalityType.CAN]]
            if permissions:
                return f"Yes, {permissions[0].action}"

        # What/definitional questions
        elif "what" in question_lower:
            if node.what:
                return node.what[0].text

        # Default: return first WHAT
        if node.what:
            return node.what[0].text

        return "See " + node.citation
