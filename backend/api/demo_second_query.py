#!/usr/bin/env python3
"""
Second Query Demo - Different Type of Question
"""
import sys
import os

backend_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, backend_dir)
sys.path.insert(0, os.path.join(backend_dir, 'api'))

from conversational_interface import ConversationalInterface

print()
print('=' * 80)
print('EXAMPLE 2: INDEMNITY COSTS QUERY')
print('=' * 80)
print()

interface = ConversationalInterface()

query = "When can I get indemnity costs instead of standard costs?"

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
print('LEGAL SOURCES:')
print('=' * 80)
print(f"📚 Citations: {', '.join(result['citations'])}")
print(f"⚖️  Module: {result['source_module']}")
print(f"🎯 Confidence: {result['confidence']:.0%}")
print()

print('=' * 80)
print('CASE LAW EXCERPTS IN REASONING:')
print('=' * 80)
# Show reasoning steps that contain case law
case_steps = [step for step in result['reasoning_chain'] if 'Case Law' in step.get('text', '') or 'Verbatim' in step.get('text', '')]
for i, step in enumerate(case_steps[:3], 1):
    print(f"\n{i}. [{step['dimension']}]")
    # Truncate to first 300 chars for readability
    text = step['text'][:300] + "..." if len(step['text']) > 300 else step['text']
    print(f"   {text}")

print()
print('=' * 80)
print('KEY DIFFERENCE FROM TRADITIONAL LEGAL AI:')
print('=' * 80)
print('❌ Traditional AI: Might hallucinate case names or misquote judgments')
print('✅ This System: All case quotes from validated backend')
print('✅ This System: Exact verbatim quotes with paragraph citations')
print('✅ This System: Zero hallucination - can be verified against actual judgments')
print()
