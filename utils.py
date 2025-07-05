import feedparser
from datetime import datetime
import streamlit as st

@st.cache_data(ttl=300)  # Cache for 5 minutes
def fetch_geopolitical_updates():
    rss_urls = [
        "http://feeds.reuters.com/Reuters/worldNews",
        "http://feeds.bbci.co.uk/news/world/rss.xml",
        "https://apnews.com/rss/apf-topnews"
    ]

    tag_keywords = {
        "Federal Agency Capture": ["agency", "DOJ", "FBI", "federal", "oversight", "regulator", "EPA", "bureau"],
        "Judicial Defiance": ["judge", "court", "SCOTUS", "ruling", "judicial", "justice", "overturn", "legal"],
        "Suppression of Dissent": ["protest", "arrest", "speech", "dissent", "activist", "press", "police", "censorship"],
        "NATO Disengagement": ["NATO", "withdraw", "alliances", "troops", "military", "europe", "disengagement"],
        "Media Subversion": ["media", "news", "journalist", "propaganda", "coverage", "broadcast", "misinformation"]
    }

    articles = []

    for url in rss_urls:
        feed = feedparser.parse(url)
        for entry in feed.entries[:5]:
            summary = entry.summary.lower() if hasattr(entry, 'summary') else ""
            matched_tags = []

            for tag, keywords in tag_keywords.items():
                if any(k.lower() in summary for k in keywords):
                    matched_tags.append(tag)

            articles.append({
                "title": entry.title,
                "date": datetime(*entry.published_parsed[:6]).strftime('%Y-%m-%d') if hasattr(entry, 'published_parsed') else "N/A",
                "summary": entry.summary if hasattr(entry, 'summary') else "",
                "link": entry.link,
                "tags": matched_tags or ["Uncategorized"]
            })

    return articles

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
