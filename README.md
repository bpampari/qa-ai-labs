# 🚀 QA AI Labs – Building Local AI Agents for Quality Engineering

This repository documents a structured, hands-on journey of building practical AI agents for Software Testing using a fully local setup.

The goal was not to use AI tools — but to design and build AI systems.

## 🧠 Project Objective

To design and implement:

- Context-aware AI agents
- Failure-aware automation repair loops
- Local LLM-based assistants
- Guarded AI file rewrite mechanisms
- Telegram-based productivity bots
- Lightweight 24x7 background agents
- All running locally without paid APIs.

## 🏗 System Overview

Everything runs on a single Windows machine acting as a local AI server.

```
                   ┌────────────────────────┐
                   │  Windows PC (Server)   │
                   └───────────┬────────────┘
                               │
        ┌──────────────────────┼──────────────────────┐
        │                      │                      │
 ┌──────▼──────┐       ┌───────▼────────┐      ┌──────▼────────┐
 │ Ollama LLM  │       │ Selenium Java  │      │ Telegram Bot  │
 │ qwen2.5:1.5b │      │ Framework      │      │ API           │
 └──────┬──────┘       └───────┬────────┘      └──────┬────────┘
        │                      │                      │
        │               ┌──────▼──────────┐           │
        │               │ Python AI Agents│───────────┘
        │               └──────┬──────────┘
        │                      │
        │               ┌──────▼────────┐
        │               │ Context Server│
        │               └───────────────┘
```

## 📂 Repository Structure

```
qa-ai-labs/
│
├── selenium-ai-framework/
│   ├── src/test/java/pages/
│   ├── src/test/java/tests/
│   ├── BaseTest.java
│   └── pom.xml
│
├── context-server/
│   └── server.py
│
├── ai-agents/
│   ├── mcp-agent/
│   ├── self-heal-agent/
│   │   └── self_heal.py
│   └── telegram-agent/
│       └── daily_bot.py
│
└── README.md
```


## 🧪 Phase 1 – Local LLM Infrastructure

**We installed:**

- Ollama
- Lightweight model (qwen2.5:1.5b)
- Python requests-based API calls

**Learning:**

- Local models require strict token discipline
- Larger prompts cause timeouts
- Memory constraints matter

## 🤖 Phase 2 – Context-Aware MCP-Style Agent

**Problem**

LLMs hallucinate when they lack project awareness.

**Solution**

- Built a local context server that:
- Reads project files
- Exposes them via HTTP endpoint
- Sends relevant files to LLM

**Flow:**

```
qa-ai-labs/
│
├── selenium-ai-framework/
│   ├── src/test/java/pages/
│   ├── src/test/java/tests/
│   ├── BaseTest.java
│   └── pom.xml
│
├── context-server/
│   └── server.py
│
├── ai-agents/
│   ├── mcp-agent/
│   ├── self-heal-agent/
│   │   └── self_heal.py
│   └── telegram-agent/
│       └── daily_bot.py
│
└── README.md
```

**Learning**

- Sending entire project increases token overload
- Must limit context to relevant files only


## 🔧 Phase 3 – Self-Healing Selenium Prototype

**Objective**

Automatically detect failing Selenium tests and attempt AI-driven repair

```
Run mvn test
      ↓
Detect failure
      ↓
Capture stacktrace
      ↓
Capture page-source.html
      ↓
Send failure + DOM + file to LLM
      ↓
AI generates updated Java class
      ↓
Sanitize output
      ↓
Overwrite file (with validation)
      ↓
Re-run tests

```

**Engineering Challenges Faced**

1️⃣ Token Overload

Full HTML + logs caused LLM timeouts.

Fix:

Trim logs

Trim HTML

Send only relevant file

2️⃣ Markdown Artifacts

AI returned:

java
package pages;


Fix:

Strip ```java blocks

Remove leading “java”

Add structural validation


3️⃣ Missing Imports

AI modified file but removed required imports.

Fix:

Prompt guardrails

Structural keyword validation

4️⃣ Risk of File Corruption

AI could overwrite with invalid content.

Guardrail Added:

```
if not fix_code.strip().startswith("package pages"):
    exit()

```

**Key Insights**

AI is not deterministic.

You must build:

- Validation layer

- Sanitation layer

- Guardrail layer

- Retry strategy

Self-healing is possible — but requires strong control.


## 📬 Phase 4 – Telegram QA Learning Agent

**Objective**

Send daily QA tips using local LLM.

**Flow**

Scheduler Trigger
      ↓
Generate Structured Prompt
      ↓
Call Ollama
      ↓
Send Message via Telegram API

**Features**

Theme rotation

Low token usage

Runs via Task Scheduler

Fully local AI generation


# 👨‍💻 Author

Balakrishna Pampari
Quality Engineer
AI in Testing Practitioner
Building toward AI Automation Architecture
