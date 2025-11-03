"""
Conversational Interface for Legal Advisory System v8.0

This module provides a natural language interface that:
1. Takes user queries
2. Retrieves formal legal reasoning from backend (hybrid search + 6D logic)
3. Uses Claude API to present results conversationally
4. Maintains full traceability (citations, reasoning chains, confidence)

IMPORTANT: The LLM is ONLY a presentation layer. All legal content comes
from the pre-validated 6D logic tree. The LLM does NOT generate legal advice.

Architecture:
    User Query
        ↓
    Conversational Interface
        ↓
    Hybrid Search Backend (BM25 + 6D Logic Tree)
        ↓
    Structured Results (citations, reasoning, confidence)
        ↓
    Claude API (format only, no generation)
        ↓
    Natural Language Response (with full citations)
"""

import sys
import os
from typing import Dict, Any, Optional, List
import json
import anthropic
from datetime import datetime

# Add paths
backend_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, backend_dir)
sys.path.insert(0, os.path.join(backend_dir, 'retrieval'))
sys.path.insert(0, os.path.join(backend_dir, 'knowledge_graph'))

from hybrid_search_6d import HybridSearch6D


class ConversationalInterface:
    """
    Conversational interface for legal advisory system.

    Combines:
    - Backend: Formal 6D logic tree reasoning (no hallucination)
    - Frontend: Natural language presentation via Claude

    The LLM's role is STRICTLY limited to formatting and presentation.
    All legal content comes from the pre-validated logic tree.
    """

    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize conversational interface.

        Args:
            api_key: Anthropic API key (or use ANTHROPIC_API_KEY env var)
        """
        self.api_key = api_key or os.environ.get("ANTHROPIC_API_KEY")

        if not self.api_key:
            raise ValueError(
                "Anthropic API key required. Set ANTHROPIC_API_KEY environment "
                "variable or pass api_key parameter."
            )

        # Initialize Claude client
        self.client = anthropic.Anthropic(api_key=self.api_key)

        # Initialize hybrid search backend
        self.backend = HybridSearch6D()

        # Threshold for requesting clarification (30% confidence)
        self.clarification_threshold = 0.30

        print("✅ Conversational interface initialized")
        print("   - Backend: Hybrid search (BM25 + 6D logic tree)")
        print("   - Frontend: Claude API (presentation only)")
        print("   - Modules: Order 21, Order 5, Order 14")
        print("   - Clarification mode: Enabled (asks for details when confidence < 30%)")

    def ask(
        self,
        question: str,
        conversation_history: Optional[List[Dict[str, str]]] = None
    ) -> Dict[str, Any]:
        """
        Answer a legal question conversationally.

        Process:
        1. Query backend (hybrid search)
        2. Get structured results (citations, reasoning, confidence)
        3. Use Claude to present results conversationally
        4. Return natural language response WITH full traceability

        Args:
            question: User's legal question
            conversation_history: Optional previous conversation context

        Returns:
            Dict with:
                - answer: Natural language response
                - citations: Source citations
                - reasoning_chain: Formal logic steps
                - confidence: Confidence score
                - metadata: BM25 results, module info, etc.
        """

        print(f"\n🔍 Processing query: \"{question}\"")
        print()

        # Step 1: Query backend (hybrid search + 6D logic)
        print("⚙️  Step 1: Querying backend...")
        backend_result = self.backend.hybrid_search(question, top_k=5)

        # Step 2: Extract structured information
        structured_data = self._extract_structured_data(backend_result)

        print(f"   ✅ Found: {structured_data['source_citation']}")
        print(f"   ✅ Confidence: {structured_data['confidence']:.0%}")
        print(f"   ✅ Reasoning steps: {len(structured_data['reasoning_steps'])}")
        print()

        # Check if confidence is too low - need clarification
        if structured_data['confidence'] < self.clarification_threshold:
            print(f"⚠️  Low confidence ({structured_data['confidence']:.0%}) - Asking for clarification...")
            clarifying_questions = self._generate_clarifying_questions(
                question,
                structured_data,
                conversation_history
            )
            print("   ✅ Clarifying questions generated")
            print()

            # Return request for more information
            return {
                "needs_clarification": True,
                "clarifying_questions": clarifying_questions,
                "original_question": question,
                "confidence": structured_data['confidence'],
                "source_module": structured_data['module'],
                "timestamp": datetime.now().isoformat(),
                "conversation_context": {
                    "backend_result": structured_data,
                    "question": question
                }
            }

        # Step 3: Build prompt for Claude (presentation only)
        print("💬 Step 2: Formatting conversational response...")
        prompt = self._build_presentation_prompt(question, structured_data)

        # Step 4: Get conversational response from Claude
        response = self._call_claude(prompt, conversation_history)

        print("   ✅ Conversational response generated")
        print()

        # Step 5: Package full response with traceability
        full_response = {
            "answer": response,
            "citations": structured_data['citations'],
            "reasoning_chain": structured_data['reasoning_steps'],
            "confidence": structured_data['confidence'],
            "source_module": structured_data['module'],
            "hybrid_score": structured_data['hybrid_score'],
            "timestamp": datetime.now().isoformat(),
            "metadata": {
                "bm25_results": structured_data['bm25_results'],
                "backend_conclusion": structured_data['conclusion']
            }
        }

        return full_response

    def _extract_structured_data(self, backend_result) -> Dict[str, Any]:
        """
        Extract structured information from backend result.

        This ensures all legal content comes from the backend,
        not from the LLM.
        """

        data = {
            "conclusion": "",
            "confidence": 0.0,
            "reasoning_steps": [],
            "citations": [],
            "module": "",
            "source_citation": "",
            "hybrid_score": backend_result.hybrid_score,
            "bm25_results": []
        }

        # Extract BM25 results
        if backend_result.bm25_results:
            top_result = backend_result.bm25_results[0]
            data['source_citation'] = top_result['source']['citation']
            data['module'] = top_result['source']['module_id']

            # All BM25 results for reference
            data['bm25_results'] = [
                {
                    "citation": r['source']['citation'],
                    "score": r['score'],
                    "module": r['source']['module_id']
                }
                for r in backend_result.bm25_results[:5]
            ]

        # Extract logic tree reasoning
        if backend_result.logic_tree_answer:
            logic = backend_result.logic_tree_answer
            data['conclusion'] = logic.conclusion
            data['confidence'] = logic.confidence

            # Extract reasoning chain
            data['reasoning_steps'] = [
                {
                    "dimension": step.dimension,
                    "text": step.text,
                    "source": step.citation if hasattr(step, 'citation') else "N/A"
                }
                for step in logic.reasoning_chain
            ]

            # Extract citations
            citations_set = set()
            for step in logic.reasoning_chain:
                if hasattr(step, 'citation') and step.citation:
                    citations_set.add(step.citation)
            data['citations'] = list(citations_set)

        return data

    def _build_presentation_prompt(
        self,
        question: str,
        structured_data: Dict[str, Any]
    ) -> str:
        """
        Build prompt for Claude to present results conversationally.

        CRITICAL: The prompt instructs Claude to ONLY format the provided
        information, not to generate new legal content.
        """

        # Extract case law citations separately
        case_law_steps = []
        verbatim_quotes = []
        regular_reasoning = []

        for step in structured_data['reasoning_steps']:
            if step['dimension'] == 'WHY':
                if 'Case Law' in step['text'] or 'Verbatim' in step['text']:
                    if 'Verbatim Quote:' in step['text']:
                        verbatim_quotes.append(step)
                    elif 'Case Law:' in step['text']:
                        case_law_steps.append(step)
                    else:
                        regular_reasoning.append(step)
                else:
                    regular_reasoning.append(step)
            else:
                regular_reasoning.append(step)

        # Format regular reasoning
        reasoning_text = "\n".join([
            f"  {i+1}. [{step['dimension']}] {step['text'][:200]}{'...' if len(step['text']) > 200 else ''}"
            for i, step in enumerate(regular_reasoning[:8])
        ])

        # Format case law with summaries
        case_law_text = ""
        if case_law_steps:
            case_law_text = "CASE LAW REFERENCES (with reasoning summaries):\n"
            for i, step in enumerate(case_law_steps[:3], 1):
                case_law_text += f"\n{i}. {step['text']}\n   Source: {step.get('source', 'N/A')}\n"

        # Format verbatim quotes
        verbatim_text = ""
        if verbatim_quotes:
            verbatim_text = "\nVERBATIM QUOTES FROM JUDGMENTS (for verification):\n"
            for i, step in enumerate(verbatim_quotes[:3], 1):
                verbatim_text += f"\n{i}. {step['text']}\n   Source: {step.get('source', 'N/A')}\n"

        citations_text = "\n".join([
            f"  - {citation}"
            for citation in structured_data['citations']
        ])

        prompt = f"""You are presenting legal research results from a formal legal reasoning system.

