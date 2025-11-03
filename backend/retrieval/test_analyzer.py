"""
Interactive Legal Analyzer Tester
Legal Advisory System v8.0

Test the Elasticsearch legal analyzer with custom queries.
See how synonyms, stemming, and stop words work.
"""

from elasticsearch import Elasticsearch
import sys


class AnalyzerTester:
    """Interactive tester for the legal analyzer."""

    def __init__(self):
        self.es = Elasticsearch(["http://localhost:9200"])
        self.index_name = "singapore_legal_v8"

    def analyze_text(self, text: str) -> dict:
        """
        Analyze text and show the tokens.

        Args:
            text: Text to analyze

        Returns:
            Analysis results
        """
        try:
            response = self.es.indices.analyze(
                index=self.index_name,
                body={
                    "analyzer": "legal_analyzer",
                    "text": text
                }
            )
            return response
        except Exception as e:
            return {"error": str(e)}

    def display_analysis(self, text: str):
        """Display analysis results in a nice format."""

        print("\n" + "=" * 70)
        print(f"INPUT: {text}")
        print("=" * 70)

        result = self.analyze_text(text)

        if "error" in result:
            print(f"❌ Error: {result['error']}")
            return

        tokens = result.get('tokens', [])

        if not tokens:
            print("No tokens generated")
            return

        # Show tokens
        print("\nTOKENS GENERATED:")
        print("-" * 70)
        token_list = [t['token'] for t in tokens]
        print(f"  {', '.join(token_list)}")
        print()

        # Show details
        print("DETAILED BREAKDOWN:")
        print("-" * 70)
        for i, token_info in enumerate(tokens, 1):
            token = token_info['token']
            position = token_info['position']
            print(f"  {i}. '{token}' (position: {position})")

        print()

        # Show what happened
        print("WHAT HAPPENED:")
        print("-" * 70)

        original_words = text.lower().split()
        explanations = []

        # Detect synonyms
        for word in original_words:
            if word in ['costs', 'fees', 'charges', 'expenses']:
                explanations.append(f"  • '{word}' → expanded to synonyms (costs/fees/charges/expenses)")
            elif word in ['judgment', 'judgement']:
                explanations.append(f"  • '{word}' → both spellings indexed")
            elif word in ['summary', 'expedited']:
                explanations.append(f"  • '{word}' → synonym match")
            elif word in ['default', 'absence']:
                explanations.append(f"  • '{word}' → synonym match")
            elif word in ['high', 'district', 'magistrates']:
                explanations.append(f"  • '{word}' → preserved (important legal term)")
            elif word in ['court', 'rule', 'order']:
                explanations.append(f"  • '{word}' → preserved and stemmed")

        # Detect stemming
        if any('assess' in str(token_list) for token in tokens):
            explanations.append("  • 'assessment' → stemmed to 'assess'")
        if any('applic' in str(token_list) for token in tokens):
            explanations.append("  • 'application' → stemmed to 'applic'")

        # Detect stop words removed
        stop_words = ['for', 'the', 'a', 'an', 'and', 'or', 'of', 'in', 'to', 'at']
        removed_stops = [w for w in original_words if w in stop_words]
        if removed_stops:
            explanations.append(f"  • Stop words removed: {', '.join(removed_stops)}")

        if explanations:
            for exp in explanations:
                print(exp)
        else:
            print("  • Text processed with standard tokenization and stemming")

        print()

    def run_interactive(self):
        """Run interactive testing mode."""

        print("\n" + "=" * 70)
        print("INTERACTIVE LEGAL ANALYZER TESTER")
        print("Legal Advisory System v8.0")
        print("=" * 70)
        print()
        print("This tool shows how your queries are processed by Elasticsearch.")
        print()
        print("Features:")
        print("  • Singapore legal synonyms (HC = High Court, etc.)")
        print("  • Legal term synonyms (costs = fees = charges = expenses)")
        print("  • English stemming (judgment → judg, application → applic)")
        print("  • Stop word removal (for, the, and, etc.)")
        print()
        print("Commands:")
        print("  - Type any query to analyze it")
        print("  - Type 'examples' to see sample queries")
        print("  - Type 'quit' or 'exit' to quit")
        print()

        while True:
            try:
                query = input("Enter query (or 'quit'): ").strip()

                if not query:
                    continue

                if query.lower() in ['quit', 'exit', 'q']:
                    print("\nGoodbye! 👋")
                    break

                if query.lower() == 'examples':
                    self.show_examples()
                    continue

                self.display_analysis(query)

            except KeyboardInterrupt:
                print("\n\nGoodbye! 👋")
                break
            except Exception as e:
                print(f"\n❌ Error: {e}\n")

    def show_examples(self):
        """Show example queries."""

        print("\n" + "=" * 70)
        print("EXAMPLE QUERIES TO TRY")
        print("=" * 70)
        print()

        examples = [
            ("High Court default judgment for $50,000", "See court + amount processing"),
            ("District Court summary judgment application", "See synonym expansion"),
            ("Order 21 Rule 1 costs assessment", "See legal term handling"),
            ("Interlocutory application in chambers", "See legal phrase processing"),
            ("Plaintiff costs against defendant", "See synonym matching"),
            ("Liquidated claim for fees and expenses", "See multiple synonyms"),
            ("SGHC judgment on taxation of costs", "See court abbreviations"),
        ]

        for query, description in examples:
            print(f"  {query}")
            print(f"    → {description}")
            print()

        print("Copy any example above and paste it when prompted!")
        print()


def main():
    """Main entry point."""

    tester = AnalyzerTester()

    # Check if query provided as argument
    if len(sys.argv) > 1:
        # Single query mode
        query = " ".join(sys.argv[1:])
        tester.display_analysis(query)
    else:
        # Interactive mode
        tester.run_interactive()


if __name__ == "__main__":
    main()
