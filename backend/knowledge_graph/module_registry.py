"""
Module Registry and Query Router
Legal Advisory System v8.0

The Module Registry is the central coordinator for all legal logic tree modules.

Responsibilities:
- Module registration and discovery
- Query routing (which modules to query for a given question)
- Module health monitoring
- Cross-module dependency management

This is the "brain" of the modular architecture that determines:
"Given query X, which modules (Order 21, Companies Act, etc.) should process it?"

Architecture:
    User Query
        ↓
    Query Router (analyzes query)
        ↓
    Module Registry (finds relevant modules)
        ↓
    [Order 21] [Order 5] [Companies Act] ... (parallel execution)
        ↓
    Results Aggregator
        ↓
    Final Answer
"""

from typing import List, Dict, Optional, Set, Any
from dataclasses import dataclass, field
from collections import defaultdict
import re
import logging

from logic_tree_module import (
    LogicTreeModule,
    ModuleMetadata,
    SearchResult,
    ReasoningResult
)

logger = logging.getLogger(__name__)


@dataclass
class QueryIntent:
    """
    Parsed query intent.

    The router extracts:
    - Topics (e.g., "default_judgment", "costs")
    - Question type (WHAT, IF_THEN, CAN_MUST, etc.)
    - Entities (courts, amounts, dates)
    - Relevant modules to query
    """
    raw_query: str
    topics: List[str] = field(default_factory=list)
    question_type: str = "WHAT"  # WHAT, WHICH, IF_THEN, CAN_MUST, GIVEN, WHY
    entities: Dict[str, Any] = field(default_factory=dict)
    relevant_modules: List[str] = field(default_factory=list)  # Module IDs
    confidence: float = 0.0  # How confident are we in the routing?


