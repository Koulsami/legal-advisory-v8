#!/usr/bin/env python3
"""
Interactive testing of conversational interface
"""
import sys
import os

# Add paths
backend_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, backend_dir)
sys.path.insert(0, os.path.join(backend_dir, 'api'))

from conversational_interface import ConversationalInterface

print('=' * 80)
print('INTERACTIVE CONVERSATIONAL INTERFACE TEST')
print('=' * 80)
print()

# Initialize
print('Initializing...')
interface = ConversationalInterface()
print('✅ Ready!')
print()

print('You can now ask legal questions. Type "quit" to exit.')
print()
print('Example questions:')
print('  - Can I get default judgment if defendant did not respond?')
print('  - Do I need to settle before going to court?')
print('  - How do I make a payment into court?')
print()

# Conversation history
history = []

while True:
    print('-' * 80)
    query = input('Your question: ').strip()

    if query.lower() in ['quit', 'exit', 'q']:
        print('Goodbye!')
        break

    if not query:
        continue

    print()
    print('Processing...')

    try:
        # Ask question
        result = interface.ask(query, conversation_history=history)

        print()
        print('=' * 80)
        print('ANSWER:')
        print('=' * 80)
        print()
        print(result['answer'])
        print()

        print('=' * 80)
        print('METADATA:')
        print('=' * 80)
        print(f"Citations: {', '.join(result['citations']) if result['citations'] else 'N/A'}")
        print(f"Confidence: {result['confidence']:.0%}")
        print(f"Module: {result['source_module']}")
        print(f"Hybrid Score: {result['hybrid_score']:.0%}")
        print(f"Reasoning Steps: {len(result['reasoning_chain'])}")
        print()

        # Update history
        history.append({"role": "user", "content": query})
        history.append({"role": "assistant", "content": result['answer']})

    except Exception as e:
        print(f'❌ Error: {e}')
        print()
