# ChaosGPT 2.0: Autonomous AI Agent (Ollama Edition)

![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)
![Model: Llama-3.2-1b](https://img.shields.io/badge/Model-Llama--3.2--1b-blue)
![Engine: Ollama](https://img.shields.io/badge/Engine-Ollama-orange)
![Capability: Computer Control](https://img.shields.io/badge/Control-Mouse%20%26%20Keyboard-red)

## 🤖 Project Overview
ChaosGPT 2.0 is a high-speed, autonomous agent designed to operate directly on your Linux system. Powered by **Llama 3.2:1b**, it follows a "Smart Chaos" logic: performing rapid-fire actions, capturing screenshots, and manipulating the mouse and keyboard based on real-time visual feedback.

Unlike typical chatbots, this agent runs in a **continuous loop**, making decisions independently to achieve objectives via terminal commands, web searches, and UI interactions.

---

## ⚡ Technical Features (Based on `main.py`)

### 👁️ Visual & Physical Manifestation
* **Screenshot Integration:** Automatically captures and analyzes the screen to understand the UI state.
* **Hardware Control:** Native support for `move_mouse`, `click_mouse`, and `type_text` via custom system scripts.
* **Auto-Cleanup:** Automatically prunes old screenshots every 20 cycles to save disk space.

### 🧠 Intelligent Resource Management
* **CPU Throttling:** Includes a `wait_for_cpu` safety mechanism. If CPU usage exceeds 50%, the agent pauses to prevent system instability.
* **Ollama Self-Healing:** The script checks if the Ollama server is active; if not, it attempts to launch `ollama serve` automatically.

### 🛠️ Tool-Set (JSON-Driven)
The agent communicates via valid JSON actions, including:
* `shell`: Execute bash commands.
* `google`: Real-time web searching.
* `browse`: Navigate and synthesize website content.
* `write`: Local file creation and logging.

---

## 📋 Installation & Setup

### 1. Requirements
* **Ollama:** Installed and available in your PATH.
* **Python 3.x**
* **Dependencies:** `requests`, `pyautogui` (or your custom `system_actions` modules).

### 2. Project Structure
Ensure your directory looks like this:
```text
.
├── main.py                # The core logic you provided
├── scripts/
│   ├── system_actions.py  # Mouse/Keyboard controls
│   ├── file_operations.py # Writing logs
│   ├── system_vision.py   # Screenshot logic
│   └── commands.py        # Web search & Shell tools
└── outputs/               # (Auto-created) Stores screenshots
