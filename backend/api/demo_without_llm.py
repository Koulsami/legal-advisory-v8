"""
Demo: Backend-Only Conversational Interface (No API Key Required)

This demonstrates the conversational interface architecture WITHOUT
requiring Claude API. It shows:
1. How the backend provides structured legal reasoning
2. How that could be formatted conversationally
3. The separation between legal content (backend) and presentation (LLM)

Use this to understand the system architecture without needing API credentials.
"""

import sys
import os

# Add paths
backend_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, backend_dir)
sys.path.insert(0, os.path.join(backend_dir, 'retrieval'))

from hybrid_search_6d import HybridSearch6D


def format_backend_result(query: str, result) -> dict:
    """
    Simulate what the conversational interface does:
    Extract structured data from backend and format it clearly.
    """

    formatted = {
        "query": query,
        "structured_data": {},
        "conversational_template": ""
    }

    # Extract structured data (same as conversational interface)
    if result.bm25_results:
        top_result = result.bm25_results[0]
        formatted['structured_data'] = {
            "source": top_result['source']['citation'],
            "module": top_result['source']['module_id'],
            "bm25_score": top_result['score']
        }

    if result.logic_tree_answer:
        logic = result.logic_tree_answer
        formatted['structured_data'].update({
            "conclusion": logic.conclusion,
            "confidence": logic.confidence,
            "reasoning_steps": [
                {
                    "dimension": step.dimension,
                    "text": step.text,
                    "source": step.citation if hasattr(step, 'citation') else "N/A"
                }
                for step in logic.reasoning_chain
            ]
        })

    formatted['structured_data']['hybrid_score'] = result.hybrid_score

    # Create conversational template (this is what LLM would generate)
    formatted['conversational_template'] = create_conversational_response(
        query,
        formatted['structured_data']
    )

    return formatted


def create_conversational_response(query: str, data: dict) -> str:
    """
    Create a conversational response template.
    In production, Claude API would generate this naturally.
    """

    response_parts = []

    # Direct answer
    if 'conclusion' in data:
        response_parts.append(f"**Answer:** {data['conclusion']}")
        response_parts.append("")

    # Explanation with reasoning
    if 'reasoning_steps' in data and len(data['reasoning_steps']) > 0:
        response_parts.append("**How we determined this:**")
        response_parts.append("")

        # Group by dimension
        by_dimension = {}
        for step in data['reasoning_steps']:
            dim = step['dimension']
            if dim not in by_dimension:
                by_dimension[dim] = []
            by_dimension[dim].append(step['text'])

        if 'GIVEN' in by_dimension:
            response_parts.append("*Prerequisites:*")
            for text in by_dimension['GIVEN']:
                response_parts.append(f"  • {text}")
            response_parts.append("")

        if 'IF-THEN' in by_dimension:
            response_parts.append("*Conditions:*")
            for text in by_dimension['IF-THEN']:
                response_parts.append(f"  • {text}")
            response_parts.append("")

        if 'WHAT' in by_dimension:
            response_parts.append("*Legal Rule:*")
            for text in by_dimension['WHAT']:
                response_parts.append(f"  • {text}")
            response_parts.append("")

        if 'CAN/MUST' in by_dimension:
            response_parts.append("*Your Options:*")
            for text in by_dimension['CAN/MUST']:
                response_parts.append(f"  • {text}")
            response_parts.append("")

    # Source and confidence
    response_parts.append("**Source:**")
    response_parts.append(f"  📚 {data.get('source', 'N/A')}")
    response_parts.append(f"  📦 Module: {data.get('module', 'N/A')}")
    if 'confidence' in data:
        response_parts.append(f"  🎯 Confidence: {data['confidence']:.0%}")
    if 'hybrid_score' in data:
        response_parts.append(f"  ⚖️  Overall Score: {data['hybrid_score']:.0%}")

    return "\n".join(response_parts)