IMPORTANT INSTRUCTIONS:
1. You are ONLY formatting pre-validated legal information
2. Do NOT generate new legal advice or interpretations
3. Do NOT add information not present in the provided data
4. ALWAYS cite the source provided
5. Present case law references WITH their reasoning summaries
6. Include verbatim quotes in a separate verification section
7. Acknowledge the confidence level

USER QUESTION:
{question}

BACKEND ANALYSIS (PRE-VALIDATED):
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Source: {structured_data['source_citation']}
Module: {structured_data['module']}
Confidence: {structured_data['confidence']:.0%}

CONCLUSION:
{structured_data['conclusion']}

REASONING CHAIN:
{reasoning_text}

{case_law_text}

{verbatim_text}

LEGAL CITATIONS:
{citations_text}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

YOUR TASK:
Present the above information conversationally while:
- Keeping ALL legal content exactly as provided
- Maintaining ALL citations
- Explaining the reasoning chain clearly
- IMPORTANT: Include case law references with their summaries
- IMPORTANT: Include verbatim quotes in a separate section for user verification
- Format verbatim quotes as: "Quote text here" [Paragraph X]
- Noting the confidence level
- Using natural, accessible language
- NOT adding any legal content not present above

Format your response as:
1. Direct answer to the question
2. Explanation with reasoning
3. **Case Law Support** (if applicable):
   - Case name and citation
   - Summary of reasoning
   - Verbatim quote with paragraph number
