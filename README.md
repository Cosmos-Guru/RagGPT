# Internet-RAG Chat (Gemma 2 + Ollama + LangChain)

A local Flask-based Retrieval-Augmented Generation (RAG) web app. Ask a question, the app scrapes the top Google results (no paid API), fetches each page’s visible text, and then uses Gemma 2 (running in Ollama) to produce an engaging, bullet-point summary.

---

## Table of Contents

1. [Features](#features)  
2. [Prerequisites](#prerequisites)  
   - [Mac (Apple Silicon / Intel)](#mac-intel--apple-silicon)  
   - [Windows 10/11](#windows-1011)  
3. [Setup & Installation](#setup--installation)  
   1. [Clone the Repository](#1-clone-the-repository)  
   2. [Install Ollama & Pull Gemma 2](#2-install-ollama--pull-gemma-2)  
   3. [Create a Python Virtual Environment](#3-create-a-python-virtual-environment)  
   4. [Install Python Dependencies](#4-install-python-dependencies)  
   5. [Start the Ollama Server](#5-start-the-ollama-server)  
   6. [Run the Flask App](#6-run-the-flask-app)  
4. [Usage](#usage)  
5. [Troubleshooting](#troubleshooting)  
6. [License](#license)  

---

## Features

- **Live Google scraping** (via `googlesearch-python`) ─ no API keys required.  
- **Automatic page fetching & text extraction** (with `requests` + BeautifulSoup).  
- **LangChain + Ollama (Gemma 2)** for vibrant, bullet-point summaries.  
- **Simple Flask front-end**—ask questions and see responses in your browser (port 5050).  
- 100 % local: everything runs on your machine; your data never leaves your computer.

---

## Prerequisites

Before proceeding, ensure you have the following installed:

1. **Git** ─ for cloning the repo.  
2. **Python 3.9+** ─ for running the Flask backend.  
3. **Ollama** ─ to host Gemma 2 locally.  

Below are step-by-step instructions for Mac and Windows novice users.

### Mac (Intel or Apple Silicon)

1. **Install Homebrew** (if you don’t already have it).  
   Open Terminal (`⌘ Space` → type “Terminal” → Enter), then paste:

   ```bash
   /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
   ```

   Follow on-screen prompts. Homebrew installs command-line tools and keeps them up to date.

2. **Install Git**

   ```bash
   brew install git
   ```

   Verify:

   ```bash
   git --version
   ```

   You should see something like `git version 2.x.x`.

3. **Install Python 3.9+**

   ```bash
   brew install python
   ```

   Verify:

   ```bash
   python3 --version
   pip3 --version
   ```

   You should see Python 3.x.x and pip 23.x.x (or higher).

4. **Install Ollama**

   - Visit [https://ollama.com](https://ollama.com) and click **Download for Mac**.  
   - Follow the installer prompts.  
   - Verify installation:

     ```bash
     ollama version
     ```

---

### Windows 10/11

1. **Install Git for Windows**

   - Download the installer from: https://gitforwindows.org  
   - Run the installer, accept defaults, and complete the installation.  
   - Open Command Prompt and verify:

     ```bash
     git --version
     ```

2. **Install Python 3.9+**

   - Go to https://www.python.org/downloads/windows/  
   - Download the “Windows installer (64-bit)” for the latest Python 3.x.  
   - Run the installer and check **“Add Python to PATH”** during setup.  
   - Open a new Command Prompt and verify:

     ```bash
     python --version
     pip --version
     ```

3. **Install Ollama**

   - Visit [https://ollama.com](https://ollama.com) and click **Download for Windows**.  
   - Unzip the archive and place `ollama.exe` somewhere like `C:\Ollama\`.  
   - Add that folder to your system `PATH`:  
     - `Win + R` → `sysdm.cpl` → Environment Variables → System Variables → Path → Edit → New → `C:\Ollama\`  
     - Click OK on all dialogs.  
   - Open a new Command Prompt:

     ```bash
     ollama version
     ```

---

## Setup & Installation

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/internet-rag-chat.git
cd internet-rag-chat
```

### 2. Install Ollama & Pull Gemma 2

```bash
ollama serve
# In another terminal:
ollama pull gemma2:latest
```

### 3. Create a Python Virtual Environment

```bash
# macOS / Linux
python3 -m venv venv
source venv/bin/activate

# Windows
python -m venv venv
venv\Scripts\activate
```

### 4. Install Python Dependencies

```bash
pip install --upgrade pip
pip install flask beautifulsoup4 requests googlesearch-python \
            langchain langchain-community langchain-ollama
```

### 5. Start the Ollama Server (if not already running)

```bash
ollama serve
```

### 6. Run the Flask App

```bash
# macOS / Linux
export FLASK_APP=app.py
flask run --host=0.0.0.0 --port=5050

# Windows (PowerShell)
$env:FLASK_APP="app.py"
flask run --host=0.0.0.0 --port=5050

# Or just run directly:
python app.py
```

---

## Usage

1. Open your browser: [http://localhost:5050](http://localhost:5050)  
2. Type any question, e.g., "What is the latest news on Ukraine?"  
3. Click **Send**  
4. Behind the scenes:
   - The app scrapes top 3 Google results
   - Extracts readable page content
   - Builds a prompt
   - Summarizes using Gemma 2 via LangChain

---

## Troubleshooting

- **401 Forbidden (e.g. Reuters):** We set headers; site may still block. Skipped gracefully.  
- **`[object Object]` instead of summary:** Make sure `return result_dict.get("text", "")` is used in `app.py`.  
- **Port 5050 in use?** Try another port: `flask run --port=5051`  
- **Missing modules:** Re-run `pip install ...` inside your venv.  
- **Ollama issues:**  
  ```bash
  ollama status
  ollama serve
  ```

---

## License

MIT © 2025 — Use freely.

