"""
Elasticsearch Setup for Legal Document Retrieval
Legal Advisory System v8.0

This module sets up Elasticsearch with legal-optimized settings:
- Singapore legal synonyms
- Custom legal analyzer
- BM25 similarity (k1=1.5, b=0.75 - tuned for legal documents)
- Optimized field mappings

Based on research: COLIEE 2023 competition specifications
"""

from typing import Dict, Any
from elasticsearch import Elasticsearch
import logging

logger = logging.getLogger(__name__)


class ElasticsearchLegalSetup:
    """
    Configure Elasticsearch for legal document retrieval.

    This is Day 1 of Week 3 implementation.
    """

    def __init__(self, es_url: str = "http://localhost:9200"):
        """
        Initialize Elasticsearch connection.

        Args:
            es_url: Elasticsearch connection URL
        """
        self.es = Elasticsearch([es_url])
        self.index_name = "singapore_legal_v8"

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
        Get optimized index settings for Singapore legal documents.

        Key optimizations:
        1. BM25 similarity with k1=1.5, b=0.75 (tuned for legal text)
        2. Singapore legal synonyms
        3. Custom legal analyzer

        Returns:
            Dict with index settings and mappings
        """

        settings = {
            "settings": {
                "index": {
                    "number_of_shards": 1,
                    "number_of_replicas": 0,  # Development setting
                    "similarity": {
                        "legal_bm25": {
                            "type": "BM25",
                            "k1": 1.5,  # Term frequency saturation (tuned for legal)
                            "b": 0.75   # Length normalization (tuned for legal)
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
                                # Standard English stop words
                                "a", "an", "and", "are", "as", "at", "be", "but", "by",
                                "for", "if", "in", "into", "is", "it", "no", "not", "of",
                                "on", "or", "such", "that", "the", "their", "then", "there",
                                "these", "they", "this", "to", "was", "will", "with"
                            ]
                        },
                        "legal_synonyms": {
                            "type": "synonym",
                            "synonyms": [
                                # Singapore court synonyms (simple words only for now)
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
                    # Core identification
                    "node_id": {
                        "type": "keyword"
                    },

                    # Main content with legal analyzer and BM25
                    "text": {
                        "type": "text",
                        "analyzer": "legal_analyzer",
                        "similarity": "legal_bm25",
                        "fields": {
                            "exact": {
                                "type": "keyword"
                            }
                        }
                    },

                    # 6-dimensional logic tree structure
                    "node_type": {
                        "type": "keyword"  # WHAT, WHICH, IF_THEN, MODALITY, GIVEN, WHY
                    },

                    # Legal metadata
                    "order": {
                        "type": "keyword"  # Order 21, Order 5, etc.
                    },
                    "rule": {
                        "type": "keyword"  # Rule 1, Rule 2, etc.
                    },
                    "court": {
                        "type": "keyword"  # High Court, District Court, etc.
                    },
                    "case_type": {
                        "type": "keyword"  # default_judgment, summary_judgment, etc.
                    },

                    # Claim amount for range queries
                    "claim_amount_min": {
                        "type": "float"
                    },
                    "claim_amount_max": {
                        "type": "float"
                    },

                    # Trial duration
                    "trial_days_min": {
                        "type": "integer"
                    },
                    "trial_days_max": {
                        "type": "integer"
                    },

                    # Metadata
                    "citation": {
                        "type": "text",
                        "analyzer": "legal_analyzer"
                    },
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
        Create the legal documents index with optimized settings.

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

            # Create index with legal settings
            logger.info(f"Creating index: {self.index_name}")
            settings = self.get_index_settings()

            response = self.es.indices.create(
                index=self.index_name,
                body=settings
            )

            logger.info(f"✅ Created index '{self.index_name}' with legal analyzer")
            logger.info(f"   BM25 parameters: k1=1.5, b=0.75")
            logger.info(f"   Singapore legal synonyms loaded")

            return True

        except Exception as e:
            logger.error(f"❌ Failed to create index: {e}")
            return False

    def test_analyzer(self, text: str) -> Dict[str, Any]:
        """
        Test the legal analyzer with sample text.

        Args:
            text: Text to analyze

        Returns:
            Analyzed tokens
        """

        try:
            response = self.es.indices.analyze(
                index=self.index_name,
                body={
                    "analyzer": "legal_analyzer",
                    "text": text
                }
            )

            tokens = [token['token'] for token in response['tokens']]
            logger.info(f"Analyzed text: '{text}'")
            logger.info(f"Tokens: {tokens}")

            return response

        except Exception as e:
            logger.error(f"❌ Analyzer test failed: {e}")
            return {}

    def get_index_info(self) -> Dict[str, Any]:
        """Get information about the index."""

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
                "size_bytes": size_bytes,
                "size_mb": round(size_bytes / 1024 / 1024, 2),
                "settings": settings,
                "mapping": mapping
            }

        except Exception as e:
            logger.error(f"❌ Failed to get index info: {e}")
            return {"error": str(e)}


def main():
    """
    Main setup function for Day 1 of Week 3.

    This sets up Elasticsearch with legal-optimized configuration.
    """

    print("=" * 70)
    print("Legal Advisory v8.0 - Elasticsearch Setup")
    print("Week 3, Day 1: Configure Elasticsearch with Legal Analyzer")
    print("=" * 70)
    print()

    # Initialize
    setup = ElasticsearchLegalSetup()

    # Check connection
    print("1. Testing Elasticsearch connection...")
    if not setup.check_connection():
        print("❌ Cannot connect to Elasticsearch")
        print("   Make sure: docker-compose ps shows elasticsearch as healthy")
        return

    print("✅ Connected to Elasticsearch")
    print()

    # Create index
    print("2. Creating legal documents index...")
    if setup.create_index(delete_if_exists=True):
        print("✅ Index created successfully")
    else:
        print("❌ Failed to create index")
        return

    print()

    # Test analyzer
    print("3. Testing legal analyzer...")
    test_texts = [
        "High Court default judgment for $50,000",
        "District Court summary judgment application",
        "Order 21 Rule 1 costs assessment"
    ]

    for text in test_texts:
        print(f"\nTest: '{text}'")
        result = setup.test_analyzer(text)
        if result:
            tokens = [t['token'] for t in result['tokens']]
            print(f"Tokens: {tokens}")

    print()
    print("=" * 70)
    print("✅ Week 3, Day 1 Complete!")
    print("=" * 70)
    print()
    print("Next: Day 2 - Index Order 21 nodes into Elasticsearch")
    print("      Day 3 - Implement BM25 search function")
    print()


if __name__ == "__main__":
    # Configure logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

    main()
