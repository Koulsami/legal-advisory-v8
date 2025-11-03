"""
Live test of conversational interface with Claude API
"""

import sys
import os

# Add paths
backend_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, backend_dir)
sys.path.insert(0, os.path.join(backend_dir, 'api'))

from conversational_interface import ConversationalInterface

print('=' * 80)
print('TESTING CONVERSATIONAL INTERFACE WITH CLAUDE API')
print('=' * 80)
print()

# Initialize
print('Initializing conversational interface...')
interface = ConversationalInterface()
print()

# Test query
query = "Can I get default judgment if the defendant did not respond to my lawsuit?"
print(f'QUERY: "{query}"')
print()

# Get response
print('Processing...')
result = interface.ask(query)

print()
print('=' * 80)
print('CONVERSATIONAL RESPONSE:')
print('=' * 80)
print()
print(result['answer'])
print()

print('=' * 80)
print('TRACEABILITY:')
print('=' * 80)
print(f"Citations: {', '.join(result['citations'])}")
print(f"Confidence: {result['confidence']:.0%}")
print(f"Source Module: {result['source_module']}")
print(f"Hybrid Score: {result['hybrid_score']:.0%}")
print(f"Reasoning Steps: {len(result['reasoning_chain'])}")
print()

print('✅ CONVERSATIONAL INTERFACE WORKING!')
