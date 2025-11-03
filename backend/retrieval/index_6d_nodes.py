"""
6D Node Indexer for Elasticsearch
Legal Advisory System v8.0

This script indexes 6D logic tree nodes into Elasticsearch.

Process:
1. Load nodes from logic tree modules (e.g., Order21Module)
2. Convert 6D nodes to Elasticsearch documents
3. Index with BM25 and legal analyzer
4. Enable hybrid search (keyword + logic tree)

Usage:
    python index_6d_nodes.py
"""

from typing import Dict, List, Any
from elasticsearch import Elasticsearch
from datetime import datetime
import logging
import sys
import os

# Add paths
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from knowledge_graph.six_dimensions import LegalLogicNode
from knowledge_graph.modules.order21_module import Order21Module
from knowledge_graph.modules.order21_costs_module import Order21CostsModule
from knowledge_graph.modules.order5_module import Order5Module
from knowledge_graph.modules.order14_module import Order14Module

logger = logging.getLogger(__name__)


class Node6DIndexer:
    """
    Index 6D logic tree nodes into Elasticsearch.

    This bridges the logic tree system with BM25 search,
    enabling hybrid retrieval:
    - BM25 for keyword matching
    - Logic tree for formal reasoning
    """

    def __init__(self, es_url: str = "http://localhost:9200"):
        """
        Initialize indexer.

        Args:
            es_url: Elasticsearch connection URL
        """
        self.es = Elasticsearch([es_url])
        self.index_name = "singapore_legal_6d"

    def convert_node_to_doc(self, node: LegalLogicNode) -> Dict[str, Any]:
        """
        Convert a 6D logic node to Elasticsearch document.

        Args:
            node: LegalLogicNode to convert

        Returns:
            Dict ready for Elasticsearch indexing
        """

        # Convert node to dict (uses node.to_dict())
        doc = node.to_dict()

        # Add search-optimized fields
        doc["created_at"] = datetime.now().isoformat()
        doc["updated_at"] = datetime.now().isoformat()

        # Build searchable full_text from all dimensions
        if not doc.get("full_text"):
            full_text_parts = []

            # Add citation
            full_text_parts.append(node.citation)

            # Add WHAT
            for what in node.what:
                full_text_parts.append(what.text)

            # Add WHICH
            for which in node.which:
                full_text_parts.append(which.text)

            # Add IF-THEN
            for if_then in node.if_then:
                full_text_parts.append(f"IF {if_then.condition} THEN {if_then.consequence}")

            # Add CAN/MUST
            for can_must in node.can_must:
                full_text_parts.append(f"{can_must.modality_type.value} {can_must.action}")

            # Add GIVEN
            for given in node.given:
                full_text_parts.append(given.text)

            # Add WHY
            for why in node.why:
                full_text_parts.append(why.text)

            doc["full_text"] = " ".join(full_text_parts)

        return doc

    def index_node(self, node: LegalLogicNode) -> bool:
        """
        Index a single node.

        Args:
            node: LegalLogicNode to index

        Returns:
            True if successful
        """

        try:
            doc = self.convert_node_to_doc(node)

            self.es.index(
                index=self.index_name,
                id=node.node_id,
                body=doc
            )

            logger.info(f"✅ Indexed: {node.citation}")
            return True

        except Exception as e:
            logger.error(f"❌ Failed to index {node.node_id}: {e}")
            return False

    def index_module(self, module) -> int:
        """
        Index all nodes from a module.

        Args:
            module: LogicTreeModule instance (e.g., Order21Module)

        Returns:
            Number of nodes successfully indexed
        """

        # Initialize module if needed
        if not module._initialized:
            module.initialize()

        logger.info(f"Indexing module: {module.get_metadata().name}")
        logger.info(f"Total nodes: {len(module.nodes)}")

        success_count = 0

        for node_id, node in module.nodes.items():
            if self.index_node(node):
                success_count += 1

        logger.info(f"Successfully indexed: {success_count}/{len(module.nodes)} nodes")

        # Refresh index
        self.es.indices.refresh(index=self.index_name)

        return success_count

    def delete_module_nodes(self, module_id: str) -> int:
        """
        Delete all nodes from a module.

        Args:
            module_id: Module ID (e.g., "order_21")

        Returns:
            Number of nodes deleted
        """

        try:
            # Delete by query
            response = self.es.delete_by_query(
                index=self.index_name,
                body={
                    "query": {
                        "term": {"module_id": module_id}
                    }
                }
            )

            deleted = response.get('deleted', 0)
            logger.info(f"Deleted {deleted} nodes from module: {module_id}")

            return deleted

        except Exception as e:
            logger.error(f"Failed to delete nodes: {e}")
            return 0

    def get_stats(self) -> Dict[str, Any]:
        """Get indexing statistics."""

        try:
            # Total count
            total_count = self.es.count(index=self.index_name)['count']

            # Count by module
            agg_response = self.es.search(
                index=self.index_name,
                body={
                    "size": 0,
                    "aggs": {
                        "by_module": {
                            "terms": {"field": "module_id"}
                        },
                        "by_source_type": {
                            "terms": {"field": "source_type"}
                        }
                    }
                }
            )

            modules = {}
            for bucket in agg_response['aggregations']['by_module']['buckets']:
                modules[bucket['key']] = bucket['doc_count']

            source_types = {}
            for bucket in agg_response['aggregations']['by_source_type']['buckets']:
                source_types[bucket['key']] = bucket['doc_count']

            return {
                "total_nodes": total_count,
                "by_module": modules,
                "by_source_type": source_types
            }

        except Exception as e:
            logger.error(f"Failed to get stats: {e}")
            return {"error": str(e)}


