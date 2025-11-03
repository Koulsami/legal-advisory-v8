#!/bin/bash
# Run interactive legal advisory with clarifying questions feature

# Set your Anthropic API key here or source from .env
export ANTHROPIC_API_KEY='your-api-key-here'
/home/claude/legal-advisory-v8/venv/bin/python /home/claude/legal-advisory-v8/backend/api/interactive_with_clarification.py