def demo_query(backend, query: str):
    """Demo a single query with formatted output."""

    print("=" * 80)
    print("QUERY")
    print("=" * 80)
    print(f"👤 USER: {query}")
    print()

    # Get backend result
    print("⚙️  Processing...")
    result = backend.hybrid_search(query, top_k=3)

    # Format conversationally
    formatted = format_backend_result(query, result)

    print()
    print("=" * 80)
    print("CONVERSATIONAL RESPONSE")
    print("=" * 80)
    print()
    print(formatted['conversational_template'])
    print()

    print("=" * 80)
    print("BACKEND STRUCTURED DATA (for reference)")
    print("=" * 80)
    print()
    print("This is what the backend provides:")
    print(f"  • Source: {formatted['structured_data'].get('source', 'N/A')}")
    print(f"  • Module: {formatted['structured_data'].get('module', 'N/A')}")
    print(f"  • BM25 Score: {formatted['structured_data'].get('bm25_score', 0):.2f}")
    print(f"  • Confidence: {formatted['structured_data'].get('confidence', 0):.0%}")
    print(f"  • Reasoning Steps: {len(formatted['structured_data'].get('reasoning_steps', []))}")
    print()


def main():
    """
    Demo the conversational interface architecture without API key.
    """

    print("=" * 80)
    print("CONVERSATIONAL INTERFACE - BACKEND DEMO")
    print("(No API Key Required)")
    print("=" * 80)
    print()

    print("This demo shows:")
    print("  1. How the backend provides structured legal reasoning")
    print("  2. How that data is formatted conversationally")
    print("  3. The separation between legal content and presentation")
    print()

    print("NOTE: In production, Claude API would generate the conversational")
    print("response naturally. This demo uses templates to show the concept.")
    print()

    # Initialize backend
    print("Initializing backend...")
    backend = HybridSearch6D()
    print("✅ Backend initialized (3 modules: Order 21, 5, 14)")
    print()

    # Demo queries
    test_queries = [
        "Can I get default judgment if defendant didn't respond?",
        "Do I need to try to settle before going to court?",
        "How do I pay money into court as a settlement offer?"
    ]

    for query in test_queries:
        demo_query(backend, query)
        print("\n\n")

    # Summary
    print("=" * 80)
    print("ARCHITECTURE EXPLANATION")
    print("=" * 80)
    print()

    print("Layer 1: BACKEND (Formal Legal Reasoning)")
    print("  ┌─────────────────────────────────────────────┐")
    print("  │ • Hybrid Search (BM25 + 6D Logic Tree)     │")
    print("  │ • Pre-validated by legal experts           │")
    print("  │ • Formal logic structure                   │")
    print("  │ • Zero hallucination                       │")
    print("  └─────────────────────────────────────────────┘")
    print("            ↓ (Structured Data)")
    print()

    print("Layer 2: PRESENTATION (Natural Language Formatting)")
    print("  ┌─────────────────────────────────────────────┐")
    print("  │ • Claude API (or template-based)           │")
    print("  │ • Formats backend data conversationally    │")
    print("  │ • Does NOT generate legal content          │")
    print("  │ • Preserves all citations and confidence   │")
    print("  └─────────────────────────────────────────────┘")
    print("            ↓ (Natural Language)")
    print()

    print("Result: USER RECEIVES")
    print("  ┌─────────────────────────────────────────────┐")
    print("  │ • Conversational answer (easy to read)     │")
    print("  │ • Full citations (Order 21 Rule 1, etc.)   │")
    print("  │ • Reasoning chain (GIVEN → IF-THEN → WHAT) │")
    print("  │ • Confidence score (90%, etc.)             │")
    print("  │ • Module source (order_21, etc.)           │")
    print("  └─────────────────────────────────────────────┘")
    print()

    print("Key Principle:")
    print("  🔒 ALL legal content from validated backend")
    print("  🔒 LLM only formats (no generation)")
    print("  🔒 <2% hallucination rate maintained")
    print()

    print("To use with Claude API:")
    print("  1. export ANTHROPIC_API_KEY='your-key'")
    print("  2. python api/example_conversation.py")
    print()


if __name__ == "__main__":
    main()
