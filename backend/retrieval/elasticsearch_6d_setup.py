"""
Elasticsearch Setup for 6D Logic Tree Integration
Legal Advisory System v8.0

This extends the base Elasticsearch setup to support 6D logic tree nodes.

New capabilities:
- Store complete 6D node structure (WHAT, WHICH, IF_THEN, etc.)
- Index relationships (parent-child, interprets, extends)
- Store authority weights
- Support temporal validity
- Enable hybrid search (BM25 + logic tree reasoning)

Based on: Week 3 Day 3 - 6D Logic Tree Architecture
"""

from typing import Dict, Any
from elasticsearch import Elasticsearch
import logging

logger = logging.getLogger(__name__)


class Elasticsearch6DSetup:
    """
    Configure Elasticsearch for 6D logic tree nodes.

    Combines:
    - BM25 keyword search (from earlier setup)
    - 6D logic tree structure
    - Relationship mapping
    - Authority weighting
    """

    def __init__(self, es_url: str = "http://localhost:9200"):
        """
        Initialize Elasticsearch connection.

        Args:
            es_url: Elasticsearch connection URL
        """
        self.es = Elasticsearch([es_url])
        self.index_name = "singapore_legal_6d"

        logger.info(f"Connecting to Elasticsearch at {es_url}")

    def check_connection(self) -> bool:
        """Verify Elasticsearch is accessible."""
        try:
            if self.es.ping():
                logger.info("✅ Connected to Elasticsearch")
                return True
            else:
                logger.error("❌ Cannot connect to Elasticsearch")
                return False
        except Exception as e:
            logger.error(f"❌ Elasticsearch connection error: {e}")
            return False

    def get_index_settings(self) -> Dict[str, Any]:
        """
        Get index settings for 6D logic tree nodes.

        This extends the base settings with:
        - 6D dimension fields (what, which, if_then, can_must, given, why)
        - Relationship fields (parent, children, interprets, etc.)
        - Authority weighting
        - Module metadata

        Returns:
            Dict with complete index settings and mappings
        """

        settings = {
            "settings": {
                "index": {
                    "number_of_shards": 1,
                    "number_of_replicas": 0,  # Development setting
                    "similarity": {
                        "legal_bm25": {
                            "type": "BM25",
                            "k1": 1.5,  # Term frequency saturation
                            "b": 0.75   # Length normalization
                        }
                    }
                },
                "analysis": {
                    "analyzer": {
                        "legal_analyzer": {
                            "type": "custom",
                            "tokenizer": "standard",
                            "filter": [
                                "lowercase",
                                "legal_stop_words",
                                "legal_synonyms",
                                "english_stemmer"
                            ]
                        }
                    },
                    "filter": {
                        "legal_stop_words": {
                            "type": "stop",
                            "stopwords": [
                                "a", "an", "and", "are", "as", "at", "be", "but", "by",
                                "for", "if", "in", "into", "is", "it", "no", "not", "of",
                                "on", "or", "such", "that", "the", "their", "then", "there",
                                "these", "they", "this", "to", "was", "will", "with"
                            ]
                        },
                        "legal_synonyms": {
                            "type": "synonym",
                            "synonyms": [
                                # Singapore court synonyms
                                "plaintiff,claimant,applicant",
                                "defendant,respondent",
                                "HC,SGHC",
                                "DC,SGDC",
                                "MC,SGMC",
                                "CA,SGCA",

                                # Legal terms
                                "costs,fees,charges,expenses",
                                "judgment,judgement",
                                "order,direction",
                                "application,motion",
                                "liquidated,ascertained",
                                "unliquidated,unascertained",
                                "default,absence",
                                "summary,expedited",
                                "trial,hearing",
                                "appeal,review",

                                # Common terms
                                "interlocutory,interim,temporary"
                            ]
                        },
                        "english_stemmer": {
                            "type": "stemmer",
                            "language": "english"
                        }
                    }
                }
            },
            "mappings": {
                "properties": {
                    # ========== Core Identification ==========
                    "node_id": {
                        "type": "keyword"
                    },
                    "citation": {
                        "type": "text",
                        "analyzer": "legal_analyzer",
                        "fields": {
                            "keyword": {"type": "keyword"}
                        }
                    },
                    "source_type": {
                        "type": "keyword"  # STATUTE, RULE, CASE
                    },
                    "authority_weight": {
                        "type": "float"
                    },

                    # ========== 6D Dimensions ==========
                    # Each dimension is both text (searchable) and structured (for reasoning)

                    "what": {
                        "type": "nested",
                        "properties": {
                            "text": {
                                "type": "text",
                                "analyzer": "legal_analyzer",
                                "similarity": "legal_bm25"
                            },
                            "confidence": {"type": "float"},
                            "source_line": {"type": "keyword"}
                        }
                    },

                    "which": {
                        "type": "nested",
                        "properties": {
                            "text": {
                                "type": "text",
                                "analyzer": "legal_analyzer",
                                "similarity": "legal_bm25"
                            },
                            "confidence": {"type": "float"},
                            "source_line": {"type": "keyword"}
                        }
                    },

                    "if_then": {
                        "type": "nested",
                        "properties": {
                            "condition": {
                                "type": "text",
                                "analyzer": "legal_analyzer",
                                "similarity": "legal_bm25"
                            },
                            "consequence": {
                                "type": "text",
                                "analyzer": "legal_analyzer",
                                "similarity": "legal_bm25"
                            },
                            "exceptions": {"type": "text"},
                            "confidence": {"type": "float"},
                            "source_line": {"type": "keyword"}
                        }
                    },

                    "can_must": {
                        "type": "nested",
                        "properties": {
                            "action": {
                                "type": "text",
                                "analyzer": "legal_analyzer",
                                "similarity": "legal_bm25"
                            },
                            "modality": {
                                "type": "keyword"  # MUST, SHALL, MAY, etc.
                            },
                            "conditions": {"type": "text"},
                            "confidence": {"type": "float"},
                            "source_line": {"type": "keyword"}
                        }
                    },

                    "given": {
                        "type": "nested",
                        "properties": {
                            "text": {
                                "type": "text",
                                "analyzer": "legal_analyzer",
                                "similarity": "legal_bm25"
                            },
                            "confidence": {"type": "float"},
                            "source_line": {"type": "keyword"}
                        }
                    },

                    "why": {
                        "type": "nested",
                        "properties": {
                            "text": {
                                "type": "text",
                                "analyzer": "legal_analyzer",
                                "similarity": "legal_bm25"
                            },
                            "confidence": {"type": "float"},
                            "source_line": {"type": "keyword"}
                        }
                    },

                    # ========== Full Text (for BM25 search) ==========
                    "full_text": {
                        "type": "text",
                        "analyzer": "legal_analyzer",
                        "similarity": "legal_bm25"
                    },

                    # ========== Tree Relationships ==========
                    "parent_id": {
                        "type": "keyword"
                    },
                    "children_ids": {
                        "type": "keyword"
                    },

                    # ========== Legal Relationships ==========
                    "interprets_ids": {
                        "type": "keyword"
                    },
                    "extends_ids": {
                        "type": "keyword"
                    },
                    "overruled_by_ids": {
                        "type": "keyword"
                    },
                    "distinguishes_ids": {
                        "type": "keyword"
                    },
                    "conflicts_with_ids": {
                        "type": "keyword"
                    },
                    "harmonizes_with_ids": {
                        "type": "keyword"
                    },

                    # ========== Temporal Validity ==========
                    "effective_date": {
                        "type": "date"
                    },
                    "overruled_date": {
                        "type": "date"
                    },
                    "is_valid": {
                        "type": "boolean"
                    },

                    # ========== Module Metadata ==========
                    "module_id": {
                        "type": "keyword"
                    },
                    "version": {
                        "type": "keyword"
                    },
                    "validated_by": {
                        "type": "keyword"
                    },
                    "validated_date": {
                        "type": "date"
                    },

                    # ========== Search Metadata ==========
                    "created_at": {
                        "type": "date"
                    },
                    "updated_at": {
                        "type": "date"
                    }
                }
            }
        }

        return settings

    def create_index(self, delete_if_exists: bool = False) -> bool:
        """
        Create the 6D logic tree index.

        Args:
            delete_if_exists: If True, delete existing index first

        Returns:
            True if successful, False otherwise
        """

        try:
            # Check if index exists
            if self.es.indices.exists(index=self.index_name):
                if delete_if_exists:
                    logger.warning(f"Deleting existing index: {self.index_name}")
                    self.es.indices.delete(index=self.index_name)
                else:
                    logger.info(f"Index '{self.index_name}' already exists")
                    return True

            # Create index with 6D settings
            logger.info(f"Creating index: {self.index_name}")
            settings = self.get_index_settings()

            response = self.es.indices.create(
                index=self.index_name,
                body=settings
            )

            logger.info(f"✅ Created index '{self.index_name}' with 6D logic tree support")
            logger.info(f"   BM25 parameters: k1=1.5, b=0.75")
            logger.info(f"   6D dimensions: WHAT, WHICH, IF_THEN, CAN_MUST, GIVEN, WHY")
            logger.info(f"   Relationships: parent-child, interprets, extends, etc.")

            return True

        except Exception as e:
            logger.error(f"❌ Failed to create index: {e}")
            return False

    def get_index_info(self) -> Dict[str, Any]:
        """Get information about the 6D index."""

        try:
            if not self.es.indices.exists(index=self.index_name):
                return {"error": "Index does not exist"}

            stats = self.es.indices.stats(index=self.index_name)
            settings = self.es.indices.get_settings(index=self.index_name)
            mapping = self.es.indices.get_mapping(index=self.index_name)

            doc_count = stats['indices'][self.index_name]['total']['docs']['count']
            size_bytes = stats['indices'][self.index_name]['total']['store']['size_in_bytes']

            return {
                "index_name": self.index_name,
                "document_count": doc_count,
                "size_mb": round(size_bytes / 1024 / 1024, 2),
                "settings": settings,
                "mapping": mapping
            }

        except Exception as e:
            logger.error(f"❌ Failed to get index info: {e}")
            return {"error": str(e)}


