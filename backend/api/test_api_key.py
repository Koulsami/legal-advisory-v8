"""
Test Anthropic API key and available models
"""
import anthropic
import os

api_key = os.environ.get('ANTHROPIC_API_KEY')
print(f"API Key present: {bool(api_key)}")
print(f"API Key starts with: {api_key[:20] if api_key else 'N/A'}...")
print()

try:
    client = anthropic.Anthropic(api_key=api_key)
    print("✅ Client initialized successfully")
    print()

    # Try a simple message with different model names
    test_models = [
        "claude-3-5-sonnet-20241022",
        "claude-3-5-sonnet-20240620",
        "claude-3-sonnet-20240229",
        "claude-3-opus-20240229",
        "claude-3-haiku-20240307",
        "claude-2.1",
        "claude-2"
    ]

    for model in test_models:
        try:
            print(f"Testing model: {model}")
            response = client.messages.create(
                model=model,
                max_tokens=10,
                messages=[{"role": "user", "content": "Hi"}]
            )
            print(f"✅ SUCCESS with model: {model}")
            print(f"   Response: {response.content[0].text}")
            break
        except anthropic.NotFoundError as e:
            print(f"❌ 404 Not Found: {model}")
        except Exception as e:
            print(f"❌ Error with {model}: {type(e).__name__}: {str(e)}")

except Exception as e:
    print(f"❌ Failed to initialize client: {e}")
