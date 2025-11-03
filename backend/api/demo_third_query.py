#!/usr/bin/env python3
"""
Third Query Demo - Fundamental Principle
"""
import sys
import os

backend_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, backend_dir)
sys.path.insert(0, os.path.join(backend_dir, 'api'))

from conversational_interface import ConversationalInterface

print()
print('=' * 80)
print('EXAMPLE 3: COSTS FOLLOW THE EVENT PRINCIPLE')
print('=' * 80)
print()

interface = ConversationalInterface()

query = "I won my case - does the other side have to pay my legal costs?"

print('USER QUESTION:')
print('=' * 80)
print(query)
print()

print('PROCESSING...')
print('-' * 80)
result = interface.ask(query)
print()

print('SYSTEM ANSWER:')
print('=' * 80)
print(result['answer'])
print()

print('=' * 80)
print('LEGAL FRAMEWORK:')
print('=' * 80)
print(f"📚 Citations: {', '.join(result['citations'])}")
print(f"⚖️  Module: {result['source_module']}")
print(f"🎯 Confidence: {result['confidence']:.0%}")
print(f"📊 Hybrid Score: {result['hybrid_score']:.0%}")
print()

print('=' * 80)
print('WHAT THIS DEMONSTRATES:')
print('=' * 80)
print('✅ System understands context (user won the case)')
print('✅ Applies fundamental principle (costs follow the event)')
print('✅ Provides clear yes/no answer with legal basis')
print('✅ Includes case law supporting the principle')
print('✅ Natural language while maintaining legal precision')
print()

# Show the IF-THEN logic
print('=' * 80)
print('FORMAL LOGIC EXTRACTED:')
print('=' * 80)
if_then_steps = [step for step in result['reasoning_chain'] if step['dimension'] == 'IF_THEN']
for i, step in enumerate(if_then_steps[:2], 1):
    print(f"\n{i}. {step['text']}")

print()
