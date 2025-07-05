import streamlit as st
import datetime
from utils import fetch_geopolitical_updates, analyze_progress, trigger_emergency_alert, generate_pdf_report

# --- Sidebar ---
st.sidebar.title("Dugin-Trump Agenda Tracker")
st.sidebar.markdown("Philosophy: 🧠\n'Disintegrate the West. Restore sacred tradition. Promote multipolarity.'")

# --- Main Title ---
st.title("🧭 Dugin-Trump Agenda Tracker")
st.markdown("Tracking key authoritarian shifts in U.S. governance.")

# --- Emergency Alert ---
progress_data = analyze_progress()
alert = trigger_emergency_alert(progress_data)
if alert['triggered']:
    st.error(f"🚨 EMERGENCY ALERT: {alert['reason']}")
    st.markdown("### 🔐 Escape Readiness Guide (coming soon...)")

# --- Progress Bars & Related Articles ---
st.markdown("## 📊 Progress Toward Authoritarian Goals")

events = fetch_geopolitical_updates()
st.text(f"Sample tags from news: {[e['tags'] for e in events]}")
for item in progress_data:
    st.subheader(item['title'])
    st.progress(item['progress'] / 100)
    st.caption(f"Progress: {item['progress']}% - Last Updated: {item['last_updated']}")

    # Related Articles
    related_articles = [e for e in events if item['title'] in e.get('tags', [])]
    if related_articles:
        with st.expander(f"🗞️ View {len(related_articles)} related articles"):
            for article in related_articles:
                st.markdown(f"**[{article['title']}]({article['link']})** ({article['date']})")
                st.write(article['summary'])

# --- Latest Ungrouped Articles ---
ungrouped_articles = [e for e in events if not e.get('tags')]
if ungrouped_articles:
    st.markdown("## 🗃️ General Updates (Uncategorized)")
    for article in ungrouped_articles:
        st.markdown(f"**[{article['title']}]({article['link']})** ({article['date']})")
        st.write(article['summary'])

# --- PDF Export ---
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
