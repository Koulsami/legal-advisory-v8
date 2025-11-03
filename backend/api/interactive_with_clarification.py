#!/usr/bin/env python3
"""
Interactive Legal Advisory with Clarifying Questions
Maintains conversation context and asks for more information when needed
"""
import sys
import os

backend_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, backend_dir)
sys.path.insert(0, os.path.join(backend_dir, 'api'))

from conversational_interface import ConversationalInterface

def print_header(text):
    """Print formatted header."""
    print()
    print('=' * 80)
    print(text)
    print('=' * 80)
    print()

def print_section(title):
    """Print section divider."""
    print()
    print(f'--- {title} ---')
    print()

print_header('INTERACTIVE LEGAL ADVISORY WITH CLARIFYING QUESTIONS')

print('This is an enhanced legal advisory system that:')
print('  • Asks clarifying questions when your query is vague')
print('  • Maintains conversation context across multiple turns')
print('  • Provides specific answers when confidence is high')
print('  • Never hallucinates - asks rather than guesses')
print()
print('Type "quit" or "exit" to end the session.')
print()

# Initialize interface
interface = ConversationalInterface()

# Conversation history
conversation_history = []
context = {}

while True:
    print()
    user_input = input('YOU: ').strip()

    if not user_input:
        continue

    if user_input.lower() in ['quit', 'exit', 'q']:
        print()
        print('Thank you for using the Legal Advisory System!')
        print()
        break

    # Get response from system
    result = interface.ask(user_input, conversation_history)

    # Check if system needs clarification
    if result.get('needs_clarification'):
        print()
        print('SYSTEM: I need some more information to answer your question accurately.')
        print()
        print('Please provide details about:')
        print()

        for i, question in enumerate(result['clarifying_questions'], 1):
            print(f'  {i}. {question}')

        print()
        print(f'💡 TIP: You can answer one or more of these questions, or rephrase')
        print(f'        your original question with more specific details.')
        print()
        print(f'📊 Current confidence: {result["confidence"]:.0%} (need >30% for direct answer)')

        # Store context for next turn
        context['previous_question'] = user_input
        context['clarifying_questions'] = result['clarifying_questions']

        # Add to conversation history
        conversation_history.append({
            "role": "user",
            "content": user_input
        })
        conversation_history.append({
            "role": "assistant",
            "content": f"I need clarification. Questions: {'; '.join(result['clarifying_questions'])}"
        })

    else:
        # System provided answer
        print()
        print('SYSTEM:')
        print('-' * 80)
        print(result['answer'])
        print()
        print('-' * 80)
        print(f'📚 Sources: {", ".join(result["citations"][:2])}')
        print(f'🎯 Confidence: {result["confidence"]:.0%}')
        print(f'📊 Hybrid Score: {result["hybrid_score"]:.0%}')

        # Add to conversation history
        conversation_history.append({
            "role": "user",
            "content": user_input
        })
        conversation_history.append({
            "role": "assistant",
            "content": result['answer']
        })

        # Clear context
        context = {}

        # Limit conversation history to last 6 messages (3 turns)
        if len(conversation_history) > 6:
            conversation_history = conversation_history[-6:]

print()
