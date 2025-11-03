#!/usr/bin/env python3
"""
Demo: Enhanced Case Law Presentation
Shows case law with reasoning summaries and verbatim quotes for verification
"""
import sys
import os

backend_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, backend_dir)
sys.path.insert(0, os.path.join(backend_dir, 'api'))

from conversational_interface import ConversationalInterface

print()
print('=' * 80)
print('ENHANCED CASE LAW PRESENTATION DEMO')
print('=' * 80)
print()
print('This demonstrates how the system now presents case law with:')
print('  1. Summary of the case reasoning')
print('  2. Verbatim quote from the judgment')
print('  3. Paragraph citation for verification')
print()

interface = ConversationalInterface()

# Test with indemnity costs question (has case law)
print('=' * 80)
print('EXAMPLE: INDEMNITY COSTS QUESTION')
print('=' * 80)
print()

question = "When can I get indemnity costs instead of standard costs?"

print(f'USER QUESTION:')
print(f'  {question}')
print()

result = interface.ask(question)

if not result.get('needs_clarification'):
    print('=' * 80)
    print('SYSTEM ANSWER:')
    print('=' * 80)
    print(result['answer'])
    print()

    print('=' * 80)
    print('TRACEABILITY:')
    print('=' * 80)
    print(f"📚 Citations: {', '.join(result['citations'][:3])}")
    print(f"🎯 Confidence: {result['confidence']:.0%}")
    print(f"⚖️  Module: {result['source_module']}")
    print()

    # Show raw reasoning chain with case law
    print('=' * 80)
    print('RAW REASONING CHAIN (First 10 Steps):')
    print('=' * 80)
    print()

    case_law_count = 0
    verbatim_count = 0

    for i, step in enumerate(result['reasoning_chain'][:15], 1):
        if 'Case Law' in step['text']:
            case_law_count += 1
            print(f"{i}. [Case Law Summary]")
            print(f"   {step['text'][:300]}...")
            print(f"   📖 {step.get('source', 'N/A')}")
            print()
        elif 'Verbatim Quote' in step['text']:
            verbatim_count += 1
            print(f"{i}. [Verbatim Quote from Judgment]")
            print(f"   {step['text'][:300]}...")
            print(f"   📖 {step.get('source', 'N/A')}")
            print()

    print('=' * 80)
    print(f'CASE LAW ELEMENTS DETECTED:')
    print('=' * 80)
    print(f'  Case Law Summaries: {case_law_count}')
    print(f'  Verbatim Quotes: {verbatim_count}')
    print()

print('=' * 80)
print('KEY FEATURES:')
print('=' * 80)
print()
print('✅ Case law presented with reasoning summary')
print('✅ Verbatim quotes shown for verification')
print('✅ Paragraph citations included (e.g., [Paragraph 23-24])')
print('✅ User can verify quotes against actual judgments')
print('✅ Multiple layers of verification')
print()
print('This allows users and lawyers to:')
print('  • See WHY the case applies (reasoning summary)')
print('  • Verify WHAT the court actually said (verbatim quote)')
print('  • Check WHERE in the judgment (paragraph number)')
print()
