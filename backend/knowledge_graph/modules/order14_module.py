"""
Order 14 Module: Payment into Court
Legal Advisory System v8.0

This module implements the 6D logic tree for Singapore Rules of Court Order 14
(Payment into Court).

Coverage:
- Rule 1: Payment into Court
- Rule 2: Payment by defendant who has counterclaimed
- Rule 3: Acceptance of money paid into Court
- Rule 4: Order for payment out required in certain cases
- Rule 5: Money remaining in Court
- Rule 6: Counterclaim
- Rule 7: Non-disclosure of payment into Court
- Rules 8-12: Technical procedures

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


class Order14Module(LogicTreeModule):
    """
    Order 14: Payment into Court Module

    Covers payment into court procedures, acceptance, and disclosure rules.

    Key Topics:
    - Payment into court
    - Acceptance of payment
    - Settlement offers (Calderbank offers)
    - Costs consequences
    - Non-disclosure rules
    """

    def __init__(self):
        """Initialize Order 14 module."""
        super().__init__()
        self.module_id = "order_14"
        self._initialized = False

    def get_metadata(self) -> ModuleMetadata:
        """Get module metadata for routing."""
        from datetime import datetime
        return ModuleMetadata(
            module_id="order_14",
            name="Order 14 - Payment into Court",
            version="1.0.0",
            coverage=ModuleCoverage(
                statute="Rules of Court - Order 14",
                sections=[
                    "Order 14 Rule 1 - Payment into Court",
                    "Order 14 Rule 2 - Payment with counterclaim",
                    "Order 14 Rule 3 - Acceptance",
                    "Order 14 Rule 7 - Non-disclosure"
                ],
                topics=[
                    "payment_into_court",
                    "calderbank",
                    "settlement_offer",
                    "acceptance",
                    "costs_consequences",
                    "form_27",
                    "form_28"
                ],
                keywords=[
                    "payment into court", "pay into court", "Calderbank", "offer",
                    "accept", "acceptance", "Form 27", "Form 28", "14 days",
                    "counterclaim", "satisfaction", "stayed", "disclosure",
                    "non-disclosure", "tender"
                ]
            ),
            authority_weight=0.8,
            effective_date=datetime(2021, 12, 1),
            description="Payment into court procedures and settlement mechanisms"
        )

    def load_nodes(self) -> Dict[str, LegalLogicNode]:
        """
        Load all Order 14 nodes in 6D format.

        Returns:
            Dict mapping node_id to LegalLogicNode
        """

        nodes = {}

        # ==================== ROOT NODE ====================
        nodes["order14_root"] = LegalLogicNode(
            node_id="order14_root",
            citation="Order 14 - Payment into Court",
            source_type=SourceType.RULE,

            what=[
                Proposition(
                    text="Order 14 governs payment into court as settlement mechanism",
                    confidence=1.0,
                    source_line="Order 14"
                )
            ],

            which=[
                Proposition(
                    text="Applies to actions for debt or damages",
                    confidence=1.0,
                    source_line="Order 14, r. 1(1)"
                )
            ],

            if_then=[
                Conditional(
                    condition="action is for debt or damages",
                    consequence="defendant may pay money into court in satisfaction",
                    confidence=1.0,
                    source_line="Order 14, r. 1(1)"
                )
            ],

            can_must=[
                Modality(
                    action="pay money into court in satisfaction of claim",
                    modality_type=ModalityType.MAY,
                    conditions=["defendant in action for debt or damages"],
                    confidence=1.0,
                    source_line="Order 14, r. 1(1)"
                )
            ],

            given=[
                Proposition(
                    text="Action for debt or damages has been commenced",
                    confidence=1.0
                )
            ],

            why=[
                Proposition(
                    text="To provide settlement mechanism with costs protection for defendants",
                    confidence=0.95
                ),
                Proposition(
                    text="To encourage early settlement by creating costs consequences",
                    confidence=0.95
                )
            ],

            parent_id=None,
            children_ids=[
                "order14_rule1", "order14_rule2", "order14_rule3",
                "order14_rule4", "order14_rule5", "order14_rule7"
            ],
            module_id="order_14",
            version="1.0.0"
        )

        # ==================== RULE 1: PAYMENT INTO COURT ====================
        nodes["order14_rule1"] = LegalLogicNode(
            node_id="order14_rule1",
            citation="Order 14 Rule 1 - Payment into Court",
            source_type=SourceType.RULE,

            what=[
                Proposition(
                    text="Defendant may pay money into Court in satisfaction of cause of action",
                    confidence=1.0,
                    source_line="Order 14, r. 1(1)"
                ),
                Proposition(
                    text="Defendant must give notice in Form 27 to claimant and other defendants",
                    confidence=1.0,
                    source_line="Order 14, r. 1(2)"
                ),
                Proposition(
                    text="Claimant must send written acknowledgment within 3 days",
                    confidence=1.0,
                    source_line="Order 14, r. 1(2)"
                ),
                Proposition(
                    text="Defendant may increase payment without permission",
                    confidence=1.0,
                    source_line="Order 14, r. 1(3)"
                ),
                Proposition(
                    text="Notice of payment may not be withdrawn or amended without Court permission",
                    confidence=1.0,
                    source_line="Order 14, r. 1(3)"
                )
            ],

            which=[
                Proposition(
                    text="Applies to any action for debt or damages",
                    confidence=1.0,
                    source_line="Order 14, r. 1(1)"
                ),
                Proposition(
                    text="Available after defendant has filed notice of intention to contest or not contest",
                    confidence=1.0,
                    source_line="Order 14, r. 1(1)"
                ),
                Proposition(
                    text="May be for all or some of multiple causes of action",
                    confidence=1.0,
                    source_line="Order 14, r. 1(1)"
                )
            ],

            if_then=[
                Conditional(
                    condition="defendant pays money into court",
                    consequence="defendant must give notice in Form 27",
                    confidence=1.0,
                    source_line="Order 14, r. 1(2)"
                ),
                Conditional(
                    condition="claimant receives notice of payment",
                    consequence="claimant must send written acknowledgment within 3 days",
                    confidence=1.0,
                    source_line="Order 14, r. 1(2)"
                ),
                Conditional(
                    condition="defendant wants to increase payment",
                    consequence="may do so without permission",
                    confidence=1.0,
                    source_line="Order 14, r. 1(3)"
                ),
                Conditional(
                    condition="defendant wants to withdraw or amend notice",
                    consequence="must obtain Court permission",
                    confidence=1.0,
                    source_line="Order 14, r. 1(3)"
                ),
                Conditional(
                    condition="multiple causes of action and single payment made",
                    consequence="Court may order defendant to specify sum per cause if claimant embarrassed",
                    confidence=1.0,
                    source_line="Order 14, r. 1(5)"
                )
            ],

            can_must=[
                Modality(
                    action="pay money into Court in satisfaction of cause of action",
                    modality_type=ModalityType.MAY,
                    conditions=["defendant filed notice of intention", "action for debt or damages"],
                    confidence=1.0,
                    source_line="Order 14, r. 1(1)"
                ),
                Modality(
                    action="give notice in Form 27 to claimant and other defendants",
                    modality_type=ModalityType.MUST,
                    conditions=["making payment or increasing payment"],
                    confidence=1.0,
                    source_line="Order 14, r. 1(2)"
                ),
                Modality(
                    action="send written acknowledgment of receipt",
                    modality_type=ModalityType.MUST,
                    conditions=["claimant received notice", "within 3 days"],
                    confidence=1.0,
                    source_line="Order 14, r. 1(2)"
                ),
                Modality(
                    action="increase payment without permission",
                    modality_type=ModalityType.MAY,
                    conditions=["defendant wants to increase"],
                    confidence=1.0,
                    source_line="Order 14, r. 1(3)"
                ),
                Modality(
                    action="withdraw or amend notice without Court permission",
                    modality_type=ModalityType.MAY_NOT,
                    conditions=[],
                    confidence=1.0,
                    source_line="Order 14, r. 1(3)"
                )
            ],

            given=[
                Proposition(
                    text="Action for debt or damages commenced",
                    confidence=1.0
                ),
                Proposition(
                    text="Defendant has filed notice of intention to contest or not contest",
                    confidence=1.0,
                    source_line="Order 14, r. 1(1)"
                )
            ],

            why=[
                Proposition(
                    text="To allow defendant to make formal settlement offer with costs protection",
                    confidence=0.95
                ),
                Proposition(
                    text="To encourage claimant to accept reasonable offers (costs consequences)",
                    confidence=0.95
                ),
                Proposition(
                    text="To provide certainty through formal procedures (Form 27)",
                    confidence=0.9
                ),
                Proposition(
                    text="To prevent defendant from gaming system by withdrawing offers",
                    confidence=0.9
                )
            ],

            parent_id="order14_root",
            children_ids=[],
            module_id="order_14",
            version="1.0.0"
        )

        # ==================== RULE 2: PAYMENT WITH COUNTERCLAIM ====================
        nodes["order14_rule2"] = LegalLogicNode(
            node_id="order14_rule2",
            citation="Order 14 Rule 2 - Payment by defendant who has counterclaimed",
            source_type=SourceType.RULE,

            what=[
                Proposition(
                    text="Notice of payment must state if payment takes into account defendant's counterclaim",
                    confidence=1.0,
                    source_line="Order 14, r. 2"
                )
            ],

            which=[
                Proposition(
                    text="Applies where defendant makes counterclaim for debt or damages and pays into court",
                    confidence=1.0,
                    source_line="Order 14, r. 2"
                )
            ],

            if_then=[
                Conditional(
                    condition="defendant has counterclaim and pays into court",
                    consequence="notice must state if payment accounts for counterclaim",
                    confidence=1.0,
                    source_line="Order 14, r. 2"
                ),
                Conditional(
                    condition="payment intends to satisfy counterclaim",
                    consequence="notice must state which causes of action from counterclaim are satisfied",
                    confidence=1.0,
                    source_line="Order 14, r. 2"
                )
            ],

            can_must=[
                Modality(
                    action="state in notice whether payment takes into account and satisfies counterclaim",
                    modality_type=ModalityType.MUST,
                    conditions=["defendant has counterclaim", "making payment into court"],
                    confidence=1.0,
                    source_line="Order 14, r. 2"
                )
            ],

            given=[
                Proposition(
                    text="Defendant has made counterclaim for debt or damages",
                    confidence=1.0
                ),
                Proposition(
                    text="Defendant is making payment into court under Rule 1",
                    confidence=1.0
                )
            ],

            why=[
                Proposition(
                    text="To clarify whether payment is gross or net of counterclaim",
                    confidence=0.95
                ),
                Proposition(
                    text="To prevent confusion about what payment represents",
                    confidence=0.9
                ),
                Proposition(
                    text="To enable claimant to make informed decision on acceptance",
                    confidence=0.9
                )
            ],

            parent_id="order14_root",
            children_ids=[],
            module_id="order_14",
            version="1.0.0"
        )

        # ==================== RULE 3: ACCEPTANCE ====================
        nodes["order14_rule3"] = LegalLogicNode(
            node_id="order14_rule3",
            citation="Order 14 Rule 3 - Acceptance of money paid into Court",
            source_type=SourceType.RULE,

            what=[
                Proposition(
                    text="Claimant may accept money paid into court by giving notice in Form 28",
                    confidence=1.0,
                    source_line="Order 14, r. 3(1)"
                ),
                Proposition(
                    text="Acceptance must be within 14 days and before trial begins",
                    confidence=1.0,
                    source_line="Order 14, r. 3(1)"
                ),
                Proposition(
                    text="After trial begins, acceptance must be within 2 days and before judgment delivered",
                    confidence=1.0,
                    source_line="Order 14, r. 3(2)"
                ),
                Proposition(
                    text="On acceptance, all further proceedings are stayed",
                    confidence=1.0,
                    source_line="Order 14, r. 3(4)"
                ),
                Proposition(
                    text="Claimant entitled to payment of accepted sum",
                    confidence=1.0,
                    source_line="Order 14, r. 3(6)"
                )
            ],

            which=[
                Proposition(
                    text="Applies where money paid into Court under Rule 1",
                    confidence=1.0,
                    source_line="Order 14, r. 3(1)"
                ),
                Proposition(
                    text="May accept all or specified causes of action",
                    confidence=1.0,
                    source_line="Order 14, r. 3(1)"
                )
            ],

            if_then=[
                Conditional(
                    condition="money paid for all causes of action",
                    consequence="claimant may accept in satisfaction of all causes",
                    confidence=1.0,
                    source_line="Order 14, r. 3(1)(a)"
                ),
                Conditional(
                    condition="money paid for some causes only",
                    consequence="claimant may accept specified sum for those causes",
                    confidence=1.0,
                    source_line="Order 14, r. 3(1)(b)"
                ),
                Conditional(
                    condition="claimant accepts money",
                    consequence="all further proceedings stayed",
                    confidence=1.0,
                    source_line="Order 14, r. 3(4)"
                ),
                Conditional(
                    condition="acceptance before trial begins",
                    consequence="must be within 14 days of notice receipt",
                    confidence=1.0,
                    source_line="Order 14, r. 3(1)"
                ),
                Conditional(
                    condition="acceptance after trial begins",
                    consequence="must be within 2 days and before judgment",
                    confidence=1.0,
                    source_line="Order 14, r. 3(2)"
                ),
                Conditional(
                    condition="payment made with counterclaim statement",
                    consequence="on acceptance, counterclaim proceedings also stayed",
                    confidence=1.0,
                    source_line="Order 14, r. 3(5)"
                )
            ],

            can_must=[
                Modality(
                    action="accept money paid into Court",
                    modality_type=ModalityType.MAY,
                    conditions=["within 14 days of notice", "before trial begins"],
                    confidence=1.0,
                    source_line="Order 14, r. 3(1)"
                ),
                Modality(
                    action="accept money after trial begins",
                    modality_type=ModalityType.MAY,
                    conditions=["within 2 days of notice", "before judgment delivered"],
                    confidence=1.0,
                    source_line="Order 14, r. 3(2)"
                ),
                Modality(
                    action="give notice in Form 28 to every defendant",
                    modality_type=ModalityType.MUST,
                    conditions=["accepting payment"],
                    confidence=1.0,
                    source_line="Order 14, r. 3(1)"
                )
            ],

            given=[
                Proposition(
                    text="Money has been paid into Court under Rule 1",
                    confidence=1.0
                ),
                Proposition(
                    text="Claimant has received notice of payment",
                    confidence=1.0
                )
            ],

            why=[
                Proposition(
                    text="To enable quick settlement without further litigation",
                    confidence=0.95
                ),
                Proposition(
                    text="To create clear time limits for acceptance (certainty)",
                    confidence=0.95
                ),
                Proposition(
                    text="To automatically stay proceedings on acceptance (efficiency)",
                    confidence=0.9
                ),
                Proposition(
                    text="To allow acceptance even after trial starts (flexibility)",
                    confidence=0.85
                )
            ],

            parent_id="order14_root",
            children_ids=[],
            module_id="order_14",
            version="1.0.0"
        )

        # ==================== RULE 4: ORDER FOR PAYMENT OUT ====================
        nodes["order14_rule4"] = LegalLogicNode(
            node_id="order14_rule4",
            citation="Order 14 Rule 4 - Order for payment out required in certain cases",
            source_type=SourceType.RULE,

            what=[
                Proposition(
                    text="Court order required for payment out in certain cases",
                    confidence=1.0,
                    source_line="Order 14, r. 4(1)"
                ),
                Proposition(
                    text="Order must deal with whole costs of action",
                    confidence=1.0,
                    source_line="Order 14, r. 4(1)"
                )
            ],

            which=[
                Proposition(
                    text="Applies where payment made by some but not all joint defendants",
                    confidence=1.0,
                    source_line="Order 14, r. 4(1)(a)"
                ),
                Proposition(
                    text="Applies where payment made with defence of tender before action",
                    confidence=1.0,
                    source_line="Order 14, r. 4(1)(b)"
                ),
                Proposition(
                    text="Applies where multiple persons entitled to money (Civil Law Act cases)",
                    confidence=1.0,
                    source_line="Order 14, r. 4(1)(c)"
                )
            ],

            if_then=[
                Conditional(
                    condition="payment by some joint defendants only",
                    consequence="payment out requires Court order dealing with costs",
                    confidence=1.0,
                    source_line="Order 14, r. 4(1)(a), (2)"
                ),
                Conditional(
                    condition="acceptance after trial begun",
                    consequence="payment out requires Court order on costs",
                    confidence=1.0,
                    source_line="Order 14, r. 4(3)"
                )
            ],

            can_must=[
                Modality(
                    action="pay out money without Court order",
                    modality_type=ModalityType.MUST_NOT,
                    conditions=["special cases under r. 4(1)"],
                    confidence=1.0,
                    source_line="Order 14, r. 4(1)"
                )
            ],

            given=[
                Proposition(
                    text="Claimant has accepted money paid into Court",
                    confidence=1.0
                )
            ],

            why=[
                Proposition(
                    text="To ensure costs are properly dealt with in complex cases",
                    confidence=0.95
                ),
                Proposition(
                    text="To protect interests of non-paying joint defendants",
                    confidence=0.9
                ),
                Proposition(
                    text="To ensure proper distribution where multiple persons entitled",
                    confidence=0.9
                )
            ],

            parent_id="order14_root",
            children_ids=[],
            module_id="order_14",
            version="1.0.0"
        )

        # ==================== RULE 5: MONEY REMAINING ====================
        nodes["order14_rule5"] = LegalLogicNode(
            node_id="order14_rule5",
            citation="Order 14 Rule 5 - Money remaining in Court",
            source_type=SourceType.RULE,

            what=[
                Proposition(
                    text="Money not accepted must not be paid out except by Court order",
                    confidence=1.0,
                    source_line="Order 14, r. 5"
                ),
                Proposition(
                    text="Order may be made before, at, or after trial",
                    confidence=1.0,
                    source_line="Order 14, r. 5"
                )
            ],

            which=[
                Proposition(
                    text="Applies where money paid into Court is not accepted under Rule 3",
                    confidence=1.0,
                    source_line="Order 14, r. 5"
                )
            ],

            if_then=[
                Conditional(
                    condition="money not accepted and order made before trial",
                    consequence="money must not be paid except in satisfaction of causes for which paid in",
                    confidence=1.0,
                    source_line="Order 14, r. 5"
                )
            ],

            can_must=[
                Modality(
                    action="pay out money not accepted without Court order",
                    modality_type=ModalityType.MUST_NOT,
                    conditions=["money not accepted under Rule 3"],
                    confidence=1.0,
                    source_line="Order 14, r. 5"
                )
            ],

            given=[
                Proposition(
                    text="Money paid into Court under Rule 1",
                    confidence=1.0
                ),
                Proposition(
                    text="Money not accepted under Rule 3",
                    confidence=1.0
                )
            ],

            why=[
                Proposition(
                    text="To protect defendant's money until proper resolution",
                    confidence=0.95
                ),
                Proposition(
                    text="To ensure money only paid out in accordance with judgment or order",
                    confidence=0.95
                )
            ],

            parent_id="order14_root",
            children_ids=[],
            module_id="order_14",
            version="1.0.0"
        )

        # ==================== RULE 7: NON-DISCLOSURE ====================
        nodes["order14_rule7"] = LegalLogicNode(
            node_id="order14_rule7",
            citation="Order 14 Rule 7 - Non-disclosure of payment into Court",
            source_type=SourceType.RULE,

            what=[
                Proposition(
                    text="Fact that money paid into Court must not be communicated to Court at trial",
                    confidence=1.0,
                    source_line="Order 14, r. 7"
                ),
                Proposition(
                    text="Non-disclosure applies until all questions of liability and damages decided",
                    confidence=1.0,
                    source_line="Order 14, r. 7"
                )
            ],

            which=[
                Proposition(
                    text="Applies to all actions except tender before action defences",
                    confidence=1.0,
                    source_line="Order 14, r. 7"
                ),
                Proposition(
                    text="Applies except where proceedings stayed after trial begun under Rule 3(4)",
                    confidence=1.0,
                    source_line="Order 14, r. 7"
                )
            ],

            if_then=[
                Conditional(
                    condition="money paid into Court under Rules 1-6",
                    consequence="fact must not be pleaded or communicated to Court at trial",
                    confidence=1.0,
                    source_line="Order 14, r. 7"
                ),
                Conditional(
                    condition="liability and damages questions decided",
                    consequence="payment into court may then be disclosed",
                    confidence=1.0,
                    source_line="Order 14, r. 7"
                )
            ],

            can_must=[
                Modality(
                    action="plead fact of payment into Court",
                    modality_type=ModalityType.MUST_NOT,
                    conditions=["before liability and damages decided"],
                    confidence=1.0,
                    source_line="Order 14, r. 7"
                ),
                Modality(
                    action="communicate fact of payment to Court at trial",
                    modality_type=ModalityType.MAY_NOT,
                    conditions=["before liability and damages decided"],
                    confidence=1.0,
                    source_line="Order 14, r. 7"
                )
            ],

            given=[
                Proposition(
                    text="Money has been paid into Court",
                    confidence=1.0
                ),
                Proposition(
                    text="Trial or hearing is ongoing",
                    confidence=1.0
                )
            ],

            why=[
                Proposition(
                    text="To prevent prejudice to defendant if Court knows about payment offer",
                    confidence=0.95
                ),
                Proposition(
                    text="To ensure Court decides liability and quantum on merits alone",
                    confidence=0.95
                ),
                Proposition(
                    text="To preserve Court's ability to consider payment when assessing costs",
                    confidence=0.9
                ),
                Proposition(
                    text="To encourage defendants to make reasonable offers without fear of prejudice",
                    confidence=0.9
                )
            ],

            parent_id="order14_root",
            children_ids=[],
            module_id="order_14",
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
                "payment", "into court", "accept", "calderbank", "form 27",
                "form 28", "14 days", "disclosure", "stayed", "counterclaim"
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

        # Rule 1: Payment into court
        if any(term in question_lower for term in ["pay into court", "form 27", "notice of payment", "increase payment"]):
            target_node_id = "order14_rule1"

        # Rule 2: Counterclaim
        elif any(term in question_lower for term in ["counterclaim", "set off", "net"]):
            target_node_id = "order14_rule2"

        # Rule 3: Acceptance
        elif any(term in question_lower for term in ["accept", "acceptance", "form 28", "14 days", "stayed"]):
            target_node_id = "order14_rule3"

        # Rule 4: Payment out
        elif any(term in question_lower for term in ["payment out", "pay out", "joint defendants"]):
            target_node_id = "order14_rule4"

        # Rule 5: Money remaining
        elif any(term in question_lower for term in ["not accepted", "remaining", "money remaining"]):
            target_node_id = "order14_rule5"

        # Rule 7: Non-disclosure
        elif any(term in question_lower for term in ["disclose", "disclosure", "tell court", "inform court", "prejudice"]):
            target_node_id = "order14_rule7"

        # General payment into court
        else:
            target_node_id = "order14_root"

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
                conclusion = f"Yes, {permissions[0].action}"
                if permissions[0].conditions:
                    conclusion += f" (when: {', '.join(permissions[0].conditions)})"
                return conclusion

        # Prohibition questions
        elif "cannot" in question_lower or "must not" in question_lower:
            prohibitions = [cm for cm in node.can_must if cm.modality_type in [ModalityType.MUST_NOT, ModalityType.MAY_NOT]]
            if prohibitions:
                return f"No, {prohibitions[0].action}"

        # What/definitional questions
        elif "what" in question_lower:
            if node.what:
                return node.what[0].text

        # How questions
        elif "how" in question_lower:
            procedures = [cm for cm in node.can_must if cm.modality_type == ModalityType.MUST]
            if procedures:
                return f"You must {procedures[0].action}"

        # Default: return first WHAT
        if node.what:
            return node.what[0].text

        return "See " + node.citation
