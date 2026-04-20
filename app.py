
import streamlit as st
import pandas as pd
from datetime import date
import folium
from streamlit_folium import st_folium

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

st.header("🗺️ Running Routes")

routes = [
    {
        "name": "Riverside Easy Loop",
        "distance": 5,
        "lat": 52.586,
        "lon": -1.546
    },
    {
        "name": "Park Endurance Route",
        "distance": 10,
        "lat": 52.589,
        "lon": -1.550
    },
    {
        "name": "Hill Challenge",
        "distance": 15,
        "lat": 52.583,
        "lon": -1.540
    }
]

selected_distance = st.selectbox(
    "Select preferred route distance (km)",
    [5, 10, 15]
)

# Create map
m = folium.Map(location=[52.586, -1.546], zoom_start=13)

for route in routes:
    if route["distance"] == selected_distance:
        folium.Marker(
            location=[route["lat"], route["lon"]],
            popup=f"{route['name']} - {route['distance']} km",
            icon=folium.Icon(color="green", icon="info-sign")
        ).add_to(m)

st_folium(m, width=700, height=450)

st.header("🤖 Route Recommendation")

if "runs" in st.session_state and len(st.session_state.runs) > 0:
    average_distance = pd.DataFrame(st.session_state.runs)["distance"].mean()

    if average_distance < 6:
        st.info(
            "Based on your logged runs, the **Riverside Easy Loop** is recommended "
            "to build consistency without overloading."
        )
    elif average_distance < 12:
        st.success(
            "You're ready for the **Park Endurance Route** to continue improving stamina."
        )
    else:
        st.warning(
            "The **Hill Challenge** suits your fitness, but ensure adequate recovery."
        )
else:
    st.info(
        "Log a few runs to unlock personalised route recommendations."
    )

# Show data
if len(st.session_state.runs) > 0:
    df = pd.DataFrame(st.session_state.runs)

    st.header("📊 Your Running Data")
    st.dataframe(df)

    st.header("📈 Pace Trend")
    st.line_chart(df["pace"])

    avg_pace = df["pace"].mean()

    # AI metrics
    recent_runs = df.tail(3)
    pace_trend = recent_runs["pace"].iloc[-1] - recent_runs["pace"].iloc[0]
    run_frequency = len(df)


st.header("🤖 AI Coaching Insight")

st.write(f"✅ Average pace: **{avg_pace:.2f} min/km**")

if pace_trend < -0.3:
    st.success(
        "🚀 **Performance improving!** Your pace has dropped, which means you're running faster. "
        "This suggests your training load is well balanced."
    )

elif pace_trend > 0.3:
    st.warning(
        "⚠️ **Pace slowing slightly.** This can happen due to fatigue or stress. "
        "Consider easier runs or a recovery day."
    )

else:
    st.info(
        "📈 **Stable performance.** You're maintaining consistency, which is excellent for endurance."
    )

st.header("💬 AI Motivation")

if run_frequency >= 6:
    st.success(
        "🏆 Outstanding commitment! Your logging shows strong discipline. "
        "This level of consistency is associated with long‑term performance gains."
    )

elif run_frequency >= 3:
    st.info(
        "👏 Great job staying consistent. You're building a solid running habit — "
        "keep the rhythm going!"
    )

else:
    st.info(
        "🌱 Every runner starts somewhere. Focus on small wins — even one extra run matters."
    )

    # Motivational message
if len(df) >= 5 and df["pace"].iloc[-1] < df["pace"].iloc[0]:
    st.success("🚀 You're getting faster! Your training is clearly working.")
elif len(df) >= 3:
    st.success("✅ Strong consistency — this is how endurance is built.")
else:
    st.info("🌱 You're just getting started. Every run counts!")

with st.expander("🧠 How does the AI coach work?"):
    st.write(
        "The AI coach analyses your recent running patterns, pace trends, and consistency. "
        "It compares recent runs to identify improvement, stability, or fatigue, and adjusts "
        "its advice and motivation accordingly. This approach ensures transparency and avoids "
        "black‑box decision making."
    )
