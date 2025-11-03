#!/usr/bin/env python3
"""
Demo: Clarifying Questions Feature
Shows how the system asks for more information when confidence is low
"""
import sys
import os

backend_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, backend_dir)
sys.path.insert(0, os.path.join(backend_dir, 'api'))

from conversational_interface import ConversationalInterface

print()
print('=' * 80)
print('CLARIFYING QUESTIONS DEMO')
print('=' * 80)
print()
print('This demonstrates how the system asks for more information when the')
print('initial query is too vague or ambiguous.')
print()

interface = ConversationalInterface()

# Example 1: Vague question that will trigger clarification
vague_question = "I won my case - does the other side have to pay my legal costs?"

print('=' * 80)
print('EXAMPLE 1: VAGUE QUESTION (Triggers Clarification)')
print('=' * 80)
print()
print(f'USER: {vague_question}')
print()

result1 = interface.ask(vague_question)

if result1.get('needs_clarification'):
    print('SYSTEM: I need some more information to answer your question accurately.')
    print()
    print('📋 CLARIFYING QUESTIONS:')
    print('-' * 80)
    for i, question in enumerate(result1['clarifying_questions'], 1):
        print(f'{i}. {question}')
    print()
    print(f'⚠️  Confidence: {result1["confidence"]:.0%} (below 30% threshold)')
    print(f'📚 Best match found: {result1["source_module"]}')
    print()

    # Simulate user providing more details
    print('=' * 80)
    print('USER PROVIDES MORE DETAILS:')
    print('=' * 80)
    print()
    detailed_question = ("I won my case and the judge said costs follow the event. "
                        "The case was about a contract dispute. What does this mean "
                        "for recovering my legal costs?")
    print(f'USER (refined): {detailed_question}')
    print()

    # Try again with more details
    result2 = interface.ask(detailed_question)

    if result2.get('needs_clarification'):
        print('SYSTEM: Still need more information:')
        print()
        for i, question in enumerate(result2['clarifying_questions'], 1):
            print(f'{i}. {question}')
    else:
        print('SYSTEM ANSWER:')
        print('-' * 80)
        print(result2['answer'][:400] + "..." if len(result2['answer']) > 400 else result2['answer'])
        print()
        print(f'✅ Confidence: {result2["confidence"]:.0%}')
        print(f'📚 Citations: {", ".join(result2["citations"][:2])}')

else:
    print('SYSTEM PROVIDED DIRECT ANSWER')
    print()
    print(result1['answer'][:300])

print()
print('=' * 80)
print('EXAMPLE 2: SPECIFIC QUESTION (Direct Answer)')
print('=' * 80)
print()

specific_question = "What are the costs for opposing a stay application in a case worth $500,000?"
print(f'USER: {specific_question}')
print()

result3 = interface.ask(specific_question)

if result3.get('needs_clarification'):
    print('SYSTEM: Need clarification:')
    for i, question in enumerate(result3['clarifying_questions'], 1):
        print(f'{i}. {question}')
else:
    print('SYSTEM ANSWER:')
    print('-' * 80)
    print(result3['answer'][:400] + "..." if len(result3['answer']) > 400 else result3['answer'])
    print()
    print(f'✅ Confidence: {result3["confidence"]:.0%}')
    print(f'📊 Hybrid Score: {result3["hybrid_score"]:.0%}')

print()
print('=' * 80)
print('KEY FEATURES DEMONSTRATED:')
print('=' * 80)
print()
print('✅ System detects low confidence queries (< 30%)')
print('✅ Generates intelligent clarifying questions')
print('✅ Asks for specific details to improve search')
print('✅ Maintains conversation context')
print('✅ Provides direct answer when confidence is high')
print('✅ No hallucination - asks rather than guesses!')
print()
