# The Decisive CEO

The Decisive CEO is a context-aware decision simulation tool built for business owners and teams who want to understand the risks, tradeoffs, and upside of decisions **before** they are made.

Instead of reacting after outcomes unfold, this tool helps teams slow down, think clearly, and evaluate decisions using their company’s real context as the foundation.

---

## The Problem

Business decisions rarely fail because people don’t care.

They fail because the full consequences aren’t visible upfront.

Most AI tools require you to repeatedly explain:
- Who your company is  
- What industry you’re in  
- What matters most to you  
- Why a decision is sensitive  

That repetition creates friction, fatigue, and inconsistency.

Context gets lost — and decisions suffer.

---

## The Solution

The Decisive CEO flips the model.

Instead of prompting AI from scratch every time, you:
1. Enter your company’s context once  
2. Ask “What happens if…” style questions  
3. Receive analysis grounded in your business reality  

Every decision is evaluated through the same lens — consistently and intentionally.

---

## What the App Does

- Creates a shared company workspace  
- Stores company context (industry, size, model, priorities, sensitivity)  
- Accepts decision scenarios  
- Simulates risks, best cases, and second-order effects  
- Saves decision history for reflection and learning  

This is **not** a chat interface.  
It is a **context-first decision engine**.

---

## Why I Built This

I’m committing to building **one piece of useful software every week** that solves a real problem for an end user.

Each project is intentionally:
- Focused  
- Lightweight  
- Practical  
- Free to use  

If even one person finds it helpful, it’s worth building.

---

## Tech Stack

- FastAPI  
- SQLite  
- SQLAlchemy  
- Jinja2  
- Tailwind CSS  
- OpenAI API  

---

## Getting Started

### 1) Clone the repository
Run: `git clone https://github.com/Stepho31/TheDecisiveCEO.git`  
Then: `cd TheDecisiveCEO`

### 2) Create and activate a virtual environment
Create it: `python -m venv venv`  
Activate it (Mac/Linux): `source venv/bin/activate`  
Activate it (Windows): `venv\Scripts\activate`

### 3) Install dependencies
Install: `pip install -r requirements.txt`

### 4) Set environment variables
Create a `.env` file in the project root and add your key like this:  
`OPENAI_API_KEY=your_api_key_here`

Important: never commit `.env` to GitHub. Ensure `.env` is listed in your `.gitignore`.

### 5) Run the application
Start the server: `uvicorn app:app --reload`  
Open the app in your browser: `http://127.0.0.1:8000`

---

## How It Works

1. A company is created with shared context (industry, size, priorities, sensitivity)  
2. That context is stored once and reused  
3. Decision scenarios are submitted against that context  
4. AI evaluates outcomes using the company’s real constraints  
5. Decisions are saved and can be reviewed over time  

This avoids the need to repeatedly restate context and keeps decision-making consistent.

---

## What Makes This Different

Most AI tools are **prompt-first**.

The Decisive CEO is **context-first**.

Instead of asking:
> “Here’s my company again…”

The system already knows:
- Who you are  
- What matters most  
- What decisions are sensitive  
- What tradeoffs exist  

This leads to clearer, more relevant decision analysis.

---

## Notes

- This tool supports decision-making — it does not replace human judgment  
- The goal is clarity, not prediction  
- Designed to reduce decision fatigue, not automate leadership  

---

## Roadmap

- Decision comparison across scenarios  
- Confidence scoring and risk weighting  
- Team roles and permissions  
- Exportable decision history  
- UI polish and UX improvements  

---

## Philosophy

Good decisions compound.  
Bad decisions compound faster.

The Decisive CEO exists to slow down the moment **before** a decision is made — when clarity matters most.

---

## License

MIT License
