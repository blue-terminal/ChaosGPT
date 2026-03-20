# ChaosGPT 2.0: Autonomous AI Agent Implementation

![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)
![Model: Llama-3.2-1b](https://img.shields.io/badge/Model-Llama--3.2--1b-blue)
![Engine: Ollama](https://img.shields.io/badge/Engine-Ollama-orange)

## 🤖 Project Overview
This repository contains an autonomous implementation of **ChaosGPT 2.0**, optimized to run locally using the **Llama 3.2:1b** model via **Ollama**. Unlike standard chat interfaces, ChaosGPT 2.0 operates in a continuous "Thought-Action-Observation" loop to achieve complex goals without constant human prompting.

> **Disclaimer:** This project is for educational and research purposes regarding AI autonomy. Use responsibly.

---

## 🚀 Key Features in v2.0

### 🧠 Advanced Reasoning (Tree of Thoughts)
ChaosGPT 2.0 doesn't just predict the next word; it explores multiple reasoning paths, evaluating the success probability of each step before execution.

### 💾 Long-Term Memory (RAG Integration)
Integrated with a **Vector Database**, the agent can:
* Store information from web searches.
* Recall previous errors to avoid repeating them.
* Maintain context over sessions lasting days.

### 🛠️ Native Tool Access
The agent is equipped with a suite of local tools:
* **Web Browser:** Real-time information gathering.
* **Terminal/Shell:** Executing Python scripts in a sandboxed environment.
* **File Manager:** Reading and writing local documentation.

---

## 🛠️ Technical Stack
* **LLM:** Meta Llama 3.2 (1 Billion parameters) — *Fast, lightweight, and local.*
* **Runtime:** [Ollama](https://ollama.ai/)
* **Architecture:** Agentic Workflow (Self-Correction & Reflection)
* **Memory:** Vector Embeddings for persistent storage.

---

## 📋 How to Run Locally

1. **Install Ollama:**
   Download from [ollama.com](https://ollama.com).

2. **Pull the Model:**
   ```bash
   ollama run llama3.2:1b
