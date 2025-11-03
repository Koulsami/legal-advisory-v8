# Quick Test - Conversational Interface ⚡

**Problem?** If you get "ModuleNotFoundError: No module named 'elasticsearch'", use the helper scripts below!

---

## 🚀 Easiest Way: Use Helper Scripts

```bash
cd /home/claude/legal-advisory-v8/backend/api

# Option 1: Run verification (19 automated tests)
./run_test_verify.sh

# Option 2: Run single query test
./run_test_live.sh

# Option 3: Run comprehensive demo
./run_demo.sh

# Option 4: Interactive testing (your own queries)
./run_interactive.sh
```

These scripts automatically:
- ✅ Use the correct Python (venv)
- ✅ Set the API key
- ✅ Handle all paths correctly

---

## 🔧 Manual Testing (If Scripts Don't Work)

### Method 1: Use Full Python Path
```bash
export ANTHROPIC_API_KEY='your-api-key-here'
cd /home/claude/legal-advisory-v8/backend/api
/home/claude/legal-advisory-v8/venv/bin/python test_verify.py
```

### Method 2: Fix Venv Activation
```bash
# Deactivate if already in venv
deactivate

# Properly activate venv
source /home/claude/legal-advisory-v8/venv/bin/activate

# Verify correct Python
which python
# Should show: /home/claude/legal-advisory-v8/venv/bin/python

# Set API key
export ANTHROPIC_API_KEY='your-api-key-here'

# Run test
python test_verify.py
```

---

## ✅ Expected Output

**When working correctly:**
```
================================================================================
CONVERSATIONAL INTERFACE - VERIFICATION TEST
================================================================================

TEST 1: API Key
✅ PASS: API key set

TEST 2: Module Imports
✅ PASS: anthropic module
✅ PASS: ConversationalInterface

[... more tests ...]

Tests Passed: 19/19

🎉 ALL TESTS PASSED - CONVERSATIONAL INTERFACE WORKING!
```

---

## 🐛 Troubleshooting

**Error: "ModuleNotFoundError: No module named 'elasticsearch'"**
- **Cause:** Using system Python instead of venv Python
- **Fix:** Use helper scripts (./run_test_verify.sh) or full Python path

**Error: "permission denied: ./run_test_verify.sh"**
- **Fix:** `chmod +x /home/claude/legal-advisory-v8/backend/api/run_*.sh`

**Error: "ANTHROPIC_API_KEY not set"**
- **Fix:** Already set in helper scripts. If using manual method, export the key.

---

## 📝 Test Queries to Try (Interactive Mode)

Run `./run_interactive.sh` then try:

```
✅ "Can I get default judgment if defendant didn't respond?"
✅ "Do I need to send notice first?"
✅ "What is the time limit for filing a defense?"
✅ "Do I need to settle before going to court?"
✅ "How do I make a payment into court?"
```

Type `quit` to exit.

---

## 📚 Available Helper Scripts

```bash
./run_test_verify.sh    # ⚡ Automated verification (19 tests)
./run_test_live.sh      # 📝 Single query test
./run_demo.sh           # 🎯 Full feature demo
./run_interactive.sh    # 💬 Interactive Q&A
```

All scripts handle venv Python and API key automatically!

---

## 🎯 Quick Test (Copy-Paste)

```bash
cd /home/claude/legal-advisory-v8/backend/api && ./run_test_verify.sh
```

**Expected:** ✅ 19/19 tests passed

---

**Bottom Line:** Just run `./run_test_verify.sh` from the api directory! 🎉