class QueryRouter:
    """
    Analyzes queries and determines which modules to route to.

    Uses:
    - Keyword matching against module coverage
    - Legal taxonomy mapping
    - Entity extraction (courts, amounts, etc.)
    - Question classification (6D types)

    Example:
        query = "Can I get default judgment if defendant is overseas?"

        Router extracts:
        - Topics: ["default_judgment", "overseas_service"]
        - Question type: "CAN_MUST" (asking about permission)
        - Entities: {"defendant_location": "overseas"}
        - Relevant modules: ["order_21", "order_11"]
    """

    def __init__(self, registry: 'ModuleRegistry'):
        self.registry = registry

        # Legal taxonomy - maps terms to topics
        self.taxonomy = self._build_legal_taxonomy()

        # Question type patterns
        self.question_patterns = self._build_question_patterns()

    def analyze_query(self, query: str) -> QueryIntent:
        """
        Analyze query and determine routing intent.

        Args:
            query: Natural language legal question

        Returns:
            QueryIntent with topics, question type, and relevant modules
        """
        # Extract topics
        topics = self._extract_topics(query)

        # Classify question type
        question_type = self._classify_question_type(query)

        # Extract entities
        entities = self._extract_entities(query)

        # Find relevant modules
        relevant_modules = self._find_modules_for_topics(topics)

        # Calculate confidence
        confidence = self._calculate_routing_confidence(topics, relevant_modules)

        return QueryIntent(
            raw_query=query,
            topics=topics,
            question_type=question_type,
            entities=entities,
            relevant_modules=relevant_modules,
            confidence=confidence
        )

    def _extract_topics(self, query: str) -> List[str]:
        """
        Extract legal topics from query.

        Uses keyword matching against legal taxonomy.
        """
        query_lower = query.lower()
        topics = []

        for topic, keywords in self.taxonomy.items():
            # Check if any keyword matches
            if any(keyword in query_lower for keyword in keywords):
                topics.append(topic)

        return topics

    def _classify_question_type(self, query: str) -> str:
        """
        Classify into 6D question type.

        Returns: WHAT, WHICH, IF_THEN, CAN_MUST, GIVEN, or WHY
        """
        query_lower = query.lower()

        for q_type, patterns in self.question_patterns.items():
            for pattern in patterns:
                if re.search(pattern, query_lower):
                    return q_type

        return "WHAT"  # Default

    def _extract_entities(self, query: str) -> Dict[str, Any]:
        """
        Extract legal entities from query.

        Entities include:
        - Courts (High Court, District Court, etc.)
        - Amounts ($50,000)
        - Dates (within 14 days)
        - Parties (plaintiff, defendant)
        """
        entities = {}

        # Extract courts
        court_patterns = {
            "High Court": r"high\s+court|hc|sghc",
            "District Court": r"district\s+court|dc|sgdc",
            "Magistrate Court": r"magistrate|mc|sgmc",
            "Court of Appeal": r"court\s+of\s+appeal|ca|sgca"
        }

        for court, pattern in court_patterns.items():
            if re.search(pattern, query, re.IGNORECASE):
                entities["court"] = court
                break

        # Extract amounts
        amount_match = re.search(r'\$?([\d,]+)', query)
        if amount_match:
            amount_str = amount_match.group(1).replace(',', '')
            try:
                entities["amount"] = float(amount_str)
            except ValueError:
                pass

        # Extract time periods
        time_match = re.search(r'(\d+)\s+(days?|weeks?|months?)', query, re.IGNORECASE)
        if time_match:
            entities["time_period"] = {
                "value": int(time_match.group(1)),
                "unit": time_match.group(2).lower()
            }

        return entities

    def _find_modules_for_topics(self, topics: List[str]) -> List[str]:
        """
        Map topics to module IDs.

        Uses the registry's topic index to find modules covering these topics.
        """
        return self.registry.get_modules_by_topics(topics)

    def _calculate_routing_confidence(
        self,
        topics: List[str],
        modules: List[str]
    ) -> float:
        """
        Calculate confidence in routing decision.

        High confidence if:
        - Clear topics extracted
        - Modules found for all topics
        - Keywords match exactly

        Low confidence if:
        - Few topics extracted
        - No modules found
        - Ambiguous keywords
        """
        if not topics:
            return 0.0

        if not modules:
            return 0.2  # Topics found but no modules

        # Higher confidence with more topics and modules
        topic_score = min(len(topics) / 3.0, 1.0)  # 3+ topics = full score
        module_score = min(len(modules) / 2.0, 1.0)  # 2+ modules = full score

        return (topic_score + module_score) / 2.0

    def _build_legal_taxonomy(self) -> Dict[str, List[str]]:
        """
        Build mapping of legal topics to keywords.

        This is the "knowledge" that maps natural language to legal domains.
        """
        return {
            # Civil Procedure
            "default_judgment": [
                "default", "judgment", "no defense", "didn't respond",
                "failed to file", "no response"
            ],
            "summary_judgment": [
                "summary", "no triable issue", "no real prospect",
                "summary disposal"
            ],
            "costs": [
                "costs", "fees", "charges", "expenses", "legal fees",
                "party and party costs", "indemnity costs"
            ],
            "service": [
                "service", "serve", "serving documents", "delivery"
            ],
            "overseas_service": [
                "overseas", "abroad", "foreign", "out of jurisdiction",
                "outside singapore"
            ],
            "setting_aside": [
                "set aside", "setting aside", "aside", "overturn", "reverse"
            ],
            "appeals": [
                "appeal", "appellate", "review", "challenge decision"
            ],

            # Corporate Law
            "directors_duties": [
                "director", "fiduciary duty", "directors duty",
                "breach of duty", "conflict of interest"
            ],
            "insolvency": [
                "insolvent", "insolvency", "winding up", "liquidation",
                "bankruptcy", "judicial management"
            ],
            "shareholders": [
                "shareholder", "minority shareholder", "oppression",
                "unfair prejudice"
            ],

            # Contract Law
            "breach_of_contract": [
                "breach", "contract", "breach of contract", "violation",
                "non-performance"
            ],
            "damages": [
                "damages", "compensation", "loss", "remedy"
            ],

            # Court Levels
            "high_court_jurisdiction": [
                "high court jurisdiction", "hc", "sghc"
            ],
            "district_court_jurisdiction": [
                "district court jurisdiction", "dc", "sgdc"
            ]
        }

    def _build_question_patterns(self) -> Dict[str, List[str]]:
        """
        Build patterns for classifying question types.

        Maps to 6D dimensions.
        """
        return {
            "WHAT": [
                r"\bwhat\s+(is|are|does)\b",
                r"\bdefine\b",
                r"\bexplain\b",
                r"\btell\s+me\s+about\b"
            ],
            "WHICH": [
                r"\bwhich\b",
                r"\bwho\b",
                r"\bwhen\b",
                r"\bwhere\b"
            ],
            "IF_THEN": [
                r"\bif\b.*\bthen\b",
                r"\bwhen\b.*\bhappens\b",
                r"\bwhat\s+happens\s+if\b",
                r"\bconsequence\b"
            ],
            "CAN_MUST": [
                r"\bcan\s+i\b",
                r"\bmay\s+i\b",
                r"\bmust\s+i\b",
                r"\bshall\s+i\b",
                r"\bam\s+i\s+(required|allowed|permitted|obliged)\b",
                r"\bdo\s+i\s+have\s+to\b"
            ],
            "GIVEN": [
                r"\bgiven\s+that\b",
                r"\bassuming\b",
                r"\bsuppose\b",
                r"\bif\s+(the|a|an)\b"
            ],
            "WHY": [
                r"\bwhy\b",
                r"\breason\b",
                r"\brationale\b",
                r"\bpurpose\b",
                r"\bwhy\s+does\b"
            ]
        }


