# --- app.py ---
import streamlit as st
import datetime
from utils import fetch_geopolitical_updates, analyze_progress, trigger_emergency_alert, generate_pdf_report

st.set_page_config(page_title="Dugin-Trump Agenda Tracker", layout="wide")

# --- Sidebar ---
st.sidebar.title("Dugin-Trump Agenda Tracker")
st.sidebar.markdown("Philosophy: 🧠\n'Disintegrate the West. Restore sacred tradition. Promote multipolarity.'")

# --- Main Title ---
st.title("\U0001F9ED Dugin-Trump Agenda Tracker")
st.markdown("Tracking key authoritarian shifts in U.S. governance.")

# --- Fetch Data ---
progress_data = analyze_progress()
events = fetch_geopolitical_updates()

# --- Emergency Alert ---
alert = trigger_emergency_alert(progress_data)
if alert['triggered']:
    st.error(f"\U0001F6A8 EMERGENCY ALERT: {alert['reason']}")
    st.markdown("### \U0001F512 Escape Readiness Guide (coming soon...)")

# --- Progress Bars with Related Articles ---
st.markdown("## \U0001F4CA Progress Toward Authoritarian Goals")
for item in progress_data:
    st.subheader(item['title'])
    st.progress(item['progress'] / 100)
    st.caption(f"Progress: {item['progress']}% - Last Updated: {item['last_updated']}")

    # Show related articles
    related_articles = [e for e in events if item['title'] in e.get("tags", [])]
    if related_articles:
        with st.expander(f"\U0001F4F0 View {len(related_articles)} related articles"):
            for article in related_articles:
                st.markdown(f"**[{article['title']}]({article['link']})** ({article['date']})")
                st.write(article['summary'])

# --- Latest Events ---
st.markdown("## \U0001F4F0 Latest Key Events")
for event in events:
    st.markdown(f"**[{event['title']}]({event['link']})** ({event['date']})")
    st.write(event['summary'])

# --- Export Report ---
st.markdown("## \U0001F4C4 Generate Weekly Intelligence Report")
if st.button("Export PDF Report"):
    report_path = generate_pdf_report(progress_data, events)
    with open(report_path, "rb") as file:
        st.download_button(
            label="Download Report",
            data=file,
            file_name="Dugin_Trump_Weekly_Report.pdf",
            mime="application/pdf"
        )

st.caption(f"\U0001F4C5 Updated {datetime.datetime.now().strftime('%B %d, %Y')}")
