"""
BM25 Search Implementation for Legal Document Retrieval
Legal Advisory System v8.0

This module implements BM25-based search with legal-specific optimizations:
- Singapore legal synonyms expansion
- Multi-field filtering (node_type, court, order, case_type)
- Range queries (claim amounts, trial duration)
- Relevance highlighting
- Tuned BM25 parameters (k1=1.5, b=0.75)

Day 3 of Week 3 implementation.

Target: 62% retrieval accuracy (vs 30% baseline)
Based on: COLIEE 2023 competition specifications
"""

from typing import Dict, List, Any, Optional
from elasticsearch import Elasticsearch
from dataclasses import dataclass
import logging

logger = logging.getLogger(__name__)


@dataclass
class SearchFilters:
    """
    Filters for legal document search.

    All filters are optional and can be combined.
    """

    # 6D logic tree node types
    node_types: Optional[List[str]] = None  # WHAT, WHICH, IF_THEN, MODALITY, GIVEN, WHY

    # Legal metadata
    orders: Optional[List[str]] = None  # Order 21, Order 5, etc.
    rules: Optional[List[str]] = None  # Rule 1, Rule 2, etc.
    courts: Optional[List[str]] = None  # High Court, District Court, etc.
    case_types: Optional[List[str]] = None  # default_judgment, summary_judgment, etc.

    # Numerical ranges
    claim_amount_min: Optional[float] = None
    claim_amount_max: Optional[float] = None
    trial_days_min: Optional[int] = None
    trial_days_max: Optional[int] = None


@dataclass
class SearchResult:
    """
    A single search result from Elasticsearch.
    """

    node_id: str
    text: str
    score: float
    node_type: Optional[str] = None
    order: Optional[str] = None
    rule: Optional[str] = None
    court: Optional[str] = None
    case_type: Optional[str] = None
    claim_amount_min: Optional[float] = None
    claim_amount_max: Optional[float] = None
    trial_days_min: Optional[int] = None
    trial_days_max: Optional[int] = None
    highlights: Optional[List[str]] = None

    def __repr__(self) -> str:
        return f"SearchResult(node_id={self.node_id}, score={self.score:.4f}, text={self.text[:50]}...)"


