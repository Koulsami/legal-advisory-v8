#!/bin/bash
# Show the actual conversational answer

# Set your Anthropic API key here or source from .env
export ANTHROPIC_API_KEY='your-api-key-here'
/home/claude/legal-advisory-v8/venv/bin/python /home/claude/legal-advisory-v8/backend/api/show_answer.py