def main():
    """
    Setup script for 6D Elasticsearch index.
    """

    print("=" * 70)
    print("Legal Advisory v8.0 - 6D Logic Tree + Elasticsearch Integration")
    print("Week 3, Day 3: Hybrid Search (BM25 + Logic Tree)")
    print("=" * 70)
    print()

    # Initialize
    setup = Elasticsearch6DSetup()

    # Check connection
    print("1. Testing Elasticsearch connection...")
    if not setup.check_connection():
        print("❌ Cannot connect to Elasticsearch")
        print("   Make sure: docker-compose ps shows elasticsearch as healthy")
        return

    print("✅ Connected to Elasticsearch")
    print()

    # Create index
    print("2. Creating 6D logic tree index...")
    if setup.create_index(delete_if_exists=True):
        print("✅ Index created successfully")
    else:
        print("❌ Failed to create index")
        return

    print()

    # Show index info
    print("3. Index Information:")
    info = setup.get_index_info()
    print(f"   Index: {info.get('index_name')}")
    print(f"   Documents: {info.get('document_count', 0)}")
    print(f"   Size: {info.get('size_mb', 0)} MB")
    print()

    # Show mappings summary
    print("4. Index Capabilities:")
    print("   ✅ BM25 keyword search (k1=1.5, b=0.75)")
    print("   ✅ Legal synonyms (Singapore-specific)")
    print("   ✅ 6D dimensions (WHAT, WHICH, IF_THEN, CAN_MUST, GIVEN, WHY)")
    print("   ✅ Tree relationships (parent-child)")
    print("   ✅ Legal relationships (interprets, extends, overrules)")
    print("   ✅ Authority weighting")
    print("   ✅ Temporal validity")
    print()

    print("=" * 70)
    print("✅ 6D Elasticsearch Index Ready!")
    print("=" * 70)
    print()
    print("Next Steps:")
    print("  1. Index Order 21 nodes (run indexer)")
    print("  2. Test hybrid search (BM25 + logic tree)")
    print("  3. Benchmark retrieval accuracy")
    print()


if __name__ == "__main__":
    # Configure logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

    main()
