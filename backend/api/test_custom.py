#!/usr/bin/env python3
"""
Custom test script - modify queries as needed
"""
import sys
import os

# Add paths
backend_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, backend_dir)
sys.path.insert(0, os.path.join(backend_dir, 'api'))

from conversational_interface import ConversationalInterface

print('=' * 80)
print('CUSTOM TEST QUERIES')
print('=' * 80)
print()

# Initialize
interface = ConversationalInterface()
print()

# ADD YOUR TEST QUERIES HERE
test_queries = [
    "Can I get default judgment if the defendant didn't respond?",
    # Add more queries below:
    # "Do I need to send notice before applying for default judgment?",
    # "What is the time limit for filing a defense?",
    # "Can the court set aside a default judgment?",
]

# Run tests
for i, query in enumerate(test_queries, 1):
    print(f'TEST {i}/{len(test_queries)}')
    print('=' * 80)
    print(f'Query: "{query}"')
    print()

    result = interface.ask(query)

    # Display answer
    print('ANSWER:')
    print('-' * 80)
    print(result['answer'])
    print()

    # Display metadata
    print('METADATA:')
    print('-' * 80)
    print(f"✅ Citations: {', '.join(result['citations']) if result['citations'] else 'N/A'}")
    print(f"✅ Confidence: {result['confidence']:.0%}")
    print(f"✅ Module: {result['source_module']}")
    print(f"✅ Hybrid Score: {result['hybrid_score']:.0%}")
    print(f"✅ Reasoning Steps: {len(result['reasoning_chain'])}")
    print()

    # Display reasoning chain (first 3 steps)
    if result['reasoning_chain']:
        print('REASONING CHAIN (first 3 steps):')
        print('-' * 80)
        for j, step in enumerate(result['reasoning_chain'][:3], 1):
            print(f"{j}. [{step['dimension']}] {step['text'][:100]}...")
        if len(result['reasoning_chain']) > 3:
            print(f"   ... and {len(result['reasoning_chain']) - 3} more steps")
        print()

    print()

print('=' * 80)
print(f'✅ COMPLETED {len(test_queries)} TESTS')
print('=' * 80)
