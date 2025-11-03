"""
Logic Tree Module Base Class
Legal Advisory System v8.0

This module defines the base class for all legal logic tree modules.

Each legal domain (Order 21, Companies Act, etc.) extends this base class
to create a self-contained, independently deployable module.

Architecture:
- Each module has its own logic tree (6D nodes)
- Modules are independently versioned and validated
- Modules expose standard interface for:
  * Searching within the module
  * Reasoning using module's logic
  * Retrieving specific nodes
  * Getting metadata

This enables:
- Modular development (add Order 5 without touching Order 21)
- Independent scaling (scale high-demand modules)
- Fault isolation (one module failure doesn't break system)
- Flexible deployment (microservices architecture)
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any
from datetime import datetime
import json
from pathlib import Path

from six_dimensions import LegalLogicNode, SourceType


@dataclass
class ModuleCoverage:
    """
    What legal topics this module covers.

    Used by the router to determine which modules to query.
    """
    statute: str  # e.g., "Civil Procedure Rules"
    sections: List[str]  # e.g., ["Order 21 Rule 1-9"]
    topics: List[str]  # e.g., ["default_judgment", "costs"]
    keywords: List[str]  # e.g., ["default", "judgment", "no defense"]
    jurisdictions: List[str] = field(default_factory=lambda: ["Singapore"])


@dataclass
class ModuleMetadata:
    """
    Metadata about a logic tree module.

    This is used by the registry for:
    - Module discovery
    - Query routing
    - Version management
    - Dependency tracking
    """
    module_id: str  # Unique identifier, e.g., "order_21"
    name: str  # Human-readable name
    version: str  # Semantic version
    coverage: ModuleCoverage
    authority_weight: float  # Based on source type (0.0-1.0)
    effective_date: datetime
    dependencies: List[str] = field(default_factory=list)  # Other modules referenced
    description: str = ""
    maintainer: str = ""
    validated_by: Optional[str] = None
    validated_date: Optional[datetime] = None
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization."""
        return {
            "module_id": self.module_id,
            "name": self.name,
            "version": self.version,
            "coverage": {
                "statute": self.coverage.statute,
                "sections": self.coverage.sections,
                "topics": self.coverage.topics,
                "keywords": self.coverage.keywords,
                "jurisdictions": self.coverage.jurisdictions
            },
            "authority_weight": self.authority_weight,
            "effective_date": self.effective_date.isoformat(),
            "dependencies": self.dependencies,
            "description": self.description,
            "maintainer": self.maintainer,
            "validated_by": self.validated_by,
            "validated_date": self.validated_date.isoformat() if self.validated_date else None,
            "metadata": self.metadata
        }


@dataclass
class SearchResult:
    """
    Result from searching a module.

    Includes the node plus relevance score and reasoning path.
    """
    node: LegalLogicNode
    relevance_score: float  # 0.0-1.0
    reasoning_path: List[str] = field(default_factory=list)  # Node IDs from root to this node
    matched_dimension: str = ""  # Which dimension matched (WHAT, IF_THEN, etc.)
    matched_text: str = ""  # The actual text that matched


@dataclass
class ReasoningStep:
    """
    A single step in a logical reasoning chain.

    Example:
        "Given service was properly effected (Order 10)"
        "IF defendant fails to file defense (Order 18)"
        "THEN plaintiff MAY apply for default judgment (Order 21 Rule 1)"
    """
    node_id: str
    citation: str
    dimension: str  # WHAT, IF_THEN, GIVEN, etc.
    text: str
    authority_weight: float


@dataclass
class ReasoningResult:
    """
    Result of reasoning about a legal question.

    Includes:
    - The conclusion/answer
    - The reasoning chain (how we got there)
    - Confidence score
    - Alternative paths (if any)
    """
    conclusion: str
    confidence: float  # 0.0-1.0
    reasoning_chain: List[ReasoningStep]
    alternative_paths: List[List[ReasoningStep]] = field(default_factory=list)
    applicable_nodes: List[LegalLogicNode] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)


