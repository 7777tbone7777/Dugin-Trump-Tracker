import streamlit as st
import datetime
from utils import fetch_geopolitical_updates, analyze_progress, trigger_emergency_alert, generate_pdf_report

# --- Sidebar ---
st.sidebar.title("Dugin-Trump Agenda Tracker")
st.sidebar.markdown("Philosophy: 🧠\n'Disintegrate the West. Restore sacred tradition. Promote multipolarity.'")

# --- Main Title ---
st.title("🧭 Dugin-Trump Agenda Tracker")
st.markdown("Tracking key authoritarian shifts in U.S. governance.")

# --- Progress & Alert Logic ---
progress_data = analyze_progress()
alert = trigger_emergency_alert(progress_data)
if alert['triggered']:
    st.error(f"🚨 EMERGENCY ALERT: {alert['reason']}")
    st.markdown("### 🔐 Escape Readiness Guide (coming soon...)")

# --- Progress Bars ---
st.markdown("## 📊 Progress Toward Authoritarian Goals")

# --- Fetch News with Error Handling ---
try:
    events = fetch_geopolitical_updates()
except Exception as e:
    st.error(f"Failed to load news: {e}")
    events = []

# --- Show Each Progress Category with Articles ---
for item in progress_data:
    st.subheader(item['title'])
    st.progress(item['progress'] / 100)
    st.caption(f"Progress: {item['progress']}% - Last Updated: {item['last_updated']}")

    related_articles = [e for e in events if item['title'] in e.get('tags', [])]
    if related_articles:
        with st.expander(f"🗞️ View {len(related_articles)} related articles"):
            us_articles = [a for a in related_articles if ".us" in a['link'] or "america" in a['summary'].lower()]
            intl_articles = [a for a in related_articles if a not in us_articles]

            if us_articles:
                st.markdown("### 🇺🇸 U.S. Articles")
                for article in us_articles:
                    st.markdown(f"**[{article['title']}]({article['link']})** ({article['date']})")
                    st.write(article['summary'])

            if intl_articles:
                st.markdown("### 🌍 International Articles")
                for article in intl_articles:
                    st.markdown(f"**[{article['title']}]({article['link']})** ({article['date']})")
                    st.write(article['summary'])

# --- Uncategorized Articles ---
ungrouped_articles = [e for e in events if not e.get('tags')]
if ungrouped_articles:
    st.markdown("## 🗃️ General Updates (Uncategorized)")
    for article in ungrouped_articles:
        st.markdown(f"**[{article['title']}]({article['link']})** ({article['date']})")
        st.write(article['summary'])

# --- PDF Report ---
st.markdown("## 📄 Generate Weekly Intelligence Report")
if st.button("Export PDF Report"):
    report_path = generate_pdf_report(progress_data, events)
    with open(report_path, "rb") as file:
        st.download_button(
            label="Download Report",
            data=file,
            file_name="Dugin_Trump_Weekly_Report.pdf",
            mime="application/pdf"
        )

# --- Footer ---
st.caption(f"📅 Updated {datetime.datetime.now().strftime('%B %d, %Y')}")
