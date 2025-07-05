import feedparser
from datetime import datetime
import streamlit as st

def analyze_progress():
    return [
        {"title": "Federal Agency Capture", "progress": 82, "last_updated": "2025-04-17"},
        {"title": "Judicial Defiance", "progress": 73, "last_updated": "2025-04-17"},
        {"title": "Suppression of Dissent", "progress": 78, "last_updated": "2025-04-17"},
        {"title": "NATO Disengagement", "progress": 43, "last_updated": "2025-04-17"},
        {"title": "Media Subversion", "progress": 54, "last_updated": "2025-04-17"},
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
            title = entry.title.lower()
            summary = entry.summary.lower()

            tags = []
            if any(word in title or summary for word in ["fbi", "irs", "agency", "oversight", "executive"]):
                tags.append("Federal Agency Capture")
            if any(word in title or summary for word in ["judge", "supreme court", "ruling", "constitutional"]):
                tags.append("Judicial Defiance")
            if any(word in title or summary for word in ["protest", "arrest", "media", "speech", "journalist"]):
                tags.append("Suppression of Dissent")
            if any(word in title or summary for word in ["nato", "europe", "alliance", "withdrawal", "ukraine"]):
                tags.append("NATO Disengagement")
            if any(word in title or summary for word in ["cnn", "fake news", "press", "censorship"]):
                tags.append("Media Subversion")

            articles.append({
                "title": entry.title,
                "date": datetime(*entry.published_parsed[:6]).strftime('%Y-%m-%d') if hasattr(entry, 'published_parsed') else "N/A",
                "summary": entry.summary if hasattr(entry, 'summary') else "",
                "link": entry.link,
                "tags": tags
            })

    return articles

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
