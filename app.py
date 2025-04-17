
import streamlit as st
import datetime
from utils import fetch_geopolitical_updates, analyze_progress, trigger_emergency_alert, generate_pdf_report

# --- Sidebar ---
st.sidebar.title("Dugin-Trump Agenda Tracker")
st.sidebar.markdown("Philosophy: 🧠
'Disintegrate the West. Restore sacred tradition. Promote multipolarity.'")

# --- Main Title ---
st.title("🧭 Dugin-Trump Agenda Tracker")
st.markdown("Tracking key authoritarian shifts in U.S. governance.")

# --- Progress Bars ---
progress_data = analyze_progress()

for item in progress_data:
    st.subheader(item['title'])
    st.progress(item['progress'] / 100)
    st.caption(f"Progress: {item['progress']}% - Last Updated: {item['last_updated']}")

# --- Emergency Alert ---
alert = trigger_emergency_alert(progress_data)
if alert['triggered']:
    st.error(f"🚨 EMERGENCY ALERT: {alert['reason']}")
    st.markdown("### 🔐 Escape Readiness Guide (coming soon...)")

# --- Latest Events ---
st.markdown("## 📰 Latest Key Events")
events = fetch_geopolitical_updates()
for event in events:
    st.markdown(f"**{event['title']}** ({event['date']})")
    st.write(event['summary'])

# --- Export Report ---
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

st.caption(f"📅 Updated {datetime.datetime.now().strftime('%B %d, %Y')}")
