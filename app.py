
import streamlit as st
import pandas as pd
from datetime import date

st.title("🏃 AI Running Companion")

st.write("Log your runs, track progress, and get AI insights.")

# Create empty run storage
if "runs" not in st.session_state:
    st.session_state.runs = []

# Run logging form
st.header("📌 Log a Run")
with st.form("run_form"):
    run_date = st.date_input("Date", date.today())
    distance = st.number_input("Distance (km)", min_value=0.0)
    duration = st.number_input("Duration (minutes)", min_value=0.0)
    effort = st.slider("Effort level (1 = easy, 5 = hard)", 1, 5)
    submitted = st.form_submit_button("Save Run")

    if submitted:
        pace = duration / distance if distance > 0 else 0
        st.session_state.runs.append({
            "date": run_date,
            "distance": distance,
            "duration": duration,
            "pace": pace,
            "effort": effort
        })
        st.success("Run saved!")

# Show data
if len(st.session_state.runs) > 0:
    df = pd.DataFrame(st.session_state.runs)

    st.header("📊 Your Running Data")
    st.dataframe(df)

    st.header("📈 Pace Trend")
    st.line_chart(df["pace"])

    avg_pace = df["pace"].mean()

    st.header("🤖 AI Insight")
    st.write(f"Your average pace is **{avg_pace:.2f} min/km**.")

    # Motivational message
if len(df) >= 5 and df["pace"].iloc[-1] < df["pace"].iloc[0]:
    st.success("🚀 You're getting faster! Your training is clearly working.")
elif len(df) >= 3:
    st.success("✅ Strong consistency — this is how endurance is built.")
else:
    st.info("🌱 You're just getting started. Every run counts!")
``