class ModuleRegistry:
    """
    Central registry for all legal logic tree modules.

    Manages:
    - Module registration and discovery
    - Topic indexing (which modules cover which topics)
    - Query routing
    - Module lifecycle

    Example:
        registry = ModuleRegistry()
        registry.register_module(order21_module)
        registry.register_module(companies_act_module)

        # Route query
        modules = registry.find_relevant_modules("Can I get default judgment?")
        # Returns: [order21_module]
    """

    def __init__(self):
        self.modules: Dict[str, LogicTreeModule] = {}
        self.metadata_index: Dict[str, ModuleMetadata] = {}
        self.topic_index: Dict[str, List[str]] = defaultdict(list)  # topic → module_ids
        self.keyword_index: Dict[str, List[str]] = defaultdict(list)  # keyword → module_ids
        self.router = QueryRouter(self)

    def register_module(self, module: LogicTreeModule) -> None:
        """
        Register a new module.

        Args:
            module: LogicTreeModule instance to register

        This:
        - Initializes the module (loads nodes)
        - Indexes by topics and keywords
        - Makes module available for querying
        """
        # Initialize module
        module.initialize()

        # Get metadata
        metadata = module.get_metadata()
        module_id = metadata.module_id

        # Store module
        self.modules[module_id] = module
        self.metadata_index[module_id] = metadata

        # Index by topics
        for topic in metadata.coverage.topics:
            self.topic_index[topic].append(module_id)

        # Index by keywords
        for keyword in metadata.coverage.keywords:
            self.keyword_index[keyword.lower()].append(module_id)

        logger.info(f"Registered module: {module_id} ({len(module.nodes)} nodes)")

    def unregister_module(self, module_id: str) -> None:
        """
        Unregister a module.

        Args:
            module_id: ID of module to remove
        """
        if module_id not in self.modules:
            return

        # Remove from indexes
        metadata = self.metadata_index[module_id]

        for topic in metadata.coverage.topics:
            if module_id in self.topic_index[topic]:
                self.topic_index[topic].remove(module_id)

        for keyword in metadata.coverage.keywords:
            if module_id in self.keyword_index[keyword.lower()]:
                self.keyword_index[keyword.lower()].remove(module_id)

        # Remove module
        del self.modules[module_id]
        del self.metadata_index[module_id]

        logger.info(f"Unregistered module: {module_id}")

    def get_module(self, module_id: str) -> Optional[LogicTreeModule]:
        """Get module by ID."""
        return self.modules.get(module_id)

    def get_all_modules(self) -> List[LogicTreeModule]:
        """Get all registered modules."""
        return list(self.modules.values())

    def get_modules_by_topics(self, topics: List[str]) -> List[str]:
        """
        Get module IDs covering given topics.

        Args:
            topics: List of topic strings

        Returns:
            List of module IDs (deduplicated and sorted by coverage)
        """
        module_scores: Dict[str, int] = defaultdict(int)

        for topic in topics:
            for module_id in self.topic_index.get(topic, []):
                module_scores[module_id] += 1

        # Sort by score (how many topics matched)
        sorted_modules = sorted(
            module_scores.items(),
            key=lambda x: x[1],
            reverse=True
        )

        return [module_id for module_id, score in sorted_modules]

    def find_relevant_modules(
        self,
        query: str,
        max_modules: int = 5
    ) -> List[LogicTreeModule]:
        """
        Find modules relevant to a query.

        Args:
            query: Natural language query
            max_modules: Maximum number of modules to return

        Returns:
            List of LogicTreeModule instances, sorted by relevance
        """
        # Analyze query
        intent = self.router.analyze_query(query)

        # Get modules
        modules = [
            self.modules[module_id]
            for module_id in intent.relevant_modules[:max_modules]
            if module_id in self.modules
        ]

        return modules

    def route_query(self, query: str) -> QueryIntent:
        """
        Route query to appropriate modules.

        Args:
            query: Natural language query

        Returns:
            QueryIntent with modules to query
        """
        return self.router.analyze_query(query)

    def get_statistics(self) -> Dict[str, Any]:
        """
        Get registry statistics.

        Returns:
            Dictionary with counts and coverage info
        """
        total_modules = len(self.modules)
        total_nodes = sum(len(m.nodes) for m in self.modules.values())
        total_topics = len(self.topic_index)

        # Get module breakdown
        module_stats = {}
        for module_id, module in self.modules.items():
            module_stats[module_id] = {
                "nodes": len(module.nodes),
                "topics": len(self.metadata_index[module_id].coverage.topics),
                "version": self.metadata_index[module_id].version
            }

        return {
            "total_modules": total_modules,
            "total_nodes": total_nodes,
            "total_topics": total_topics,
            "modules": module_stats,
            "topic_coverage": {
                topic: len(modules)
                for topic, modules in self.topic_index.items()
            }
        }

    def __repr__(self) -> str:
        return f"<ModuleRegistry modules={len(self.modules)} topics={len(self.topic_index)}>"


