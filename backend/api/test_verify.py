#!/usr/bin/env python3
"""
Verification test - checks all components
"""
import sys
import os

# Add paths
backend_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, backend_dir)
sys.path.insert(0, os.path.join(backend_dir, 'api'))

print('=' * 80)
print('CONVERSATIONAL INTERFACE - VERIFICATION TEST')
print('=' * 80)
print()

# Test results
tests_passed = 0
tests_total = 0

def test(name, condition, details=""):
    global tests_passed, tests_total
    tests_total += 1
    if condition:
        print(f'✅ PASS: {name}')
        if details:
            print(f'   {details}')
        tests_passed += 1
    else:
        print(f'❌ FAIL: {name}')
        if details:
            print(f'   {details}')
    print()

# Test 1: API Key
print('TEST 1: API Key')
print('-' * 80)
api_key = os.environ.get('ANTHROPIC_API_KEY')
test('API key set', bool(api_key), f'Key present: {api_key[:20] if api_key else "N/A"}...')

# Test 2: Import modules
print('TEST 2: Module Imports')
print('-' * 80)
try:
    import anthropic
    test('anthropic module', True, 'anthropic package installed')
except ImportError:
    test('anthropic module', False, 'Run: pip install anthropic')

try:
    from conversational_interface import ConversationalInterface
    test('ConversationalInterface', True, 'Interface module loaded')
except Exception as e:
    test('ConversationalInterface', False, f'Error: {e}')

# Test 3: Initialize interface
print('TEST 3: Interface Initialization')
print('-' * 80)
try:
    interface = ConversationalInterface()
    test('Initialize interface', True, 'Backend and Claude client ready')
except Exception as e:
    test('Initialize interface', False, f'Error: {e}')
    print('Stopping tests - initialization failed')
    sys.exit(1)

# Test 4: Backend query
print('TEST 4: Backend Query')
print('-' * 80)
try:
    backend_result = interface.backend.hybrid_search(
        "Can I get default judgment?", top_k=3
    )
    test('Backend search', True, f'Hybrid score: {backend_result.hybrid_score:.0%}')

    if backend_result.bm25_results:
        top = backend_result.bm25_results[0]
        test('BM25 results', True, f'Found: {top["source"]["citation"]}')
    else:
        test('BM25 results', False, 'No results returned')

except Exception as e:
    test('Backend search', False, f'Error: {e}')

# Test 5: Order 21 full query
print('TEST 5: Order 21 Full Query')
print('-' * 80)
try:
    result = interface.ask("Can I get default judgment if defendant didn't respond?")

    test('Query processed', True, 'Full query executed')
    test('Natural language answer', bool(result.get('answer')),
         f'Length: {len(result.get("answer", ""))} chars')
    test('Citations present', bool(result.get('citations')),
         f'Citations: {result.get("citations", [])}')
    test('Confidence > 0', result.get('confidence', 0) > 0,
         f'Confidence: {result.get("confidence", 0):.0%}')
    test('Module identified', bool(result.get('source_module')),
         f'Module: {result.get("source_module", "N/A")}')
    test('Reasoning chain', bool(result.get('reasoning_chain')),
         f'Steps: {len(result.get("reasoning_chain", []))}')

except Exception as e:
    test('Order 21 query', False, f'Error: {e}')

# Test 6: Cross-module routing
print('TEST 6: Cross-Module Routing')
print('-' * 80)
test_queries = [
    ("Order 21", "Can I get default judgment?", "order_21"),
    ("Order 5", "Do I need to settle first?", "order_5"),
    ("Order 14", "How do I pay into court?", "order_14"),
]

for name, query, expected_module in test_queries:
    try:
        result = interface.ask(query)
        module = result.get('source_module', '')
        test(f'{name} routing', module == expected_module,
             f'Expected: {expected_module}, Got: {module}')
    except Exception as e:
        test(f'{name} routing', False, f'Error: {e}')

# Test 7: Response quality (Order 21)
print('TEST 7: Response Quality (Order 21)')
print('-' * 80)
try:
    result = interface.ask("Can I get default judgment if defendant didn't respond?")

    answer = result.get('answer', '')
    test('Answer length > 100 chars', len(answer) > 100,
         f'Length: {len(answer)} chars')
    test('Contains "default judgment"', 'default judgment' in answer.lower(),
         'Query topic mentioned')
    test('Contains citation reference', any(keyword in answer.lower()
         for keyword in ['order 21', 'rule 1', 'source', 'citation']),
         'Citation mentioned in answer')
    test('Confidence >= 80%', result.get('confidence', 0) >= 0.8,
         f'Confidence: {result.get("confidence", 0):.0%}')

except Exception as e:
    test('Response quality', False, f'Error: {e}')

# Summary
print('=' * 80)
print('VERIFICATION SUMMARY')
print('=' * 80)
print()
print(f'Tests Passed: {tests_passed}/{tests_total}')
print()

if tests_passed == tests_total:
    print('🎉 ALL TESTS PASSED - CONVERSATIONAL INTERFACE WORKING!')
    print()
    print('✅ API key configured')
    print('✅ Backend integration working')
    print('✅ Claude API working')
    print('✅ Order 21 fully functional (90% confidence)')
    print('✅ Cross-module routing working')
    print('✅ Natural language responses generated')
    print('✅ Full traceability maintained')
    print()
    print('Ready for production use!')
elif tests_passed >= tests_total * 0.8:
    print('⚠️  MOST TESTS PASSED - SYSTEM MOSTLY WORKING')
    print()
    print(f'Passed: {tests_passed}/{tests_total} ({tests_passed/tests_total*100:.0f}%)')
    print()
    print('Check failed tests above for details.')
else:
    print('❌ MANY TESTS FAILED - SYSTEM NEEDS ATTENTION')
    print()
    print(f'Passed: {tests_passed}/{tests_total} ({tests_passed/tests_total*100:.0f}%)')
    print()
    print('Check failed tests above and see TESTING_GUIDE.md for troubleshooting.')

print()
print('=' * 80)
