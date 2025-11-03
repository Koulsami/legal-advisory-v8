"""
6D Legal Logic Framework
Legal Advisory System v8.0

This module implements the six-dimensional decompositional structure for
representing legal knowledge as formal logic rather than natural language.

The 6D Framework:
- WHAT:     Core holdings, rules, or facts established
- WHICH:    Scope and applicability boundaries
- IF-THEN:  Conditional logic and consequences
- MODALITY: Obligations (MUST), permissions (MAY), prohibitions (SHALL NOT)
- GIVEN:    Prerequisites and assumptions
- WHY:      Rationale and policy considerations

This structure enables:
- Queryable legal logic
- Design-time validation by experts
- Multi-path reasoning
- Systematic verification
- Cross-domain reasoning

Based on: Formal legal reasoning theory + COLIEE competition design
"""

from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any
from enum import Enum
from datetime import datetime


class ModalityType(Enum):
    """
    Modal logic types for legal obligations and permissions.

    Based on deontic logic theory applied to law.
    """
    MUST = "MUST"           # Strict obligation (no discretion)
    SHALL = "SHALL"         # Legal obligation (formal)
    MAY = "MAY"             # Permission (discretionary)
    CAN = "CAN"             # Capability/possibility
    SHOULD = "SHOULD"       # Recommendation (not binding)
    SHALL_NOT = "SHALL_NOT" # Prohibition
    MUST_NOT = "MUST_NOT"   # Strict prohibition
    MAY_NOT = "MAY_NOT"     # No permission


class SourceType(Enum):
    """
    Legal source types with authority hierarchy.

    Authority weights:
    - Constitution: 1.0 (supreme law)
    - Statute: 1.0 (primary legislation)
    - Rule: 0.8 (subordinate legislation)
    - Appellate Case: 0.7 (binding precedent)
    - High Court Case: 0.6 (persuasive precedent)
    - Lower Court Case: 0.4 (minimal precedent value)
    """
    CONSTITUTION = ("CONSTITUTION", 1.0)
    STATUTE = ("STATUTE", 1.0)
    RULE = ("RULE", 0.8)
    APPELLATE_CASE = ("APPELLATE_CASE", 0.7)
    HIGH_COURT_CASE = ("HIGH_COURT_CASE", 0.6)
    LOWER_COURT_CASE = ("LOWER_COURT_CASE", 0.4)

    def __init__(self, label: str, weight: float):
        self.label = label
        self.weight = weight


@dataclass
class Proposition:
    """
    A single logical proposition.

    Used for WHAT, WHICH, GIVEN, and WHY dimensions.

    Example:
        Proposition(
            text="The court may enter default judgment",
            confidence=1.0,
            source_line="Order 21 Rule 1(1)"
        )
    """
    text: str
    confidence: float = 1.0  # 0.0 to 1.0
    source_line: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)

    def __str__(self) -> str:
        return f"{self.text} (confidence: {self.confidence:.2f})"


@dataclass
class Conditional:
    """
    IF-THEN conditional logic.

    Represents legal conditionals: "IF condition met, THEN consequence follows"

    Example:
        Conditional(
            condition="defendant fails to file defense within time",
            consequence="plaintiff may apply for default judgment",
            exceptions=["if defendant obtains leave to file late defense"]
        )
    """
    condition: str  # The IF part
    consequence: str  # The THEN part
    exceptions: List[str] = field(default_factory=list)
    confidence: float = 1.0
    source_line: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)

    def __str__(self) -> str:
        base = f"IF {self.condition} THEN {self.consequence}"
        if self.exceptions:
            base += f" (EXCEPT: {', '.join(self.exceptions)})"
        return base


@dataclass
class Modality:
    """
    Modal logic for obligations and permissions.

    Captures MUST/MAY/SHALL distinctions critical to legal reasoning.

    Example:
        Modality(
            action="serve notice of application on defendant",
            modality_type=ModalityType.MUST,
            conditions=["before applying for default judgment"]
        )
    """
    action: str
    modality_type: ModalityType
    conditions: List[str] = field(default_factory=list)
    confidence: float = 1.0
    source_line: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)

    def __str__(self) -> str:
        base = f"{self.modality_type.value} {self.action}"
        if self.conditions:
            base += f" (when: {', '.join(self.conditions)})"
        return base


