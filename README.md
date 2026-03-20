# ChaosGPT 2.0: Autonomous AI Agent Implementation

![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)
![Model: Llama-3.2-1b](https://img.shields.io/badge/Model-Llama--3.2--1b-blue)
![Engine: Ollama](https://img.shields.io/badge/Engine-Ollama-orange)
![Vision: Supported](https://img.shields.io/badge/Vision-Enabled-green)

## 🤖 Project Overview
This repository features an autonomous implementation of **ChaosGPT 2.0**, optimized for local execution using the **Llama 3.2:1b** model via **Ollama**. Unlike standard chat interfaces, ChaosGPT 2.0 operates within a continuous "Thought-Action-Observation" loop, enabling it to achieve complex objectives without requiring constant human intervention.

Now updated with **Computer Vision capabilities**, the agent can perceive its environment and interact with the desktop interface directly.

> [!IMPORTANT]
> **Disclaimer:** This project is intended strictly for educational and research purposes regarding AI autonomy. Use responsibly.

---

## 🚀 Key Features in v2.0

### 👁️ Vision & Desktop Control
ChaosGPT 2.0 now features **Visual Grounding**. The agent can:
* **Analyze Screenshots:** "See" the current state of your desktop or specific applications.
* **Mouse Control:** Identify UI elements (buttons, icons, text fields) and calculate coordinates to perform clicks, drags, and movements.
* **Real-time Feedback:** Use visual confirmation to verify if an action (like clicking a "Submit" button) was successful.

### 🧠 Advanced Reasoning (Tree of Thoughts)
ChaosGPT 2.0 goes beyond simple word prediction; it explores multiple reasoning paths, evaluating the success probability of each step before execution.

### 💾 Long-Term Memory (RAG Integration)
Integrated with a **Vector Database**, the agent can:
* Store and index information from web searches.
* Recall previous errors to avoid repetition.
* Maintain context across sessions lasting multiple days.

### 🛠️ Native Tool Access
The agent is equipped with a suite of local tools:
* **Web Browser:** For real-time information gathering.
* **Terminal/Shell:** To execute Python scripts in a secure, sandboxed environment.
* **File Manager:** For reading and writing local documentation and logs.

---

## 🛠️ Technical Stack
* **LLM:** Meta Llama 3.2 (1 Billion parameters) — *Fast, lightweight, and local.*
* **Vision Engine:** Integrated Screenshot Analysis Module.
* **Runtime:** [Ollama](https://ollama.ai/)
* **Architecture:** Agentic Workflow (Self-Correction & Reflection)
* **Memory:** Vector Embeddings for persistent storage.

---

## 📋 How to Run Locally

1. **Install Ollama:**
   Download and install from [ollama.com](https://ollama.com).

2. **Pull the Model:**
   ```bash
   ollama run llama3.2:1b
