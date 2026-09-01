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


```

### Login Credentials

```
Email: tanveer.ganesan@hotmail.com (or any user from seed)
Password: password123
```

---

## 🛠️ Tech Stack

| Category | Technology |
|----------|------------|
| **Framework** | FastAPI |
| **Database** | SQLite + SQLAlchemy ORM |
| **AI/LLM** | Groq API (Llama 3.3 70B) |
| **Templates** | Jinja2 |
| **Authentication** | Session-based (itsdangerous) |
| **Password Hashing** | bcrypt / passlib |

---

## 📂 Project Structure

```
ai-yearbook/
├── app/
│   ├── main.py          # FastAPI routes & app setup
│   ├── models.py        # SQLAlchemy database models
│   ├── ai.py            # AI integration (Groq API)
│   ├── config.py        # Environment configuration
│   ├── security.py      # Authentication & session handling
│   ├── social.py        # Social media data collector
│   └── db.py            # Database connection
├── templates/
│   ├── base.html        # Base template
│   ├── index.html       # Yearbook directory
│   ├── profile.html     # User profile & testimonials
│   └── login.html       # Login page
├── static/
│   └── style.css        # Styling
├── seed.py              # Database seeder (200+ users)
├── requirements.txt     # Python dependencies
├── .env.example         # Environment variables template
└── README.md            # This file
```

---

## 🎯 How It Works

### 1. **Browse Profiles**
- Visit the yearbook directory
- Search for any user
- Click on a profile to view

### 2. **Generate AI Testimonial**
- Click **"Generate AI"** on a user's profile
- AI uses chat history & social signals
- Automatically checks similarity with existing testimonials
- Regenerates if too similar (up to 3 attempts)

### 3. **Write Manually**
- Click **"Write"** on the homepage (auto-opens form)
- Or click **"Write Manually"** on profile
- Submit your own testimonial

### 4. **View Testimonials**
- All testimonials appear on the user's profile
- AI-generated ones show 🤖 tag
- Manual ones show ✍️ tag

---

## 🔑 API Configuration

### Groq API Setup

1. Visit [Groq Console](https://console.groq.com)
2. Sign up / Login
3. Go to **API Keys** → **Create API Key**
4. Copy the key (starts with `gsk_...`)
5. Add to `.env`:

```env
GROQ_API_KEY=gsk_xxxxxxxxxxxxxxxxxxxx
GROQ_MODEL=openai/gpt-oss-120b
```

### Environment Variables

| Variable | Description |
|----------|-------------|
| `APP_SECRET` | Secret key for session encryption |
| `DATABASE_URL` | SQLite database path |
| `GROQ_API_KEY` | Your Groq API key |
| `GROQ_MODEL` | Groq model to use |
| `SIMILARITY_THRESHOLD` | Similarity tolerance (0.0 - 1.0) |
| `MAX_GENERATION_ATTEMPTS` | Max retries for uniqueness |
| `MAX_CHAT_CONTEXT` | Number of chats to include |

---

## 🧪 Testing

```bash
# Run similarity tests
python test_similarity.py

# Check database
sqlite3 yearbook.db
SELECT COUNT(*) FROM users;
```

---

## 📦 Dependencies

```
fastapi
uvicorn[standard]
sqlalchemy
jinja2
python-multipart
passlib[bcrypt]
python-dotenv
httpx
beautifulsoup4
itsdangerous
faker
```

---

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing`)
5. Open a Pull Request

---

## 📄 License

Free to use, modify, and distribute.

---

## ⚠️ Important Notes

- **Database resets** when running `seed.py` (backup if needed)
- **Groq free tier** allows 30 requests/minute (enough for most usage)

---

## 🧑‍💻 Created By

Your Name — [GitHub](https://github.com/tanishq-jain124)

---

## ⭐ Support

If you find this project useful, please give it a ⭐ on GitHub!

---
