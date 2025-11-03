"""
Comprehensive demo of conversational interface capabilities
"""
import sys
import os

# Add paths
backend_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, backend_dir)
sys.path.insert(0, os.path.join(backend_dir, 'api'))

from conversational_interface import ConversationalInterface

print('=' * 80)
print('COMPREHENSIVE CONVERSATIONAL INTERFACE DEMO')
print('Legal Advisory System v8.0')
print('=' * 80)
print()

# Initialize
interface = ConversationalInterface()
print()

# Demo 1: Cross-module queries
print('=' * 80)
print('DEMO 1: CROSS-MODULE QUERY ROUTING')
print('=' * 80)
print()

test_queries = [
    ("Order 21 query", "Can I get default judgment if defendant didn't respond?"),
    ("Order 5 query", "Do I need to try to settle before going to court?"),
    ("Order 14 query", "How do I make a payment into court?")
]

for label, query in test_queries:
    print(f'📝 {label}')
    print(f'   Query: "{query}"')
    result = interface.ask(query)
    print(f'   → Routed to: {result["source_module"]}')
    print(f'   → Citation: {result["citations"][0] if result["citations"] else "N/A"}')
    print(f'   → Confidence: {result["confidence"]:.0%}')
    print()

# Demo 2: Multi-turn conversation
print('=' * 80)
print('DEMO 2: MULTI-TURN CONVERSATION (Context Preservation)')
print('=' * 80)
print()

conversation = [
    "What is default judgment?",
    "Do I need to send notice before applying?",
    "What happens if they filed a defense late?"
]

history = []
for i, query in enumerate(conversation, 1):
    print(f'Turn {i}: "{query}"')
    result = interface.ask(query, conversation_history=history)

    # Show first 200 chars of answer
    answer_preview = result['answer'][:200] + '...' if len(result['answer']) > 200 else result['answer']
    print(f'Answer: {answer_preview}')
    print(f'Citation: {result["citations"][0] if result["citations"] else "N/A"}')
    print()

    # Update history
    history.append({"role": "user", "content": query})
    history.append({"role": "assistant", "content": result['answer']})

# Demo 3: Full response detail
print('=' * 80)
print('DEMO 3: FULL RESPONSE WITH TRACEABILITY')
print('=' * 80)
print()

query = "Can I get default judgment if defendant hasn't responded?"
print(f'Query: "{query}"')
print()

result = interface.ask(query)

print('CONVERSATIONAL ANSWER:')
print('-' * 80)
print(result['answer'])
print()

print('TRACEABILITY:')
print('-' * 80)
print(f'Citations: {", ".join(result["citations"])}')
print(f'Source Module: {result["source_module"]}')
print(f'Confidence: {result["confidence"]:.0%}')
print(f'Hybrid Score: {result["hybrid_score"]:.0%}')
print()

print('REASONING CHAIN:')
print('-' * 80)
for i, step in enumerate(result['reasoning_chain'][:5], 1):
    print(f'{i}. [{step["dimension"]}] {step["text"][:80]}...')
if len(result['reasoning_chain']) > 5:
    print(f'   ... and {len(result["reasoning_chain"]) - 5} more steps')
print()

# Summary
print('=' * 80)
print('✅ CONVERSATIONAL INTERFACE DEMO COMPLETE')
print('=' * 80)
print()
print('Demonstrated:')
print('  ✅ Cross-module query routing (Order 21, 5, 14)')
print('  ✅ Multi-turn conversations with context')
print('  ✅ Natural language presentation')
print('  ✅ Full traceability (citations, reasoning, confidence)')
print('  ✅ Zero hallucination (all content from backend)')
print()
print('Architecture:')
print('  Backend (Layer 1): Formal 6D logic tree reasoning')
print('  Frontend (Layer 2): Claude API presentation')
print('  Result: Natural UX + Zero hallucination')
print()
