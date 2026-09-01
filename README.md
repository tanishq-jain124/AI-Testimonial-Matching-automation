# AI-Testimonial-Matching-automation


An AI-powered digital yearbook that generates personalized testimonials using Groq API. Users can either let AI generate a testimonial or write one manually.

---

## ✨ Features

- 🔐 **User Authentication** — Login system with session management
- 👥 **Yearbook Directory** — Browse all users with search functionality
- 🤖 **AI-Generated Testimonials** — Powered by Groq's Llama 3.3 70B model
- ✍️ **Manual Testimonials** — Write your own testimonials
- 🔄 **Similarity Checking** — Prevents duplicate testimonials
- 📊 **200+ Demo Users** — Pre-seeded database with realistic data
- 🎯 **Context-Aware** — Uses chat history and social signals for personalized responses

---

## 🚀 Quick Start

### Prerequisites

- Python 3.11+
- Groq API Key (free) — [Get it here](https://console.groq.com)

### Installation

```bash
# 1. Clone the repository
git clone https://github.com/tanishq-jain124/AI-Testimonial-Matching-automation.git
cd AI-Testimonial-Matching-automation

# 2. Create and activate virtual environment
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
# .venv\Scripts\activate   # Windows

# 3. Install dependencies
pip install -r requirements.txt

# 4. Create .env file (copy from .env.example)
cp .env.example .env

# 5. Add your Groq API key to .env
# GROQ_API_KEY=your_groq_api_key_here

# 6. Seed the database with sample users
python seed.py

# 7. Run the application
uvicorn app.main:app --reload