class LegalBM25Search:
    """
    BM25-based search for legal documents with filtering.

    Features:
    - Full-text search using legal analyzer (with synonyms)
    - BM25 ranking (k1=1.5, b=0.75)
    - Multi-field filtering
    - Relevance highlighting
    - Pagination support
    """

    def __init__(self, es_url: str = "http://localhost:9200"):
        """
        Initialize the BM25 search engine.

        Args:
            es_url: Elasticsearch connection URL
        """
        self.es = Elasticsearch([es_url])
        self.index_name = "singapore_legal_v8"

        logger.info(f"Initialized BM25 search for index: {self.index_name}")

    def search(
        self,
        query: str,
        filters: Optional[SearchFilters] = None,
        top_k: int = 10,
        min_score: Optional[float] = None,
        enable_highlight: bool = True
    ) -> List[SearchResult]:
        """
        Search for legal documents using BM25.

        Args:
            query: Search query text
            filters: Optional filters to apply
            top_k: Number of results to return (default: 10)
            min_score: Minimum relevance score threshold (optional)
            enable_highlight: Whether to highlight matched terms

        Returns:
            List of SearchResult objects, sorted by relevance

        Example:
            >>> searcher = LegalBM25Search()
            >>> filters = SearchFilters(
            ...     node_types=["WHAT", "IF_THEN"],
            ...     courts=["High Court"],
            ...     claim_amount_min=10000
            ... )
            >>> results = searcher.search("default judgment costs", filters=filters, top_k=5)
            >>> for r in results:
            ...     print(f"{r.score:.2f} - {r.text[:100]}")
        """

        if not query.strip():
            logger.warning("Empty query provided")
            return []

        # Build Elasticsearch query
        es_query = self._build_query(query, filters, min_score, enable_highlight)

        try:
            # Execute search
            response = self.es.search(
                index=self.index_name,
                body=es_query,
                size=top_k
            )

            # Parse results
            results = self._parse_results(response)

            logger.info(f"Search query: '{query}' returned {len(results)} results")

            return results

        except Exception as e:
            logger.error(f"Search failed: {e}")
            return []

    def _build_query(
        self,
        query: str,
        filters: Optional[SearchFilters],
        min_score: Optional[float],
        enable_highlight: bool
    ) -> Dict[str, Any]:
        """
        Build the Elasticsearch query DSL.

        This creates a compound query with:
        1. Full-text search on 'text' field (BM25 with legal analyzer)
        2. Optional filters (must clauses)
        3. Optional minimum score threshold
        4. Optional highlighting
        """

        # Main query structure
        es_query: Dict[str, Any] = {
            "query": {
                "bool": {
                    "must": [
                        {
                            # BM25 full-text search with legal analyzer
                            "match": {
                                "text": {
                                    "query": query,
                                    "operator": "or"  # Match any term (default)
                                }
                            }
                        }
                    ]
                }
            }
        }

        # Add filters
        if filters:
            filter_clauses = self._build_filter_clauses(filters)
            if filter_clauses:
                es_query["query"]["bool"]["filter"] = filter_clauses

        # Add minimum score
        if min_score is not None:
            es_query["min_score"] = min_score

        # Add highlighting
        if enable_highlight:
            es_query["highlight"] = {
                "fields": {
                    "text": {
                        "pre_tags": ["<em>"],
                        "post_tags": ["</em>"],
                        "number_of_fragments": 3,
                        "fragment_size": 150
                    }
                }
            }

        return es_query

    def _build_filter_clauses(self, filters: SearchFilters) -> List[Dict[str, Any]]:
        """
        Build filter clauses from SearchFilters.

        Filters are applied as 'must' clauses (AND logic).
        """

        clauses = []

        # Node type filter (multi-value)
        if filters.node_types:
            clauses.append({
                "terms": {"node_type": filters.node_types}
            })

        # Order filter (multi-value)
        if filters.orders:
            clauses.append({
                "terms": {"order": filters.orders}
            })

        # Rule filter (multi-value)
        if filters.rules:
            clauses.append({
                "terms": {"rule": filters.rules}
            })

        # Court filter (multi-value)
        if filters.courts:
            clauses.append({
                "terms": {"court": filters.courts}
            })

        # Case type filter (multi-value)
        if filters.case_types:
            clauses.append({
                "terms": {"case_type": filters.case_types}
            })

        # Claim amount range
        if filters.claim_amount_min is not None or filters.claim_amount_max is not None:
            range_clause: Dict[str, Any] = {}

            if filters.claim_amount_min is not None:
                # Document's max claim must be >= filter's min
                range_clause["claim_amount_max"] = {"gte": filters.claim_amount_min}

            if filters.claim_amount_max is not None:
                # Document's min claim must be <= filter's max
                range_clause["claim_amount_min"] = {"lte": filters.claim_amount_max}

            for field, condition in range_clause.items():
                clauses.append({"range": {field: condition}})

        # Trial days range
        if filters.trial_days_min is not None or filters.trial_days_max is not None:
            range_clause = {}

            if filters.trial_days_min is not None:
                range_clause["trial_days_max"] = {"gte": filters.trial_days_min}

            if filters.trial_days_max is not None:
                range_clause["trial_days_min"] = {"lte": filters.trial_days_max}

            for field, condition in range_clause.items():
                clauses.append({"range": {field: condition}})

        return clauses

    def _parse_results(self, response: Dict[str, Any]) -> List[SearchResult]:
        """
        Parse Elasticsearch response into SearchResult objects.
        """

        results = []

        for hit in response['hits']['hits']:
            source = hit['_source']

            # Extract highlights if available
            highlights = None
            if 'highlight' in hit and 'text' in hit['highlight']:
                highlights = hit['highlight']['text']

            result = SearchResult(
                node_id=source.get('node_id', ''),
                text=source.get('text', ''),
                score=hit['_score'],
                node_type=source.get('node_type'),
                order=source.get('order'),
                rule=source.get('rule'),
                court=source.get('court'),
                case_type=source.get('case_type'),
                claim_amount_min=source.get('claim_amount_min'),
                claim_amount_max=source.get('claim_amount_max'),
                trial_days_min=source.get('trial_days_min'),
                trial_days_max=source.get('trial_days_max'),
                highlights=highlights
            )

            results.append(result)

        return results

    def multi_match_search(
        self,
        query: str,
        fields: List[str] = ["text", "citation"],
        filters: Optional[SearchFilters] = None,
        top_k: int = 10
    ) -> List[SearchResult]:
        """
        Search across multiple fields with boosting.

        Args:
            query: Search query
            fields: List of fields to search (can include boost, e.g. "text^2")
            filters: Optional filters
            top_k: Number of results

        Returns:
            List of SearchResult objects

        Example:
            >>> results = searcher.multi_match_search(
            ...     "default judgment",
            ...     fields=["text^2", "citation^1"]  # Boost text field 2x
            ... )
        """

        es_query: Dict[str, Any] = {
            "query": {
                "bool": {
                    "must": [
                        {
                            "multi_match": {
                                "query": query,
                                "fields": fields,
                                "type": "best_fields"  # Use best matching field
                            }
                        }
                    ]
                }
            }
        }

        # Add filters
        if filters:
            filter_clauses = self._build_filter_clauses(filters)
            if filter_clauses:
                es_query["query"]["bool"]["filter"] = filter_clauses

        try:
            response = self.es.search(
                index=self.index_name,
                body=es_query,
                size=top_k
            )

            return self._parse_results(response)

        except Exception as e:
            logger.error(f"Multi-match search failed: {e}")
            return []

    def get_stats(self) -> Dict[str, Any]:
        """
        Get search index statistics.

        Returns:
            Dictionary with index stats (doc count, size, etc.)
        """

        try:
            stats = self.es.indices.stats(index=self.index_name)

            doc_count = stats['indices'][self.index_name]['total']['docs']['count']
            size_bytes = stats['indices'][self.index_name]['total']['store']['size_in_bytes']

            return {
                "index_name": self.index_name,
                "document_count": doc_count,
                "size_mb": round(size_bytes / 1024 / 1024, 2)
            }

        except Exception as e:
            logger.error(f"Failed to get stats: {e}")
            return {"error": str(e)}