class LogicTreeModule(ABC):
    """
    Base class for all legal logic tree modules.

    Each legal domain (Order 21, Companies Act, etc.) extends this class.

    Required implementations:
    - get_metadata(): Return module information
    - load_nodes(): Load the logic tree nodes
    - search(): Search within this module
    - reason(): Answer questions using this module's logic

    Optional overrides:
    - traverse_tree(): Custom tree traversal
    - validate_node(): Custom validation logic
    """

    def __init__(self, data_dir: Optional[Path] = None):
        """
        Initialize the module.

        Args:
            data_dir: Directory containing module data files
                     (nodes.json, relationships.json, metadata.json)
        """
        self.data_dir = data_dir
        self.nodes: Dict[str, LegalLogicNode] = {}
        self.root_node_ids: List[str] = []
        self._initialized = False

    def initialize(self) -> None:
        """
        Initialize the module by loading all data.

        This is called once when the module is registered.
        """
        if self._initialized:
            return

        # Load nodes
        self.nodes = self.load_nodes()

        # Identify root nodes (no parent)
        self.root_node_ids = [
            node_id for node_id, node in self.nodes.items()
            if node.parent_id is None
        ]

        self._initialized = True

    # ========== Abstract Methods (Must Implement) ==========

    @abstractmethod
    def get_metadata(self) -> ModuleMetadata:
        """
        Return metadata about this module.

        This is used by the registry for routing and discovery.
        """
        pass

    @abstractmethod
    def load_nodes(self) -> Dict[str, LegalLogicNode]:
        """
        Load all logic tree nodes for this module.

        Returns:
            Dictionary mapping node_id -> LegalLogicNode

        This can load from:
        - JSON files
        - Database
        - Programmatic generation
        """
        pass

    @abstractmethod
    def search(
        self,
        query: str,
        filters: Optional[Dict[str, Any]] = None,
        top_k: int = 10
    ) -> List[SearchResult]:
        """
        Search for relevant nodes within this module.

        Args:
            query: Search query text
            filters: Optional filters (e.g., node_type, citation)
            top_k: Number of results to return

        Returns:
            List of SearchResult objects, ranked by relevance
        """
        pass

    @abstractmethod
    def reason(self, question: str) -> ReasoningResult:
        """
        Answer a legal question using this module's logic.

        Args:
            question: Legal question in natural language

        Returns:
            ReasoningResult with conclusion, reasoning chain, and confidence

        Example:
            question = "Can I get default judgment if defendant didn't respond?"
            result = module.reason(question)
            print(result.conclusion)  # "Yes, if..."
            print(result.reasoning_chain)  # [Step1, Step2, Step3]
        """
        pass

    # ========== Concrete Methods (Can Override) ==========

    def get_node(self, node_id: str) -> Optional[LegalLogicNode]:
        """
        Retrieve a specific node by ID.

        Args:
            node_id: Node identifier

        Returns:
            LegalLogicNode or None if not found
        """
        return self.nodes.get(node_id)

    def get_children(self, node_id: str) -> List[LegalLogicNode]:
        """
        Get all child nodes of a given node.

        Args:
            node_id: Parent node ID

        Returns:
            List of child nodes
        """
        node = self.get_node(node_id)
        if not node:
            return []

        return [
            self.nodes[child_id]
            for child_id in node.children_ids
            if child_id in self.nodes
        ]

    def get_parent(self, node_id: str) -> Optional[LegalLogicNode]:
        """
        Get the parent node of a given node.

        Args:
            node_id: Child node ID

        Returns:
            Parent node or None
        """
        node = self.get_node(node_id)
        if not node or not node.parent_id:
            return None

        return self.get_node(node.parent_id)

    def traverse_tree(
        self,
        start_node_id: str,
        direction: str = "down",
        max_depth: int = 10
    ) -> List[LegalLogicNode]:
        """
        Traverse the tree from a starting node.

        Args:
            start_node_id: Node to start from
            direction: "up" (to parents), "down" (to children), or "both"
            max_depth: Maximum depth to traverse

        Returns:
            List of nodes encountered during traversal
        """
        visited = []
        queue = [(start_node_id, 0)]  # (node_id, depth)
        seen = set()

        while queue:
            current_id, depth = queue.pop(0)

            if current_id in seen or depth > max_depth:
                continue

            seen.add(current_id)
            node = self.get_node(current_id)

            if not node:
                continue

            visited.append(node)

            # Add next nodes to queue
            if direction in ["down", "both"]:
                for child_id in node.children_ids:
                    queue.append((child_id, depth + 1))

            if direction in ["up", "both"] and node.parent_id:
                queue.append((node.parent_id, depth + 1))

        return visited

    def get_reasoning_path(
        self,
        start_node_id: str,
        end_node_id: str
    ) -> List[LegalLogicNode]:
        """
        Find the path between two nodes in the tree.

        Uses breadth-first search to find the shortest path.

        Args:
            start_node_id: Starting node
            end_node_id: Target node

        Returns:
            List of nodes forming the path (empty if no path exists)
        """
        if start_node_id == end_node_id:
            node = self.get_node(start_node_id)
            return [node] if node else []

        # BFS to find path
        queue = [(start_node_id, [start_node_id])]
        visited = set()

        while queue:
            current_id, path = queue.pop(0)

            if current_id in visited:
                continue

            visited.add(current_id)

            if current_id == end_node_id:
                # Found path - convert IDs to nodes
                return [self.get_node(nid) for nid in path if self.get_node(nid)]

            node = self.get_node(current_id)
            if not node:
                continue

            # Explore connections
            connections = []
            connections.extend(node.children_ids)
            if node.parent_id:
                connections.append(node.parent_id)
            connections.extend(node.interprets_ids)
            connections.extend(node.extends_ids)

            for next_id in connections:
                if next_id not in visited:
                    queue.append((next_id, path + [next_id]))

        return []  # No path found

    def validate_node(self, node: LegalLogicNode) -> List[str]:
        """
        Validate a node's structure and content.

        Args:
            node: Node to validate

        Returns:
            List of validation errors (empty if valid)
        """
        errors = []

        # Check required fields
        if not node.node_id:
            errors.append("Missing node_id")
        if not node.citation:
            errors.append("Missing citation")

        # Check at least one dimension is populated
        if not any([node.what, node.which, node.if_then, node.can_must, node.given, node.why]):
            errors.append("At least one 6D dimension must be populated")

        # Check parent exists
        if node.parent_id and node.parent_id not in self.nodes:
            errors.append(f"Parent node {node.parent_id} not found")

        # Check children exist
        for child_id in node.children_ids:
            if child_id not in self.nodes:
                errors.append(f"Child node {child_id} not found")

        return errors

    def get_statistics(self) -> Dict[str, Any]:
        """
        Get statistics about this module.

        Returns:
            Dictionary with counts, coverage, etc.
        """
        total_nodes = len(self.nodes)
        root_nodes = len(self.root_node_ids)

        # Count nodes by source type
        source_type_counts = {}
        for node in self.nodes.values():
            st = node.source_type.label
            source_type_counts[st] = source_type_counts.get(st, 0) + 1

        # Count dimensions populated
        dimension_counts = {
            "what": sum(1 for n in self.nodes.values() if n.what),
            "which": sum(1 for n in self.nodes.values() if n.which),
            "if_then": sum(1 for n in self.nodes.values() if n.if_then),
            "can_must": sum(1 for n in self.nodes.values() if n.can_must),
            "given": sum(1 for n in self.nodes.values() if n.given),
            "why": sum(1 for n in self.nodes.values() if n.why)
        }

        # Count relationships
        relationship_counts = {
            "parent_child": sum(1 for n in self.nodes.values() if n.parent_id),
            "interprets": sum(len(n.interprets_ids) for n in self.nodes.values()),
            "extends": sum(len(n.extends_ids) for n in self.nodes.values()),
            "overruled": sum(len(n.overruled_by_ids) for n in self.nodes.values())
        }

        return {
            "total_nodes": total_nodes,
            "root_nodes": root_nodes,
            "source_types": source_type_counts,
            "dimensions": dimension_counts,
            "relationships": relationship_counts
        }

    def __repr__(self) -> str:
        metadata = self.get_metadata()
        return f"<LogicTreeModule module_id={metadata.module_id} nodes={len(self.nodes)}>"