4. Source citations
5. Confidence/caveats if applicable
"""

        return prompt

    def _generate_clarifying_questions(
        self,
        question: str,
        structured_data: Dict[str, Any],
        conversation_history: Optional[List[Dict[str, str]]] = None
    ) -> List[str]:
        """
        Generate clarifying questions when confidence is low.

        Uses Claude to analyze the query and determine what additional
        information would help provide a better answer.
        """

        # Build prompt to generate clarifying questions
        clarification_prompt = f"""You are a legal advisory system that needs more information to answer a user's question accurately.

USER QUESTION:
{question}

CURRENT SITUATION:
- The system found some potentially relevant information, but confidence is low ({structured_data['confidence']:.0%})
- Best match found: {structured_data['source_citation']}
- Module: {structured_data['module']}

YOUR TASK:
Generate 2-4 clarifying questions to help the user provide the specific information needed to answer their question accurately.

The questions should:
1. Help narrow down the specific area of law they're asking about
2. Gather missing details that would improve the search
3. Be clear and easy to answer
4. Focus on legal context (type of case, court level, stage of proceedings, etc.)

AVAILABLE MODULES:
- Order 21: Default judgment, costs assessment, indemnity basis
- Order 5: Amicable resolution, settlement
- Order 14: Payment into court

Format your response as a numbered list of questions only, no explanations.
"""

        messages = [
            {
                "role": "user",
                "content": clarification_prompt
            }
        ]

        response = self.client.messages.create(
            model="claude-3-haiku-20240307",
            max_tokens=500,
            messages=messages
        )

        # Parse questions from response
        questions_text = response.content[0].text
        questions = [
            q.strip()
            for q in questions_text.split('\n')
            if q.strip() and (q.strip()[0].isdigit() or q.strip().startswith('-'))
        ]

        # Clean up numbering
        cleaned_questions = []
        for q in questions:
            # Remove leading numbers, dots, dashes
            q = q.lstrip('0123456789.-) ').strip()
            if q:
                cleaned_questions.append(q)

        return cleaned_questions[:4]  # Maximum 4 questions

    def _call_claude(
        self,
        prompt: str,
        conversation_history: Optional[List[Dict[str, str]]] = None
    ) -> str:
        """
        Call Claude API for conversational presentation.

        The model's role is STRICTLY formatting/presentation.
        """

        messages = []

        # Add conversation history if provided
        if conversation_history:
            messages.extend(conversation_history)

        # Add current query
        messages.append({
            "role": "user",
            "content": prompt
        })

        # Call Claude
        response = self.client.messages.create(
            model="claude-3-haiku-20240307",  # Claude 3 Haiku (available with this API key)
            max_tokens=2000,
            temperature=0.3,  # Low temperature for consistency
            messages=messages
        )

        return response.content[0].text

    def display_result(self, result: Dict[str, Any]):
        """
        Display conversational result with full traceability.
        """

        print("=" * 80)
        print("CONVERSATIONAL RESPONSE")
        print("=" * 80)
        print()
        print(result['answer'])
        print()

        print("=" * 80)
        print("TRACEABILITY")
        print("=" * 80)
        print()
        print(f"Source: {result['citations'][0] if result['citations'] else 'N/A'}")
        print(f"Module: {result['source_module']}")
        print(f"Confidence: {result['confidence']:.0%}")
        print(f"Hybrid Score: {result['hybrid_score']:.0%}")
        print()

        print("Reasoning Chain:")
        for i, step in enumerate(result['reasoning_chain'][:5], 1):
            print(f"  {i}. [{step['dimension']}] {step['text'][:80]}...")

        if len(result['reasoning_chain']) > 5:
            remaining = len(result['reasoning_chain']) - 5
            print(f"  ... and {remaining} more steps")

        print()
        print(f"Timestamp: {result['timestamp']}")
        print()


def main():
    """
    Demo the conversational interface.
    """

    print("=" * 80)
    print("CONVERSATIONAL LEGAL ADVISORY INTERFACE")
    print("Legal Advisory System v8.0")
    print("=" * 80)
    print()

    # Check for API key
    if not os.environ.get("ANTHROPIC_API_KEY"):
        print("❌ ANTHROPIC_API_KEY environment variable not set")
        print()
        print("To use this interface:")
        print("  export ANTHROPIC_API_KEY='your-api-key-here'")
        print()
        print("Alternatively, you can test without Claude by examining the backend:")
        print("  python -c 'from hybrid_search_6d import HybridSearch6D; ...'")
        return

    # Initialize interface
    interface = ConversationalInterface()
    print()

    # Test queries
    test_queries = [
        "Can I get default judgment if the defendant didn't respond to my lawsuit?",
        "Do I need to try to settle with the other party before going to court?",
        "How do I make a formal settlement offer using the payment into court procedure?"
    ]

    for i, query in enumerate(test_queries, 1):
        print("=" * 80)
        print(f"DEMO QUERY {i}")
        print("=" * 80)
        print()

        result = interface.ask(query)
        interface.display_result(result)
        print()

    print("=" * 80)
    print("✅ CONVERSATIONAL INTERFACE DEMO COMPLETE")
    print("=" * 80)
    print()

    print("What This Demonstrates:")
    print("  ✅ Natural language questions → Backend reasoning → Conversational answers")
    print("  ✅ Full traceability (citations, reasoning, confidence)")
    print("  ✅ LLM used ONLY for presentation (no hallucination)")
    print("  ✅ Backend provides all legal content from validated 6D logic")
    print()

    print("System Architecture:")
    print("  User Query")
    print("      ↓")
    print("  Conversational Interface")
    print("      ↓")
    print("  Hybrid Search (BM25 + 6D Logic)")
    print("      ↓")
    print("  Formal Reasoning (pre-validated)")
    print("      ↓")
    print("  Claude API (presentation only)")
    print("      ↓")
    print("  Natural Response (with citations)")
    print()


if __name__ == "__main__":
    main()
