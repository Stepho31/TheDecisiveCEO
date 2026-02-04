# --- imports unchanged ---
import os
import json
from datetime import datetime

from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

from sqlalchemy import (
    create_engine, Column, Integer, String, Text, DateTime, ForeignKey
)
from sqlalchemy.orm import sessionmaker, declarative_base

from dotenv import load_dotenv
from openai import OpenAI

# ---------------- ENV ----------------
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# ---------------- DATABASE ----------------
DATABASE_URL = "sqlite:///./simulator.db"
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

# ---------------- APP ----------------
app = FastAPI()
templates = Jinja2Templates(directory="templates")

# ---------------- MODELS ----------------
class Company(Base):
    __tablename__ = "company"

    id = Column(Integer, primary_key=True)
    company_key = Column(String, unique=True, index=True)

    industry = Column(String)
    size = Column(String)
    model = Column(String)
    sensitivity = Column(String)
    priorities = Column(Text)
    updated_at = Column(DateTime, default=datetime.utcnow)


class Decision(Base):
    __tablename__ = "decisions"

    id = Column(Integer, primary_key=True)
    company_id = Column(Integer, ForeignKey("company.id"))

    description = Column(Text)
    ai_result = Column(Text)
    created_by = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    context_snapshot = Column(Text)


Base.metadata.create_all(bind=engine)

# ---------------- HELPERS ----------------
def get_company_by_key(db, company_key: str):
    return db.query(Company).filter(Company.company_key == company_key).first()


def normalize_array(value):
    if isinstance(value, list):
        return value
    if isinstance(value, str):
        return [value]
    return []


def run_simulation(company: Company, scenario: str) -> dict:
    prompt = f"""
Return valid JSON only.

Company:
Industry: {company.industry}
Size: {company.size}
Model: {company.model}
Sensitivity: {company.sensitivity}
Priorities: {company.priorities}

Decision:
{scenario}

Keys:
risk_level, risk_summary,
best_case_outcomes,
worst_case_risks,
second_order_effects,
recommendation
"""

    response = client.responses.create(
        model="gpt-4o-mini",
        input=prompt,
        temperature=0.2,
    )

    text = ""
    for item in response.output:
        if item.type == "message":
            for c in item.content:
                if c.type == "output_text":
                    text += c.text

        clean_text = text.strip()

    if not clean_text:
        raise ValueError("AI returned empty response")

    # Attempt to extract JSON object from text
    start = clean_text.find("{")
    end = clean_text.rfind("}")

    if start == -1 or end == -1 or end <= start:
        raise ValueError(f"AI returned non-JSON output: {clean_text}")

    json_text = clean_text[start : end + 1]

    result = json.loads(json_text)


    result["best_case_outcomes"] = normalize_array(result.get("best_case_outcomes"))
    result["worst_case_risks"] = normalize_array(result.get("worst_case_risks"))
    result["second_order_effects"] = normalize_array(result.get("second_order_effects"))

    return result

# ---------------- ROUTES ----------------

# Landing
@app.get("/", response_class=HTMLResponse)
def landing(request: Request):
    return templates.TemplateResponse("landing.html", {"request": request})


# Enter company page
@app.get("/enter", response_class=HTMLResponse)
def enter_page(request: Request):
    return templates.TemplateResponse("enter.html", {"request": request})


# Enter company action
@app.post("/enter")
def enter_company(company_key: str = Form(...)):
    return RedirectResponse(
        url=f"/workspace?company_key={company_key}",
        status_code=303
    )

@app.get("/setup", response_class=HTMLResponse)
def setup_page(request: Request):
    return templates.TemplateResponse(
        "setup.html",
        {"request": request}
    )

# Create company action
@app.post("/setup")
def setup_company(
    company_key: str = Form(...),
    industry: str = Form(...),
    size: str = Form(...),
    model: str = Form(...),
    sensitivity: str = Form(...),
    priorities: str = Form(...),
):
    db = SessionLocal()

    if get_company_by_key(db, company_key):
        db.close()
        return HTMLResponse("Company key already exists.", status_code=400)

    company = Company(
        company_key=company_key,
        industry=industry,
        size=size,
        model=model,
        sensitivity=sensitivity,
        priorities=priorities,
    )

    db.add(company)
    db.commit()
    db.close()

    return RedirectResponse(
        url=f"/workspace?company_key={company_key}",
        status_code=303
    )


# Workspace (your existing app)
@app.get("/workspace", response_class=HTMLResponse)
def workspace(request: Request, company_key: str):
    db = SessionLocal()
    company = get_company_by_key(db, company_key)

    if not company:
        db.close()
        return RedirectResponse("/")

    decisions = (
        db.query(Decision)
        .filter(Decision.company_id == company.id)
        .order_by(Decision.created_at.desc())
        .all()
    )

    for d in decisions:
        try:
            parsed = json.loads(d.ai_result)
        except Exception:
            parsed = {
                "risk_level": "Unknown",
                "risk_summary": "This decision could not be parsed.",
                "best_case_outcomes": [],
                "worst_case_risks": [],
                "second_order_effects": [],
                "recommendation": "No recommendation available."
            }

        parsed["best_case_outcomes"] = normalize_array(
            parsed.get("best_case_outcomes")
        )
        parsed["worst_case_risks"] = normalize_array(
            parsed.get("worst_case_risks")
        )
        parsed["second_order_effects"] = normalize_array(
            parsed.get("second_order_effects")
        )

        # 🔑 ALWAYS assign this
        d.ai_result_parsed = parsed



    db.close()

    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "company": company,
            "decisions": decisions,
            "company_key": company_key,
        },
    )


# Run simulation
@app.post("/simulate")
def simulate(
    scenario: str = Form(...),
    company_key: str = Form(...),
    created_by: str = Form("Team"),
):
    db = SessionLocal()
    company = get_company_by_key(db, company_key)

    result = run_simulation(company, scenario)

    decision = Decision(
        company_id=company.id,
        description=scenario,
        ai_result=json.dumps(result),
        created_by=created_by,
        context_snapshot=json.dumps({
            "company_key": company.company_key,
            "industry": company.industry,
            "size": company.size,
            "model": company.model,
            "sensitivity": company.sensitivity,
            "priorities": company.priorities,
        }),

    )

    db.add(decision)
    db.commit()
    db.close()

    return RedirectResponse(
        url=f"/workspace?company_key={company_key}",
        status_code=303
    )
