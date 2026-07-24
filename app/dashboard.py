import streamlit as st
import requests
import pandas as pd
import time

st.set_page_config(page_title="Streaming Analytics Dashboard", layout="wide")

st.title("⚡ Real-Time Telemetry Ingestion & Analytics Engine")
st.markdown("Live monitoring of event buffers, client throughput, and rate-limiting metrics.")

STATS_URL = "http://127.0.0.1:8000/api/v1/stats"

placeholder = st.empty()

while True:
    try:
        res = requests.get(STATS_URL).json()
        total_events = res.get("total_buffered_events", 0)
        recent_buffer = res.get("buffer_preview", [])

        df = pd.DataFrame(recent_buffer)

        with placeholder.container():
            col1, col2, col3 = st.columns(3)
            col1.metric("Total Buffered Events", total_events)
            col2.metric("Active Pipeline Status", "ONLINE ✅")
            col3.metric("Rate Limiter Status", "ACTIVE (50 req/min) 🛡️")

            st.subheader("📋 Live Event Stream Buffer (Recent Ingests)")
            if not df.empty:
                st.dataframe(df[["event_id", "client_id", "event_type", "timestamp"]], use_container_width=True)
            else:
                st.info("No events in buffer yet. Start the traffic generator script!")

    except Exception as e:
        st.error(f"Could not connect to FastAPI backend: {e}")

    time.sleep(1)
