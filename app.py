import streamlit as st
import datetime
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import requests
import time
import random
from textblob import TextBlob

# Dugin agenda and polarity flip map (True = flip sentiment)
AGENDA_ITEMS = {
    "Dismantling NATO Alliances": (["NATO", "withdraw troops", "Trump NATO"], True),
    "Weakening U.S. Intelligence Community": (["FBI purge", "CIA cuts", "intelligence overhaul"], True),
    "Pulling Troops from Strategic Regions": (["troop withdrawal", "military exit"], True),
    "Promoting Christian Nationalism": (["Christian nationalism", "evangelical politics"], True),
    "Delegitimizing Elections": (["voter fraud", "rigged election"], True),
    "Reducing Federal Power Over States": (["states' rights", "federal overreach"], True),
    "Isolationist Foreign Policy": (["America First", "foreign aid cuts"], True),
    "Discrediting Free Press": (["fake news", "enemy of the people"], True),
    "Fostering Civil Unrest": (["civil war", "armed protest"], True),
    "Undermining Global Democratic Norms": (["autocracy rise", "authoritarian alliance"], True)
}

@st.cache_data(show_spinner=False)
def fetch_sentiment_progress():
    api_key = st.secrets["NEWSAPI_KEY"]
    base_url = "https://newsapi.org/v2/everything"
    results = {}

    for item, (keywords, flip_sentiment) in AGENDA_ITEMS.items():
        keyword = random.choice(keywords)
        headlines = []
        sentiment_scores = []

        params = {
            "q": keyword,
            "language": "en",
            "pageSize": 10,
            "sortBy": "publishedAt",
            "apiKey": api_key
        }

        try:
            response = requests.get(base_url, params=params, timeout=5)
            time.sleep(1)
            data = response.json()
            articles = data.get("articles", [])
            for article in articles:
                title = article["title"]
                url = article["url"]
                source = article["source"]["name"]
                polarity = TextBlob(title).sentiment.polarity
                if flip_sentiment:
                    polarity *= -1
                sentiment_scores.append(polarity)
                headlines.append((title, url, source))
        except Exception as e:
            print(f"Error fetching {keyword}: {e}")

        if sentiment_scores:
            avg_score = sum(sentiment_scores) / len(sentiment_scores)
        else:
            avg_score = 0

        # Normalize from -1 to 1 → 0 to 100%
        progress = round((avg_score + 1) * 50)
        progress = max(0, min(progress, 100))

        results[item] = {
            "progress": progress,
            "headlines": headlines[:3],
            "keyword_used": keyword
        }

    return results

# UI
st.sidebar.title("Dugin Context")
st.sidebar.markdown("""
Aleksandr Dugin, a Russian political philosopher, promotes a Eurasian worldview opposed to liberal Western democracy.

This dashboard tracks the advancement of his ideological blueprint through U.S. politics.
""")

st.title("Dugin-Trump Agenda Tracker")
st.markdown("Sentiment-based monitoring of 10 strategic objectives aligned with Dugin's ideology to evaluate their adoption within U.S. governance.")

data = fetch_sentiment_progress()
st.markdown("### Current Sentiment Progress (Auto-Sourced)")

for item, details in data.items():
    st.progress(details["progress"], text=f"{item}: {details['progress']}%")
    st.caption(f"🧠 Keyword: *{details['keyword_used']}*")
    with st.expander("See headlines"):
        for title, url, source in details["headlines"]:
            st.markdown(f"- [{title}]({url}) _(via {source})_")

# Email Report
def send_weekly_email():
    sender_email = st.secrets["EMAIL_USER"]
    password = st.secrets["EMAIL_PASS"]
    receiver_email = "scarfaceforward@gmail.com"

    message = MIMEMultipart("alternative")
    message["Subject"] = "Weekly Dugin-Trump Sentiment Update"
    message["From"] = sender_email
    message["To"] = receiver_email

    html = f"<html><body><h2>Dugin-Trump Sentiment Report - {datetime.date.today()}</h2><ul>"
    for item, details in data.items():
        html += f"<li><strong>{item}:</strong> {details['progress']}% (Keyword: {details['keyword_used']})</li>"
    html += "</ul><p>This report was generated from sentiment analysis of current news headlines.</p></body></html>"

    part = MIMEText(html, "html")
    message.attach(part)

    with smtplib.SMTP_SSL("smtp.mail.yahoo.com", 465) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message.as_string())

if st.button("Send Weekly Email Report"):
    send_weekly_email()
    st.success("Email sent to scarfaceforward@gmail.com")