def main():
    """
    Demo script for Day 3: BM25 Search Function

    Tests various search scenarios:
    1. Simple text search
    2. Search with node_type filter
    3. Search with court filter
    4. Search with claim amount range
    5. Multi-field search
    """

    print("=" * 70)
    print("Legal Advisory v8.0 - BM25 Search Implementation")
    print("Week 3, Day 3: BM25 Search Function")
    print("=" * 70)
    print()

    # Initialize searcher
    searcher = LegalBM25Search()

    # Check index stats
    print("1. Index Statistics")
    print("-" * 70)
    stats = searcher.get_stats()
    print(f"   Index: {stats.get('index_name')}")
    print(f"   Documents: {stats.get('document_count', 0)}")
    print(f"   Size: {stats.get('size_mb', 0)} MB")
    print()

    # Test 1: Simple text search
    print("2. Simple Text Search")
    print("-" * 70)
    print("   Query: 'default judgment costs'")

    results = searcher.search("default judgment costs", top_k=5)

    if results:
        print(f"   Found {len(results)} results:\n")
        for i, r in enumerate(results, 1):
            print(f"   {i}. [Score: {r.score:.4f}] {r.node_id}")
            print(f"      {r.text[:100]}...")
            if r.highlights:
                print(f"      Highlights: {r.highlights[0][:80]}...")
            print()
    else:
        print("   ⚠️  No results (index may be empty)")
    print()

    # Test 2: Search with node_type filter
    print("3. Search with Node Type Filter")
    print("-" * 70)
    print("   Query: 'summary judgment'")
    print("   Filter: node_type = ['WHAT', 'IF_THEN']")

    filters = SearchFilters(node_types=["WHAT", "IF_THEN"])
    results = searcher.search("summary judgment", filters=filters, top_k=5)

    if results:
        print(f"   Found {len(results)} results:\n")
        for i, r in enumerate(results, 1):
            print(f"   {i}. [Score: {r.score:.4f}] {r.node_id} (Type: {r.node_type})")
            print(f"      {r.text[:100]}...")
            print()
    else:
        print("   ⚠️  No results (index may be empty or no matches)")
    print()

    # Test 3: Search with court filter
    print("4. Search with Court Filter")
    print("-" * 70)
    print("   Query: 'interlocutory application'")
    print("   Filter: court = ['High Court']")

    filters = SearchFilters(courts=["High Court"])
    results = searcher.search("interlocutory application", filters=filters, top_k=5)

    if results:
        print(f"   Found {len(results)} results:\n")
        for i, r in enumerate(results, 1):
            print(f"   {i}. [Score: {r.score:.4f}] {r.node_id} (Court: {r.court})")
            print(f"      {r.text[:100]}...")
            print()
    else:
        print("   ⚠️  No results (index may be empty or no matches)")
    print()

    # Test 4: Search with claim amount range
    print("5. Search with Claim Amount Range")
    print("-" * 70)
    print("   Query: 'costs assessment'")
    print("   Filter: claim_amount >= $10,000")

    filters = SearchFilters(claim_amount_min=10000.0)
    results = searcher.search("costs assessment", filters=filters, top_k=5)

    if results:
        print(f"   Found {len(results)} results:\n")
        for i, r in enumerate(results, 1):
            claim_range = ""
            if r.claim_amount_min or r.claim_amount_max:
                claim_range = f" (${r.claim_amount_min}-${r.claim_amount_max})"
            print(f"   {i}. [Score: {r.score:.4f}] {r.node_id}{claim_range}")
            print(f"      {r.text[:100]}...")
            print()
    else:
        print("   ⚠️  No results (index may be empty or no matches)")
    print()

    # Test 5: Multi-field search
    print("6. Multi-Field Search")
    print("-" * 70)
    print("   Query: 'Order 21 Rule 1'")
    print("   Fields: text^2 (boosted), citation")

    results = searcher.multi_match_search(
        "Order 21 Rule 1",
        fields=["text^2", "citation^1"],
        top_k=5
    )

    if results:
        print(f"   Found {len(results)} results:\n")
        for i, r in enumerate(results, 1):
            print(f"   {i}. [Score: {r.score:.4f}] {r.node_id}")
            print(f"      Order: {r.order}, Rule: {r.rule}")
            print(f"      {r.text[:100]}...")
            print()
    else:
        print("   ⚠️  No results (index may be empty or no matches)")
    print()

    # Summary
    print("=" * 70)
    print("✅ Week 3, Day 3 Complete!")
    print("=" * 70)
    print()
    print("What We Built:")
    print("  ✅ BM25 search with legal analyzer (synonyms)")
    print("  ✅ Multi-field filtering (node_type, court, order, etc.)")
    print("  ✅ Range queries (claim amounts, trial days)")
    print("  ✅ Relevance highlighting")
    print("  ✅ Multi-field search with boosting")
    print()
    print("Next Steps:")
    print("  - Day 4: Test and tune BM25 parameters")
    print("  - Day 5: Benchmark Stage 1 accuracy (target: 62%)")
    print()
    print("Note: To see actual results, you need to:")
    print("  1. Run Day 2 script to index Order 21 nodes")
    print("  2. Then run this search demo again")
    print()


if __name__ == "__main__":
    # Configure logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

    main()
