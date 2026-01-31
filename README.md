# Smart-Spider | AI-Powered SEO Intelligence Platform

![Python](https://img.shields.io/badge/Python-3.10%2B-blue?style=for-the-badge&logo=python)
![Streamlit](https://img.shields.io/badge/Frontend-Streamlit-FF4B4B?style=for-the-badge&logo=streamlit)
![Gemini AI](https://img.shields.io/badge/AI_Vision-Google_Gemini-8E75B2?style=for-the-badge&logo=google)
![SQLite](https://img.shields.io/badge/Database-SQLite-003B57?style=for-the-badge&logo=sqlite)

> **A Next-Generation Technical SEO Auditor that combines asynchronous crawling, computer vision, and topological graph theory to deliver enterprise-grade site analysis.**

🔗 **[Live Demo: Launch Smart-Spider](https://smart-spider.streamlit.app)**

---

## Overview

**Smart-Spider** is not just a scraper; it is a full-stack SEO intelligence agent. Unlike traditional tools that only read text, Smart-Spider employs **Multimodal AI (Google Gemini)** to "see" images and generate accessibility captions (Alt-Text) automatically.

Built for the modern web, it features a **Force-Directed Knowledge Graph** to visualize site architecture and a **Persistent Ledger** to track historical SEO performance over time.

---

## Key Features

### 1. Multimodal AI Vision Analysis
* Integrates **Google Gemini 1.5 Flash** to analyze website assets.
* Automatically detects broken or missing `alt-text`.
* **Self-Healing:** Generates context-aware, SEO-optimized captions for images in real-time.

### 2. Topological Site Architecture
* Visualizes internal linking structures using **NetworkX** and **PyVis**.
* Renders a 3D interactive, force-directed graph to identify "orphan pages" and link equity distribution.

### 3. Persistent History Ledger
* Built-in **SQLite engine** stores audit logs permanently.
* Allows users to "Time Travel" and reload previous audit reports to compare scores over time.

### 4. Automated Compliance Reporting
* Generates **PDF Audit Certificates** using `FPDF`.
* Produces industry-standard documentation ready for client delivery immediately after scanning.

---

## Technical Architecture

The system follows a **Headless Modular Architecture**:

1.  **The Crawler Engine (`crawler.py`):** An asynchronous Python worker that parses DOM structures using `BeautifulSoup4` and handles networking via `Requests`.
2.  **The Intelligence Layer (`utils.py`):** Manages API handshakes with Google GenAI, handling rate limits and tokenization.
3.  **The Persistence Layer (`database.py`):** A lightweight ORM wrapper around SQLite3 for ACID-compliant data storage.
4.  **The Visualization Layer (`app.py`):** A reactive frontend built on Streamlit, utilizing Plotly for metrics and JavaScript bridging for the Knowledge Graph.

---

## Installation & Local Setup

Clone the repository to run the enterprise version (with persistent database) locally.

```bash
# 1. Clone the repository
git clone [https://github.com/your-username/smart-spider-seo.git](https://github.com/your-username/smart-spider-seo.git)
cd smart-spider-seo

# 2. Install dependencies
pip install -r requirements.txt

# 3. Configure Environment Variables
# Create a .env file and add your Google API Key
echo "GOOGLE_API_KEY=your_api_key_here" > .env

# 4. Launch the Platform
streamlit run src/app.py
```
# License & Credits

Developed by: Harsh M. Parikh | License: MIT License.
