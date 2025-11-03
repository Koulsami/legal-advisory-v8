#!/usr/bin/env python3
"""
Show the actual conversational answer clearly
"""
import sys
import os

# Add paths
backend_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, backend_dir)
sys.path.insert(0, os.path.join(backend_dir, 'api'))

from conversational_interface import ConversationalInterface

print()
print('=' * 80)
print('CONVERSATIONAL LEGAL ADVISORY - DEMO')
print('=' * 80)
print()

# Initialize
interface = ConversationalInterface()
print()

# Ask a question
query = "Can I get default judgment if the defendant did not respond to my lawsuit?"

print('QUESTION:')
print('-' * 80)
print(query)
print()

# Get answer
print('Processing...')
print()
result = interface.ask(query)

# Show the conversational answer
print()
print('=' * 80)
print('CONVERSATIONAL ANSWER:')
print('=' * 80)
print()
print(result['answer'])
print()

# Show traceability
print('=' * 80)
print('LEGAL SOURCES & TRACEABILITY:')
print('=' * 80)
print()
print(f"📚 Citation: {', '.join(result['citations']) if result['citations'] else 'N/A'}")
print(f"⚖️  Source Module: {result['source_module']}")
print(f"🎯 Confidence: {result['confidence']:.0%}")
print(f"📊 Hybrid Score: {result['hybrid_score']:.0%}")
print(f"🔗 Reasoning Steps: {len(result['reasoning_chain'])}")
print()

# Show reasoning chain
if result['reasoning_chain']:
    print('=' * 80)
    print('REASONING CHAIN (Formal Logic):')
    print('=' * 80)
    print()
    for i, step in enumerate(result['reasoning_chain'][:5], 1):
        print(f"{i}. [{step['dimension']}]")
        print(f"   {step['text']}")
        print()

    if len(result['reasoning_chain']) > 5:
        print(f"   ... and {len(result['reasoning_chain']) - 5} more steps")
        print()

print('=' * 80)
print('✅ DEMO COMPLETE')
print('=' * 80)
print()
print('What you just saw:')
print('  1. Natural language question')
print('  2. Conversational answer (formatted by Claude)')
print('  3. Full legal citations and sources')
print('  4. Formal reasoning chain from backend')
print()
print('Key Point: The legal content comes from the validated backend,')
print('Claude only formatted it to be conversational!')
print()
