import streamlit as st
import pandas as pd
import datetime
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
import requests
from bs4 import BeautifulSoup

# Agenda Items and Keywords for Auto-Tracking
AGENDA_ITEMS = {
    "Dismantling NATO Alliances": ["NATO", "withdraw troops", "Trump NATO", "defund NATO"],
    "Weakening U.S. Intelligence Community": ["FBI purge", "CIA cuts", "intelligence overhaul"],
    "Pulling Troops from Strategic Regions": ["troop withdrawal", "military exit", "Trump Middle East pullout"],
    "Promoting Christian Nationalism": ["Christian nationalism", "evangelical politics", "dominionism"],
    "Delegitimizing Elections": ["voter fraud", "rigged election", "fake ballots"],
    "Reducing Federal Power Over States": ["states' rights", "federal overreach", "sovereignty acts"],
    "Isolationist Foreign Policy": ["America First", "foreign aid cuts", "Trump isolationism"],
    "Discrediting Free Press": ["fake news", "enemy of the people", "media lies"],
    "Fostering Civil Unrest": ["civil war", "armed protest", "Trump militia"],
    "Undermining Global Democratic Norms": ["autocracy rise", "authoritarian alliance", "dismantle democracy"]
}

# Improved binning logic for progress scoring
@st.cache_data(show_spinner=False)
def fetch_progress():
    headers = {"User-Agent": "Mozilla/5.0"}
    base_url = "https://news.google.com/search?q={query}&hl=en-US&gl=US&ceid=US:en"
    updated = {}

    for item, keywords in AGENDA_ITEMS.items():
        total_hits = 0
        for keyword in keywords:
            try:
                url = base_url.format(query=keyword.replace(" ", "+"))
                response = requests.get(url, headers=headers, timeout=5)
                soup = BeautifulSoup(response.content, "html.parser")
                articles = soup.find_all("article")
                total_hits += len(articles)
            except Exception:
                continue

        # Map raw hit count into a defined progress bin
        if total_hits <= 3:
            progress = 10
        elif total_hits <= 7:
            progress = 30
        elif total_hits <= 15:
            progress = 60
        elif total_hits <= 25:
            progress = 80
        else:
            progress = 100

        updated[item] = progress

    return updated

# Sidebar
st.sidebar.title("Dugin Context")
st.sidebar.markdown("""
Aleksandr Dugin, a Russian political philosopher, promotes a Eurasian worldview opposed to liberal Western democracy.

This dashboard tracks the advancement of his ideological blueprint through U.S. politics.
""")

# Header
st.title("Dugin-Trump Agenda Tracker")
st.markdown("""
Live monitoring of 10 strategic objectives aligned with Dugin's ideology to evaluate their adoption within U.S. governance.
""")

# Fetch progress
st.markdown("### Current Progress Snapshot (Auto-Sourced)")
latest_progress = fetch_progress()
for item, value in latest_progress.items():
    st.progress(value, text=f"{item}: {value}%")

# Export PDF (placeholder)
if st.button("Export Intelligence PDF"):
    st.info("PDF export coming soon - this will include headlines and trend charts.")

# Email Report
def send_weekly_email():
    sender_email = os.getenv("EMAIL_USER")
    receiver_email = "scarfaceforward@gmail.com"
    password = os.getenv("EMAIL_PASS")

    message = MIMEMultipart("alternative")
    message["Subject"] = "Weekly Dugin-Trump Agenda Progress Update"
    message["From"] = sender_email
    message["To"] = receiver_email

    html = f"<html><body><h2>Dugin-Trump Agenda Weekly Report - {datetime.date.today()}</h2><ul>"
    for item, value in latest_progress.items():
        html += f"<li><strong>{item}:</strong> {value}%</li>"
    html += "</ul><p>This report was auto-generated by the Dugin-Trump Tracker System.</p></body></html>"

    part = MIMEText(html, "html")
    message.attach(part)

    with smtplib.SMTP_SSL("smtp.mail.yahoo.com", 465) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message.as_string())

# Send email button
if st.button("Send Weekly Email Report"):
    send_weekly_email()
    st.success("Email sent to scarfaceforward@gmail.com")
