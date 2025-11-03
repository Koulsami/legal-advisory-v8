"""
Unit Tests for BM25 Search
Legal Advisory System v8.0

Tests the elasticsearch_search module functionality.
"""

import unittest
from elasticsearch_search import LegalBM25Search, SearchFilters, SearchResult


class TestSearchFilters(unittest.TestCase):
    """Test SearchFilters dataclass."""

    def test_create_empty_filters(self):
        """Test creating empty filters."""
        filters = SearchFilters()

        self.assertIsNone(filters.node_types)
        self.assertIsNone(filters.orders)
        self.assertIsNone(filters.courts)
        self.assertIsNone(filters.claim_amount_min)

    def test_create_filters_with_values(self):
        """Test creating filters with values."""
        filters = SearchFilters(
            node_types=["WHAT", "IF_THEN"],
            courts=["High Court"],
            claim_amount_min=10000.0
        )

        self.assertEqual(filters.node_types, ["WHAT", "IF_THEN"])
        self.assertEqual(filters.courts, ["High Court"])
        self.assertEqual(filters.claim_amount_min, 10000.0)
        self.assertIsNone(filters.orders)


class TestSearchResult(unittest.TestCase):
    """Test SearchResult dataclass."""

    def test_create_search_result(self):
        """Test creating a search result."""
        result = SearchResult(
            node_id="order21_rule1_001",
            text="Default judgment may be entered...",
            score=12.5,
            node_type="WHAT",
            order="Order 21"
        )

        self.assertEqual(result.node_id, "order21_rule1_001")
        self.assertEqual(result.score, 12.5)
        self.assertEqual(result.node_type, "WHAT")

    def test_search_result_repr(self):
        """Test SearchResult string representation."""
        result = SearchResult(
            node_id="test_001",
            text="This is a test document with some text",
            score=5.0
        )

        repr_str = repr(result)
        self.assertIn("test_001", repr_str)
        self.assertIn("5.0", repr_str)


