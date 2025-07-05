import feedparser
from datetime import datetime
import streamlit as st
import openai
import os

openai.api_key = os.getenv("OPENAI_API_KEY")

AGENDA_CATEGORIES = [
    "Federal Agency Capture",
    "Judicial Defiance",
    "Suppression of Dissent",
    "NATO Disengagement",
    "Media Subversion"
]

@st.cache_data(ttl=300)
def fetch_geopolitical_updates():
    rss_urls = [
        "http://feeds.reuters.com/Reuters/worldNews",
        "http://feeds.bbci.co.uk/news/world/rss.xml",
        "https://apnews.com/rss/apf-topnews"
    ]

    articles = []

    for url in rss_urls:
        feed = feedparser.parse(url)
        for entry in feed.entries[:3]:
            title = entry.title
            summary = entry.summary if hasattr(entry, 'summary') else ""
            full_text = f"Title: {title}\nSummary: {summary}"
            tag = assign_tag_with_ai(full_text)

            articles.append({
                "title": title,
                "date": datetime(*entry.published_parsed[:6]).strftime('%Y-%m-%d') if hasattr(entry, 'published_parsed') else "N/A",
                "summary": summary,
                "link": entry.link,
                "tags": [tag] if tag else []
            })

    return articles

def assign_tag_with_ai(article_text):
    try:
        system_prompt = (
            "You're a political analyst classifying news based on authoritarian strategy. "
            "Choose the ONE most relevant category from this list:\n"
            "1. Federal Agency Capture\n"
            "2. Judicial Defiance\n"
            "3. Suppression of Dissent\n"
            "4. NATO Disengagement\n"
            "5. Media Subversion\n"
            "If none apply, return 'None'. Only return the category name."
        )

        user_prompt = f"Classify this article:\n{article_text}"

        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.2,
            max_tokens=20
        )

        tag = response.choices[0].message['content'].strip()
        return tag if tag in AGENDA_CATEGORIES else None

    except Exception as e:
        print(f"AI tag error: {e}")
        return None

def analyze_progress():
    return [
        {"title": "Federal Agency Capture", "progress": 82, "last_updated": "2025-04-17"},
        {"title": "Judicial Defiance", "progress": 73, "last_updated": "2025-04-17"},
        {"title": "Suppression of Dissent", "progress": 78, "last_updated": "2025-04-17"},
        {"title": "NATO Disengagement", "progress": 43, "last_updated": "2025-04-17"},
        {"title": "Media Subversion", "progress": 54, "last_updated": "2025-04-17"},
    ]

def trigger_emergency_alert(progress_data):
    triggered = False
    reasons = []

    for item in progress_data:
        if item['title'] == "Federal Agency Capture" and item['progress'] >= 80:
            reasons.append("Federal agency capture exceeds safe threshold.")
        if item['title'] == "Judicial Defiance" and item['progress'] >= 70:
            reasons.append("Unconstitutional judicial defiance observed.")
        if item['title'] == "Suppression of Dissent" and item['progress'] >= 75:
            reasons.append("Active suppression of dissent detected.")

    if reasons:
        return {"triggered": True, "reason": " | ".join(reasons)}
    return {"triggered": False, "reason": ""}

def generate_pdf_report(progress_data, events):
    from fpdf import FPDF
    import tempfile

    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt="Dugin-Trump Weekly Intelligence Report", ln=True, align="C")

    pdf.ln(10)
    pdf.set_font("Arial", style='B', size=12)
    pdf.cell(200, 10, txt="Progress Overview", ln=True)
    pdf.set_font("Arial", size=11)
    for item in progress_data:
        pdf.cell(200, 8, txt=f"{item['title']}: {item['progress']}% (Last Updated: {item['last_updated']})", ln=True)

    pdf.ln(10)
    pdf.set_font("Arial", style='B', size=12)
    pdf.cell(200, 10, txt="Recent Events", ln=True)
    pdf.set_font("Arial", size=11)
    for event in events:
        pdf.cell(200, 8, txt=f"{event['title']} ({event['date']})", ln=True)
        pdf.multi_cell(200, 8, txt=event['summary'])

    temp = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
    pdf.output(temp.name)
    return temp.name
