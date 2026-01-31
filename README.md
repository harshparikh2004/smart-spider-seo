# Smart-Spider: AI-Powered Technical SEO Auditor 🕷️

## Project Overview
Smart-Spider is an automated technical SEO auditing tool developed to streamline the website optimization process at **Emblus**. Unlike traditional manual audits, this tool utilizes Python-based crawlers and AI computer vision to detect performance bottlenecks and accessibility issues (missing Alt-text) in real-time.

## Key Features
- **Automated Crawling:** Scrapes target URLs for meta-data, header hierarchy, and broken links using `BeautifulSoup`.
- **AI Image Analysis:** Integrates Hugging Face Inference API to automatically generate Alt-Text for images.
- **Performance Metrics:** Measures Time-to-First-Byte (TTFB) and load latency.
- **Interactive Dashboard:** Built with Streamlit for real-time reporting.

## Technology Stack
- **Language:** Python 3.10+
- **Frontend:** Streamlit
- **Core Logic:** Requests, BeautifulSoup4
- **AI Model:** BLIP (Bootstrapping Language-Image Pre-training) via Hugging Face API

## How to Run
1. Clone the repository
2. Install dependencies: `pip install -r requirements.txt`
3. Run the application: `streamlit run src/app.py`