@dataclass
class LegalLogicNode:
    """
    6D Legal Logic Node

    Represents a formal legal proposition with six deductive dimensions.

    This is the fundamental unit of legal knowledge in the system.
    Each node captures:
    - Complete logical structure (6 dimensions)
    - Authority and provenance
    - Relationships to other nodes
    - Temporal validity

    Example:
        Order 21 Rule 1(1) node:
        - WHAT: Default judgment may be entered
        - WHICH: Against defendant who fails to file defense
        - IF-THEN: IF no defense filed THEN may enter judgment
        - MODALITY: Plaintiff MAY apply for judgment
        - GIVEN: Service was properly effected
        - WHY: To prevent defendants from delaying proceedings
    """

    # ========== Identification ==========
    node_id: str  # Unique identifier, e.g., "order21_rule1_para1"
    citation: str  # Legal citation, e.g., "Order 21 Rule 1(1)"
    source_type: SourceType

    # ========== 6D Logic Dimensions ==========
    what: List[Proposition] = field(default_factory=list)  # Holdings/rules/facts
    which: List[Proposition] = field(default_factory=list)  # Scope/boundaries
    if_then: List[Conditional] = field(default_factory=list)  # Conditionals
    can_must: List[Modality] = field(default_factory=list)  # Obligations/permissions
    given: List[Proposition] = field(default_factory=list)  # Prerequisites
    why: List[Proposition] = field(default_factory=list)  # Rationale/policy

    # ========== Tree Structure (Vertical) ==========
    parent_id: Optional[str] = None
    children_ids: List[str] = field(default_factory=list)

    # ========== Legal Relationships (Horizontal) ==========
    interprets_ids: List[str] = field(default_factory=list)  # Cases interpreting this
    extends_ids: List[str] = field(default_factory=list)  # Extensions/elaborations
    overruled_by_ids: List[str] = field(default_factory=list)  # Superseded by
    distinguishes_ids: List[str] = field(default_factory=list)  # Distinguished from
    conflicts_with_ids: List[str] = field(default_factory=list)  # Contradicts
    harmonizes_with_ids: List[str] = field(default_factory=list)  # Reconciles with

    # ========== Temporal Validity ==========
    effective_date: Optional[datetime] = None
    overruled_date: Optional[datetime] = None
    amendment_history: List[Dict[str, Any]] = field(default_factory=list)

    # ========== Full Text (for search) ==========
    full_text: str = ""

    # ========== Metadata ==========
    module_id: str = ""  # Which module this belongs to, e.g., "order_21"
    version: str = "1.0.0"
    validated_by: Optional[str] = None  # Legal expert who validated this
    validated_date: Optional[datetime] = None
    metadata: Dict[str, Any] = field(default_factory=dict)

    def get_authority_weight(self) -> float:
        """Get authority weight based on source type."""
        return self.source_type.weight

    def is_currently_valid(self) -> bool:
        """Check if this node is currently valid law."""
        now = datetime.now()

        # Not yet effective
        if self.effective_date and self.effective_date > now:
            return False

        # Already overruled
        if self.overruled_date and self.overruled_date <= now:
            return False

        return True

    def get_all_relationships(self) -> Dict[str, List[str]]:
        """Get all relationship IDs organized by type."""
        return {
            "parent": [self.parent_id] if self.parent_id else [],
            "children": self.children_ids,
            "interprets": self.interprets_ids,
            "extends": self.extends_ids,
            "overruled_by": self.overruled_by_ids,
            "distinguishes": self.distinguishes_ids,
            "conflicts_with": self.conflicts_with_ids,
            "harmonizes_with": self.harmonizes_with_ids
        }

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization."""
        return {
            "node_id": self.node_id,
            "citation": self.citation,
            "source_type": self.source_type.label,
            "authority_weight": self.get_authority_weight(),

            # 6D dimensions
            "what": [{"text": p.text, "confidence": p.confidence, "source_line": p.source_line}
                     for p in self.what],
            "which": [{"text": p.text, "confidence": p.confidence, "source_line": p.source_line}
                      for p in self.which],
            "if_then": [{"condition": c.condition, "consequence": c.consequence,
                         "exceptions": c.exceptions, "confidence": c.confidence,
                         "source_line": c.source_line}
                        for c in self.if_then],
            "can_must": [{"action": m.action, "modality": m.modality_type.value,
                          "conditions": m.conditions, "confidence": m.confidence,
                          "source_line": m.source_line}
                         for m in self.can_must],
            "given": [{"text": p.text, "confidence": p.confidence, "source_line": p.source_line}
                      for p in self.given],
            "why": [{"text": p.text, "confidence": p.confidence, "source_line": p.source_line}
                    for p in self.why],

            # Relationships
            "parent_id": self.parent_id,
            "children_ids": self.children_ids,
            "interprets_ids": self.interprets_ids,
            "extends_ids": self.extends_ids,
            "overruled_by_ids": self.overruled_by_ids,
            "distinguishes_ids": self.distinguishes_ids,
            "conflicts_with_ids": self.conflicts_with_ids,
            "harmonizes_with_ids": self.harmonizes_with_ids,

            # Temporal
            "effective_date": self.effective_date.isoformat() if self.effective_date else None,
            "overruled_date": self.overruled_date.isoformat() if self.overruled_date else None,
            "is_valid": self.is_currently_valid(),

            # Other
            "full_text": self.full_text,
            "module_id": self.module_id,
            "version": self.version,
            "validated_by": self.validated_by,
            "validated_date": self.validated_date.isoformat() if self.validated_date else None,
            "metadata": self.metadata
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'LegalLogicNode':
        """Create from dictionary."""
        # Parse source type
        source_type = SourceType[data["source_type"]]

        # Parse 6D dimensions
        what = [Proposition(**p) for p in data.get("what", [])]
        which = [Proposition(**p) for p in data.get("which", [])]
        if_then = [Conditional(**c) for c in data.get("if_then", [])]
        can_must = [Modality(
            action=m["action"],
            modality_type=ModalityType[m["modality"]],
            conditions=m.get("conditions", []),
            confidence=m.get("confidence", 1.0),
            source_line=m.get("source_line")
        ) for m in data.get("can_must", [])]
        given = [Proposition(**p) for p in data.get("given", [])]
        why = [Proposition(**p) for p in data.get("why", [])]

        # Parse dates
        effective_date = datetime.fromisoformat(data["effective_date"]) if data.get("effective_date") else None
        overruled_date = datetime.fromisoformat(data["overruled_date"]) if data.get("overruled_date") else None
        validated_date = datetime.fromisoformat(data["validated_date"]) if data.get("validated_date") else None

        return cls(
            node_id=data["node_id"],
            citation=data["citation"],
            source_type=source_type,
            what=what,
            which=which,
            if_then=if_then,
            can_must=can_must,
            given=given,
            why=why,
            parent_id=data.get("parent_id"),
            children_ids=data.get("children_ids", []),
            interprets_ids=data.get("interprets_ids", []),
            extends_ids=data.get("extends_ids", []),
            overruled_by_ids=data.get("overruled_by_ids", []),
            distinguishes_ids=data.get("distinguishes_ids", []),
            conflicts_with_ids=data.get("conflicts_with_ids", []),
            harmonizes_with_ids=data.get("harmonizes_with_ids", []),
            effective_date=effective_date,
            overruled_date=overruled_date,
            full_text=data.get("full_text", ""),
            module_id=data.get("module_id", ""),
            version=data.get("version", "1.0.0"),
            validated_by=data.get("validated_by"),
            validated_date=validated_date,
            metadata=data.get("metadata", {})
        )

    def __str__(self) -> str:
        return f"LegalLogicNode({self.citation})"

    def __repr__(self) -> str:
        return f"<LegalLogicNode node_id={self.node_id} citation={self.citation} weight={self.get_authority_weight():.2f}>"


# Convenience functions for creating nodes

def create_simple_node(
    node_id: str,
    citation: str,
    source_type: SourceType,
    what_text: str,
    module_id: str = ""
) -> LegalLogicNode:
    """
    Create a simple node with just WHAT dimension.

    Useful for quick prototyping or simple rules.
    """
    return LegalLogicNode(
        node_id=node_id,
        citation=citation,
        source_type=source_type,
        what=[Proposition(text=what_text)],
        module_id=module_id
    )


def create_conditional_node(
    node_id: str,
    citation: str,
    source_type: SourceType,
    condition: str,
    consequence: str,
    module_id: str = ""
) -> LegalLogicNode:
    """
    Create a node focused on IF-THEN logic.

    Useful for procedural rules.
    """
    return LegalLogicNode(
        node_id=node_id,
        citation=citation,
        source_type=source_type,
        if_then=[Conditional(condition=condition, consequence=consequence)],
        module_id=module_id
    )


def create_obligation_node(
    node_id: str,
    citation: str,
    source_type: SourceType,
    action: str,
    modality_type: ModalityType,
    module_id: str = ""
) -> LegalLogicNode:
    """
    Create a node focused on obligations/permissions.

    Useful for duty-imposing rules.
    """
    return LegalLogicNode(
        node_id=node_id,
        citation=citation,
        source_type=source_type,
        can_must=[Modality(action=action, modality_type=modality_type)],
        module_id=module_id
    )


if __name__ == "__main__":
    # Example: Create Order 21 Rule 1 node

    node = LegalLogicNode(
        node_id="order21_rule1_para1",
        citation="Order 21 Rule 1(1)",
        source_type=SourceType.RULE,
        module_id="order_21",

        what=[
            Proposition(
                text="Default judgment may be entered against defendant",
                source_line="Order 21 Rule 1(1)"
            )
        ],

        which=[
            Proposition(
                text="Applies to defendants who fail to file defense or acknowledgment",
                source_line="Order 21 Rule 1(1)"
            )
        ],

        if_then=[
            Conditional(
                condition="defendant fails to file defense within prescribed time",
                consequence="plaintiff may apply for default judgment",
                exceptions=["if leave to file late defense is granted"],
                source_line="Order 21 Rule 1(1)"
            )
        ],

        can_must=[
            Modality(
                action="apply for default judgment",
                modality_type=ModalityType.MAY,
                conditions=["after time for filing defense has expired"],
                source_line="Order 21 Rule 1(1)"
            ),
            Modality(
                action="serve notice of application on defendant",
                modality_type=ModalityType.MUST,
                conditions=["before obtaining default judgment"],
                source_line="Order 21 Rule 3"
            )
        ],

        given=[
            Proposition(
                text="Service of writ was properly effected",
                source_line="Order 10"
            ),
            Proposition(
                text="Time for filing defense has expired",
                source_line="Order 18 Rule 2"
            )
        ],

        why=[
            Proposition(
                text="To prevent defendants from delaying proceedings indefinitely",
                source_line="Practice Directions"
            ),
            Proposition(
                text="To provide remedy when defendant shows no intention to defend",
                source_line="Case law"
            )
        ],

        full_text="Where a defendant to an action has failed to file a defence or acknowledgment of service within the prescribed time, the plaintiff may apply for judgment in default of defence.",

        validated_by="Senior Counsel John Doe",
        validated_date=datetime.now()
    )

    print("=" * 70)
    print("6D Legal Logic Node Example")
    print("=" * 70)
    print()
    print(f"Node: {node.citation}")
    print(f"Authority Weight: {node.get_authority_weight()}")
    print(f"Currently Valid: {node.is_currently_valid()}")
    print()

    print("WHAT (Holdings):")
    for p in node.what:
        print(f"  - {p}")
    print()

    print("WHICH (Scope):")
    for p in node.which:
        print(f"  - {p}")
    print()

    print("IF-THEN (Conditionals):")
    for c in node.if_then:
        print(f"  - {c}")
    print()

    print("CAN/MUST (Modalities):")
    for m in node.can_must:
        print(f"  - {m}")
    print()

    print("GIVEN (Prerequisites):")
    for p in node.given:
        print(f"  - {p}")
    print()

    print("WHY (Rationale):")
    for p in node.why:
        print(f"  - {p}")
    print()

    # Test serialization
    print("=" * 70)
    print("Serialization Test")
    print("=" * 70)

    node_dict = node.to_dict()
    print(f"Serialized to dict: {len(node_dict)} keys")

    node_restored = LegalLogicNode.from_dict(node_dict)
    print(f"Restored from dict: {node_restored.citation}")
    print(f"Match: {node.node_id == node_restored.node_id}")
