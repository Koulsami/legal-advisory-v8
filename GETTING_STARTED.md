# Getting Started with Legal Advisory System v8.0

Welcome to the v8.0 development! This guide will help you set up your development environment and start implementing the improvements from the ImprovementPlan.md.

---

## 🚀 Quick Start (5 Minutes)

```bash
# 1. Navigate to the project
cd /home/claude/legal-advisory-v8

# 2. Create virtual environment
python3.12 -m venv venv
source venv/bin/activate

# 3. Install dependencies
pip install --upgrade pip
pip install -r requirements.txt

# 4. Set up environment variables
cp .env.example .env
# Edit .env with your actual values

# 5. Start infrastructure
docker-compose up -d

# 6. Wait for services to be healthy (about 30 seconds)
docker-compose ps

# 7. Verify setup
python scripts/verify_setup.py
```

**You're ready to code!** 🎉

---

## 📋 Prerequisites

### Required Software
- ✅ Python 3.12 or higher
- ✅ Docker Desktop (or Docker + Docker Compose)
- ✅ Git
- ✅ 8GB+ RAM available
- ✅ 20GB+ disk space

### Recommended Software
- VSCode or PyCharm
- Postman (for API testing)
- DBeaver (for database management)

### API Keys (for AI features)
- Anthropic Claude API key (get from: https://console.anthropic.com)
- OpenAI API key (optional, for multi-model support)

---

## 🔧 Detailed Setup

### Step 1: Clone or Navigate to Project

```bash
cd /home/claude/legal-advisory-v8
```

### Step 2: Python Environment

```bash
# Create virtual environment
python3.12 -m venv venv

# Activate it
source venv/bin/activate  # Linux/Mac
# OR
venv\Scripts\activate  # Windows

# Upgrade pip
pip install --upgrade pip

# Install dependencies
pip install -r requirements.txt

# Install development dependencies
pip install -r requirements-dev.txt
```

### Step 3: Environment Configuration

```bash
# Copy example environment file
cp .env.example .env

# Edit with your values
nano .env  # or use your favorite editor
```

**Required Updates in .env:**
```
# Update these:
ANTHROPIC_API_KEY=your_actual_key_here
POSTGRES_PASSWORD=strong_password_here
NEO4J_PASSWORD=strong_password_here
SECRET_KEY=generate_with: python -c "import secrets; print(secrets.token_urlsafe(32))"
```

### Step 4: Start Infrastructure

```bash
# Start core services (Elasticsearch, PostgreSQL, Neo4j, Redis)
docker-compose up -d

# Check all services are healthy
docker-compose ps

# Expected output:
# legal-elasticsearch   running (healthy)
# legal-postgres        running (healthy)
# legal-neo4j           running (healthy)
# legal-redis           running (healthy)
```

**If services aren't healthy:**
```bash
# View logs
docker-compose logs -f [service_name]

# Common fixes:
# - Ensure ports 5432, 6379, 7474, 7687, 9200 are not in use
# - Increase Docker memory allocation to 6GB+
# - Wait longer (Neo4j can take 60+ seconds to start)
```

### Step 5: Initialize Databases

```bash
# This script will:
# - Create Elasticsearch indexes with legal analyzer
# - Initialize PostgreSQL schemas
# - Set up Neo4j graph schema
# - Load initial data

python scripts/init_databases.py
```

### Step 6: Verify Setup

```bash
# Run verification script
python scripts/verify_setup.py

# Expected output:
# ✅ Python 3.12.x
# ✅ All dependencies installed
# ✅ Elasticsearch accessible
# ✅ PostgreSQL accessible
# ✅ Neo4j accessible
# ✅ Redis accessible
# ✅ Environment variables set
# ✅ System ready for development!
```

---

## 🏃 Running the Application

### Development Mode

```bash
# Start all services
./scripts/start_dev.sh

# This will start:
# - API server (port 8000)
# - MCP registry (port 8001)
# - MCP retrieval service (port 8002)
# - MCP verification service (port 8003)
# - MCP calculation service (port 8004)

# Access the API:
# - Swagger UI: http://localhost:8000/docs
# - ReDoc: http://localhost:8000/redoc
# - Health Check: http://localhost:8000/health
```

### Running Individual Components

```bash
# Just the API
uvicorn backend.api.main:app --reload --port 8000

# Just the retrieval service
python -m backend.mcp_servers.retrieval.retrieval_server

# Just the verification service
python -m backend.mcp_servers.verification.verification_server
```

---

## 🧪 Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=backend --cov-report=html

# Run specific test file
pytest tests/retrieval/test_three_stage.py

# Run with verbose output
pytest -v

# Run fast tests only (skip slow integration tests)
pytest -m "not slow"
```

---

## 📚 Understanding the Project Structure

### Where to Find Things

**Want to implement Three-Stage Retrieval (Improvement #1)?**
→ Go to: `backend/retrieval/`
→ See: `PROJECT_PLAN.md` Phase 2

**Want to implement Citation Verification (Improvement #2)?**
→ Go to: `backend/verification/`
→ See: `PROJECT_PLAN.md` Phase 3

**Want to implement MCP Microservices (Improvement #3)?**
→ Go to: `backend/mcp_servers/`
→ See: `PROJECT_PLAN.md` Phase 4

**Want to implement Multi-Agent System (Improvement #4)?**
→ Go to: `backend/agents/`
→ See: `PROJECT_PLAN.md` Phase 5

**Want to implement Knowledge Graph (Improvement #5)?**
→ Go to: `backend/knowledge_graph/`
→ See: `PROJECT_PLAN.md` Phase 6

### Key Files

| File | Purpose |
|------|---------|
| `PROJECT_PLAN.md` | 16-week implementation roadmap |
| `README.md` | Project overview and architecture |
| `docker-compose.yml` | Infrastructure setup |
| `backend/config/settings.py` | Configuration |
| `backend/retrieval/three_stage_retrieval.py` | Main retrieval implementation |
| `backend/verification/five_stage_verification.py` | Main verification implementation |

---

## 🎯 What to Work On First

Follow the **PROJECT_PLAN.md** timeline:

**Week 1-2 (Foundation):** ✅ SETUP COMPLETE
- [x] Project structure
- [x] Docker infrastructure
- [ ] Basic API framework
- [ ] Copy Order 21 module from v6.5

**Week 3-4 (Three-Stage Retrieval):** NEXT UP
- [ ] Set up Elasticsearch with legal analyzer
- [ ] Implement BM25 retrieval
- [ ] Implement semantic search with Legal-BERT
- [ ] Integrate all three stages

**See PROJECT_PLAN.md for complete roadmap.**

---

## 🔍 Accessing Services

### Web UIs

| Service | URL | Credentials |
|---------|-----|-------------|
| API Docs (Swagger) | http://localhost:8000/docs | N/A |
| Neo4j Browser | http://localhost:7474 | neo4j / [your password] |
| Elasticsearch | http://localhost:9200 | N/A |
| Kibana (optional) | http://localhost:5601 | N/A (run with --profile monitoring) |

### Command Line Access

```bash
# Elasticsearch
curl http://localhost:9200

# PostgreSQL
psql -h localhost -U legal_user -d legal_advisory_v8

# Neo4j (Cypher Shell)
docker exec -it legal-neo4j cypher-shell -u neo4j -p [your password]

# Redis
redis-cli
```

---

## 🐛 Troubleshooting

### Port Already in Use

```bash
# Find what's using the port
lsof -i :9200  # or :5432, :7687, etc.

# Kill the process or change the port in docker-compose.yml
```

### Docker Out of Memory

```bash
# Increase Docker memory allocation:
# Docker Desktop → Settings → Resources → Memory → 8GB+
```

### Elasticsearch Won't Start

```bash
# Check logs
docker-compose logs -f elasticsearch

# Common issue: vm.max_map_count too low
# Fix:
sysctl -w vm.max_map_count=262144
```

### Dependencies Won't Install

```bash
# Make sure you're in virtual environment
which python  # Should show venv/bin/python

# Upgrade pip
pip install --upgrade pip setuptools wheel

# Install dependencies one by one to find the problematic one
pip install -r requirements.txt --verbose
```

### Can't Connect to Neo4j

```bash
# Neo4j takes longer to start (60+ seconds)
# Wait and check logs:
docker-compose logs -f neo4j

# If still failing, try:
docker-compose down
docker volume rm legal-advisory-v8_neo4j_data
docker-compose up -d neo4j
```

---

## 📖 Next Steps

1. **Read the improvement plan:**
   - `/mnt/c/Users/Samee/Downloads/ImprovementPlan.md`

2. **Review the project plan:**
   - `PROJECT_PLAN.md` - 16-week roadmap

3. **Understand the architecture:**
   - `README.md` - Architecture overview
   - `docs/architecture/` - Detailed design docs

4. **Start coding:**
   - Follow `PROJECT_PLAN.md` Phase 2 (Three-Stage Retrieval)
   - Write tests first (TDD)
   - Commit frequently

5. **Join daily standups:**
   - Review progress
   - Plan daily tasks
   - Ask for help when stuck

---

## 🤝 Getting Help

### Documentation
- `README.md` - Project overview
- `PROJECT_PLAN.md` - Implementation roadmap
- `docs/` - Detailed documentation
- `/mnt/c/Users/Samee/Downloads/ImprovementPlan.md` - Original improvement plan

### Common Questions

**Q: Where is v6.5?**
A: Still at `/home/claude/legal-advisory-v5` - unchanged and stable

**Q: Can I run both v6.5 and v8.0?**
A: Yes! They're completely separate projects. v8.0 uses different ports.

**Q: How do I know if I'm making progress?**
A: Run `pytest` frequently. Green tests = working code.

**Q: What if I break something?**
A: Git is your friend! `git diff` to see changes, `git checkout -- file` to revert.

**Q: Should I implement everything at once?**
A: NO! Follow the phased approach in PROJECT_PLAN.md. One improvement at a time.

---

## ✅ Pre-Development Checklist

Before you start coding, ensure:

- [ ] Virtual environment activated (`which python` shows venv/bin/python)
- [ ] All dependencies installed (`pip list` shows packages)
- [ ] Docker services running (`docker-compose ps` all healthy)
- [ ] Environment variables set (`.env` file exists and configured)
- [ ] Databases initialized (`python scripts/init_databases.py` completed)
- [ ] Tests passing (`pytest` runs successfully)
- [ ] Can access API docs (http://localhost:8000/docs loads)

**All checked?** You're ready to build v8.0! 🚀

---

**Welcome to the team! Let's build something amazing.** 🎉