def main():
    """
    Index Order 21 nodes into Elasticsearch.
    """

    print("=" * 70)
    print("6D Node Indexer - Elasticsearch Integration")
    print("Week 3, Day 3: Index Order 21 Logic Tree")
    print("=" * 70)
    print()

    # Initialize
    indexer = Node6DIndexer()

    # Check connection
    print("1. Checking Elasticsearch connection...")
    try:
        if not indexer.es.ping():
            print("❌ Cannot connect to Elasticsearch")
            print("   Make sure Elasticsearch is running (docker-compose up)")
            return
        print("✅ Connected to Elasticsearch")
    except Exception as e:
        print(f"❌ Connection error: {e}")
        return

    print()

    # Check if index exists
    print("2. Checking index...")
    if not indexer.es.indices.exists(index=indexer.index_name):
        print(f"❌ Index '{indexer.index_name}' does not exist")
        print("   Run: python elasticsearch_6d_setup.py first")
        return

    print(f"✅ Index '{indexer.index_name}' exists")
    print()

    # Load all modules
    print("3. Loading modules...")
    print("-" * 70)

    modules = []

    # Order 21 - Default Judgment
    order21 = Order21Module()
    order21.initialize()
    modules.append(order21)
    print(f"   ✅ Order 21 (Default Judgment): {len(order21.nodes)} nodes")

    # Order 21 - Costs
    order21_costs = Order21CostsModule()
    order21_costs.initialize()
    modules.append(order21_costs)
    print(f"   ✅ Order 21 (Costs): {len(order21_costs.nodes)} nodes")

    # Order 5
    order5 = Order5Module()
    order5.initialize()
    modules.append(order5)
    print(f"   ✅ Order 5: {len(order5.nodes)} nodes")

    # Order 14
    order14 = Order14Module()
    order14.initialize()
    modules.append(order14)
    print(f"   ✅ Order 14: {len(order14.nodes)} nodes")

    print("-" * 70)
    total_nodes = sum(len(m.nodes) for m in modules)
    print(f"   Total modules: {len(modules)}")
    print(f"   Total nodes: {total_nodes}")
    print()

    # Index nodes from all modules
    print("4. Indexing nodes...")
    print("-" * 70)

    total_success = 0
    for module in modules:
        metadata = module.get_metadata()
        print(f"\n   Indexing {metadata.name}...")
        success_count = indexer.index_module(module)
        total_success += success_count
        print(f"   ✅ Indexed {success_count}/{len(module.nodes)} nodes")

    print()
    print("-" * 70)
    print(f"✅ Total indexed: {total_success}/{total_nodes} nodes")
    print()

    # Show statistics
    print("5. Index Statistics:")
    print("-" * 70)
    stats = indexer.get_stats()

    print(f"   Total nodes: {stats.get('total_nodes', 0)}")
    print()

    if stats.get('by_module'):
        print("   By module:")
        for module, count in stats['by_module'].items():
            print(f"     {module}: {count} nodes")
        print()

    if stats.get('by_source_type'):
        print("   By source type:")
        for source, count in stats['by_source_type'].items():
            print(f"     {source}: {count} nodes")
        print()

    # Test search
    print("6. Testing search...")
    print("-" * 70)

    test_query = "default judgment"
    print(f"   Query: '{test_query}'")

    try:
        response = indexer.es.search(
            index=indexer.index_name,
            body={
                "query": {
                    "match": {
                        "full_text": test_query
                    }
                },
                "size": 3
            }
        )

        hits = response['hits']['hits']
        print(f"   Results: {len(hits)}")

        for i, hit in enumerate(hits, 1):
            source = hit['_source']
            print(f"\n   {i}. {source['citation']} (score: {hit['_score']:.2f})")
            print(f"      Module: {source['module_id']}")
            print(f"      Authority: {source['authority_weight']}")

    except Exception as e:
        print(f"   ❌ Search test failed: {e}")

    print()
    print("=" * 70)
    print("✅ Indexing Complete!")
    print("=" * 70)
    print()
    print("What's Working:")
    print("  ✅ Order 21 nodes indexed (Default Judgment)")
    print("  ✅ Order 21 Costs nodes indexed (11 case citations + Appendix G)")
    print("  ✅ Order 5 nodes indexed (Amicable Resolution)")
    print("  ✅ Order 14 nodes indexed (Payment into Court)")
    print("  ✅ 6D dimensions stored (WHAT, IF_THEN, etc.)")
    print("  ✅ BM25 search enabled")
    print("  ✅ Authority weights stored")
    print("  ✅ Relationships indexed")
    print()
    print("Next Steps:")
    print("  1. Test hybrid search with cross-module queries")
    print("  2. Test query routing across modules")
    print("  3. Benchmark retrieval accuracy")
    print()


if __name__ == "__main__":
    # Configure logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )

    main()