class TestLegalBM25Search(unittest.TestCase):
    """Test LegalBM25Search class."""

    @classmethod
    def setUpClass(cls):
        """Set up test fixtures."""
        try:
            cls.searcher = LegalBM25Search()
            cls.es_available = True
        except Exception:
            cls.es_available = False

    def test_initialization(self):
        """Test searcher initialization."""
        if not self.es_available:
            self.skipTest("Elasticsearch not available")

        self.assertEqual(self.searcher.index_name, "singapore_legal_v8")
        self.assertIsNotNone(self.searcher.es)

    def test_build_filter_clauses_empty(self):
        """Test building filter clauses with empty filters."""
        if not self.es_available:
            self.skipTest("Elasticsearch not available")

        filters = SearchFilters()
        clauses = self.searcher._build_filter_clauses(filters)

        self.assertEqual(clauses, [])

    def test_build_filter_clauses_node_types(self):
        """Test building node type filter clauses."""
        if not self.es_available:
            self.skipTest("Elasticsearch not available")

        filters = SearchFilters(node_types=["WHAT", "IF_THEN"])
        clauses = self.searcher._build_filter_clauses(filters)

        self.assertEqual(len(clauses), 1)
        self.assertIn("terms", clauses[0])
        self.assertEqual(clauses[0]["terms"]["node_type"], ["WHAT", "IF_THEN"])

    def test_build_filter_clauses_courts(self):
        """Test building court filter clauses."""
        if not self.es_available:
            self.skipTest("Elasticsearch not available")

        filters = SearchFilters(courts=["High Court"])
        clauses = self.searcher._build_filter_clauses(filters)

        self.assertEqual(len(clauses), 1)
        self.assertIn("terms", clauses[0])
        self.assertEqual(clauses[0]["terms"]["court"], ["High Court"])

    def test_build_filter_clauses_claim_amount(self):
        """Test building claim amount filter clauses."""
        if not self.es_available:
            self.skipTest("Elasticsearch not available")

        filters = SearchFilters(
            claim_amount_min=10000.0,
            claim_amount_max=50000.0
        )
        clauses = self.searcher._build_filter_clauses(filters)

        # Should have 2 range clauses (one for min, one for max)
        self.assertEqual(len(clauses), 2)

    def test_build_filter_clauses_combined(self):
        """Test building combined filter clauses."""
        if not self.es_available:
            self.skipTest("Elasticsearch not available")

        filters = SearchFilters(
            node_types=["WHAT"],
            courts=["High Court"],
            orders=["Order 21"]
        )
        clauses = self.searcher._build_filter_clauses(filters)

        # Should have 3 clauses
        self.assertEqual(len(clauses), 3)

    def test_build_query_simple(self):
        """Test building a simple query."""
        if not self.es_available:
            self.skipTest("Elasticsearch not available")

        query = self.searcher._build_query(
            "default judgment",
            filters=None,
            min_score=None,
            enable_highlight=False
        )

        self.assertIn("query", query)
        self.assertIn("bool", query["query"])
        self.assertIn("must", query["query"]["bool"])

    def test_build_query_with_filters(self):
        """Test building query with filters."""
        if not self.es_available:
            self.skipTest("Elasticsearch not available")

        filters = SearchFilters(node_types=["WHAT"])
        query = self.searcher._build_query(
            "default judgment",
            filters=filters,
            min_score=None,
            enable_highlight=False
        )

        self.assertIn("filter", query["query"]["bool"])

    def test_build_query_with_min_score(self):
        """Test building query with minimum score."""
        if not self.es_available:
            self.skipTest("Elasticsearch not available")

        query = self.searcher._build_query(
            "default judgment",
            filters=None,
            min_score=5.0,
            enable_highlight=False
        )

        self.assertIn("min_score", query)
        self.assertEqual(query["min_score"], 5.0)

    def test_build_query_with_highlight(self):
        """Test building query with highlighting."""
        if not self.es_available:
            self.skipTest("Elasticsearch not available")

        query = self.searcher._build_query(
            "default judgment",
            filters=None,
            min_score=None,
            enable_highlight=True
        )

        self.assertIn("highlight", query)
        self.assertIn("text", query["highlight"]["fields"])

    def test_search_empty_query(self):
        """Test search with empty query."""
        if not self.es_available:
            self.skipTest("Elasticsearch not available")

        results = self.searcher.search("")

        # Should return empty list for empty query
        self.assertEqual(results, [])

    def test_search_returns_list(self):
        """Test that search returns a list."""
        if not self.es_available:
            self.skipTest("Elasticsearch not available")

        results = self.searcher.search("default judgment")

        # Should return a list (may be empty if index is empty)
        self.assertIsInstance(results, list)

    def test_get_stats(self):
        """Test getting index statistics."""
        if not self.es_available:
            self.skipTest("Elasticsearch not available")

        stats = self.searcher.get_stats()

        # Should have expected keys
        self.assertIn("index_name", stats)
        self.assertIn("document_count", stats)
        self.assertIn("size_mb", stats)


class TestIntegration(unittest.TestCase):
    """Integration tests (require Elasticsearch running)."""

    @classmethod
    def setUpClass(cls):
        """Set up test fixtures."""
        try:
            cls.searcher = LegalBM25Search()
            stats = cls.searcher.get_stats()
            cls.es_available = "error" not in stats
        except Exception:
            cls.es_available = False

    def test_full_search_workflow(self):
        """Test complete search workflow."""
        if not self.es_available:
            self.skipTest("Elasticsearch not available")

        # Simple search
        results1 = self.searcher.search("default judgment", top_k=5)
        self.assertIsInstance(results1, list)

        # Search with filters
        filters = SearchFilters(node_types=["WHAT"])
        results2 = self.searcher.search("costs", filters=filters, top_k=5)
        self.assertIsInstance(results2, list)

        # Multi-field search
        results3 = self.searcher.multi_match_search(
            "Order 21",
            fields=["text^2", "citation"]
        )
        self.assertIsInstance(results3, list)


def run_tests():
    """Run all tests."""
    print("=" * 70)
    print("BM25 Search - Unit Tests")
    print("=" * 70)
    print()

    # Create test suite
    suite = unittest.TestLoader().loadTestsFromModule(__import__(__name__))

    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    # Summary
    print()
    print("=" * 70)
    if result.wasSuccessful():
        print("✅ All tests passed!")
    else:
        print("❌ Some tests failed")
    print("=" * 70)

    return result.wasSuccessful()


if __name__ == "__main__":
    run_tests()