if __name__ == "__main__":
    # Example usage

    from logic_tree_module import LogicTreeModule, ModuleCoverage
    from six_dimensions import LegalLogicNode, SourceType, Proposition
    from datetime import datetime

    # Create test modules
    class Order21Module(LogicTreeModule):
        def get_metadata(self) -> ModuleMetadata:
            return ModuleMetadata(
                module_id="order_21",
                name="Order 21 - Default Judgment",
                version="1.0.0",
                coverage=ModuleCoverage(
                    statute="Civil Procedure Rules",
                    sections=["Order 21"],
                    topics=["default_judgment", "costs"],
                    keywords=["default", "judgment", "no defense"]
                ),
                authority_weight=0.8,
                effective_date=datetime.now()
            )

        def load_nodes(self) -> Dict[str, LegalLogicNode]:
            node = LegalLogicNode(
                node_id="order21_rule1",
                citation="Order 21 Rule 1",
                source_type=SourceType.RULE,
                what=[Proposition(text="Default judgment may be entered")],
                module_id="order_21"
            )
            return {"order21_rule1": node}

        def search(self, query: str, filters=None, top_k=10) -> List[SearchResult]:
            return []

        def reason(self, question: str) -> ReasoningResult:
            return ReasoningResult(conclusion="Test", confidence=0.7, reasoning_chain=[])

    class Order5Module(LogicTreeModule):
        def get_metadata(self) -> ModuleMetadata:
            return ModuleMetadata(
                module_id="order_5",
                name="Order 5 - ADR",
                version="1.0.0",
                coverage=ModuleCoverage(
                    statute="Civil Procedure Rules",
                    sections=["Order 5"],
                    topics=["mediation", "adr"],
                    keywords=["mediation", "alternative dispute"]
                ),
                authority_weight=0.8,
                effective_date=datetime.now()
            )

        def load_nodes(self) -> Dict[str, LegalLogicNode]:
            node = LegalLogicNode(
                node_id="order5_rule1",
                citation="Order 5 Rule 1",
                source_type=SourceType.RULE,
                what=[Proposition(text="Court may order mediation")],
                module_id="order_5"
            )
            return {"order5_rule1": node}

        def search(self, query: str, filters=None, top_k=10) -> List[SearchResult]:
            return []

        def reason(self, question: str) -> ReasoningResult:
            return ReasoningResult(conclusion="Test", confidence=0.7, reasoning_chain=[])

    # Test registry
    print("=" * 70)
    print("Module Registry - Example")
    print("=" * 70)
    print()

    registry = ModuleRegistry()

    # Register modules
    registry.register_module(Order21Module())
    registry.register_module(Order5Module())

    print(f"Registry: {registry}")
    print()

    # Test query routing
    test_queries = [
        "Can I get default judgment if defendant didn't respond?",
        "What are the rules for mediation?",
        "How much does default judgment cost?"
    ]

    for query in test_queries:
        print(f"Query: {query}")
        intent = registry.route_query(query)
        print(f"  Topics: {intent.topics}")
        print(f"  Question Type: {intent.question_type}")
        print(f"  Modules: {intent.relevant_modules}")
        print(f"  Confidence: {intent.confidence:.2f}")
        print()

    # Statistics
    stats = registry.get_statistics()
    print("Registry Statistics:")
    for key, value in stats.items():
        if key != "modules":
            print(f"  {key}: {value}")