if __name__ == "__main__":
    # Example: Simple module implementation

    class SimpleTestModule(LogicTreeModule):
        """Test module for demonstration."""

        def get_metadata(self) -> ModuleMetadata:
            return ModuleMetadata(
                module_id="test_module",
                name="Test Module",
                version="1.0.0",
                coverage=ModuleCoverage(
                    statute="Test Act",
                    sections=["Section 1"],
                    topics=["testing"],
                    keywords=["test"]
                ),
                authority_weight=0.8,
                effective_date=datetime.now()
            )

        def load_nodes(self) -> Dict[str, LegalLogicNode]:
            # Create simple test nodes
            from six_dimensions import Proposition

            node1 = LegalLogicNode(
                node_id="test_001",
                citation="Test Act s.1",
                source_type=SourceType.STATUTE,
                what=[Proposition(text="This is a test rule")],
                module_id="test_module"
            )

            node2 = LegalLogicNode(
                node_id="test_002",
                citation="Test Act s.1(a)",
                source_type=SourceType.STATUTE,
                what=[Proposition(text="This is a sub-rule")],
                parent_id="test_001",
                module_id="test_module"
            )

            node1.children_ids = ["test_002"]

            return {"test_001": node1, "test_002": node2}

        def search(self, query: str, filters=None, top_k=10) -> List[SearchResult]:
            # Simple keyword search
            results = []
            for node in self.nodes.values():
                if query.lower() in node.full_text.lower():
                    results.append(SearchResult(
                        node=node,
                        relevance_score=0.8,
                        matched_dimension="WHAT"
                    ))
            return results[:top_k]

        def reason(self, question: str) -> ReasoningResult:
            # Simple reasoning: just return first node
            if self.nodes:
                first_node = list(self.nodes.values())[0]
                return ReasoningResult(
                    conclusion="Test conclusion",
                    confidence=0.7,
                    reasoning_chain=[
                        ReasoningStep(
                            node_id=first_node.node_id,
                            citation=first_node.citation,
                            dimension="WHAT",
                            text=first_node.what[0].text if first_node.what else "",
                            authority_weight=first_node.get_authority_weight()
                        )
                    ]
                )
            return ReasoningResult(conclusion="No answer", confidence=0.0, reasoning_chain=[])

    # Test the module
    print("=" * 70)
    print("Logic Tree Module - Example")
    print("=" * 70)
    print()

    module = SimpleTestModule()
    module.initialize()

    print(f"Module: {module.get_metadata().name}")
    print(f"Nodes loaded: {len(module.nodes)}")
    print()

    # Test node retrieval
    node = module.get_node("test_001")
    print(f"Retrieved node: {node.citation}")
    print(f"Children: {len(module.get_children('test_001'))}")
    print()

    # Test search
    results = module.search("test")
    print(f"Search results: {len(results)}")
    print()

    # Test reasoning
    result = module.reason("What is the test rule?")
    print(f"Reasoning result: {result.conclusion}")
    print(f"Confidence: {result.confidence}")
    print(f"Steps: {len(result.reasoning_chain)}")
    print()

    # Test statistics
    stats = module.get_statistics()
    print("Statistics:")
    for key, value in stats.items():
        print(f"  {key}: {value}")
