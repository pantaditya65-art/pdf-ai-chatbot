# PDF AI Chatbot

A simple PDF chatbot built with Python and Streamlit. You can upload a PDF and ask questions about its contents instead of searching through the document manually.

### What it does

* Upload a PDF file
* Extract text from the document
* Ask questions about the PDF
* Get answers using an AI model

### Built with

* Python
* Streamlit
* OpenRouter API
* pypdf

### Run locally

Clone the repository:

```bash
git clone https://github.com/YOUR-USERNAME/pdf-ai-chatbot.git
cd pdf-ai-chatbot
```

Install the required packages:

```bash
pip install -r requirements.txt
```

Create `.streamlit/secrets.toml` and add your OpenRouter API key:

```toml
OPENAI_API_KEY = "your-api-key"
```

Start the app:

```bash
streamlit run app.py
```

### Note

The app works best with PDFs that contain selectable text. Large documents may exceed the AI model's context limit.

This is a personal project I built to explore Python, APIs, and AI-powered document processing.
