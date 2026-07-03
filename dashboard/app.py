import streamlit as st
import pandas as pd
import json
import os
def expected_value(play):
    confidence = float(play.get("confidence", 0))
    odds = int(play.get("odds", -110))

    if odds < 0:
        payout = 100 / abs(odds)
    else:
        payout = odds / 100

    probability = confidence / 100
    ev = (probability * payout) - (1 - probability)

    return round(ev * 100, 2)

from models.best_bets import get_best_bets
from models.pick_rating import rate_pick
from models.bankroll_manager import recommend_units


def analyze_pick(play):
    confidence = play.get("confidence", 0)
    ai_score = play.get("ai_score", 0)
    edge = play.get("edge", 0)

    reasons = []

    if confidence >= 90:
        reasons.append("🔥 Very High AI Confidence")
    if ai_score >= 70:
        reasons.append("🧠 AI Model Strongly Agrees")
    if edge >= 5:
        reasons.append("📈 Positive Betting Edge")
    if not reasons:
        reasons.append("⚠️ Limited Supporting Data")

    return reasons


st.set_page_config(
    page_title="Luxx Parlay AI Dashboard",
    page_icon="🔥",
    layout="wide"
)

HISTORY_FILE = "data/picks_history.json"

st.title("🔥 Luxx Parlay AI Dashboard")
st.caption("Version 6.2 Bankroll Manager Dashboard")
import subprocess
import sys
import os
from datetime import datetime

col_refresh, col_update = st.columns(2)

with col_refresh:
    if st.button("🔄 Refresh Dashboard"):
        st.rerun()

with col_update:
    if st.button("🔥 Update Picks Now"):
        before = os.path.getmtime(HISTORY_FILE) if os.path.exists(HISTORY_FILE) else 0

        with st.spinner("Updating Luxx AI picks..."):
            result = subprocess.run(
                [sys.executable, "models/generate_today_picks.py"],
                capture_output=True,
                text=True
            )

        after = os.path.getmtime(HISTORY_FILE) if os.path.exists(HISTORY_FILE) else 0

        if result.returncode == 0:
            if after > before:
                st.success("Picks updated and history file changed.")
            else:
                st.warning("AI ran, but picks_history.json did not change.")
            st.code(result.stdout or "No output from AI engine.")
        else:
            st.error("Update failed.")
            st.code(result.stderr)

def load_history():
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return []


history = load_history()
if history:
    latest = history[-1]
    generated = latest.get("generated_at", "Unknown")
    st.caption(f"🕒 Last Pick Update: {generated}")

if not history:
    st.warning("No pick history found yet.")
    st.stop()

    from datetime import datetime

st.info(f"🕒 Dashboard refreshed: {datetime.now().strftime('%I:%M:%S %p')}")

total_runs = len(history)
total_picks = wins = losses = pushes = pending = 0

for run in history:
    for play in run.get("plays", []):
        total_picks += 1
        result = str(play.get("result", "pending")).lower()

        if result == "win":
            wins += 1
        elif result == "loss":
            losses += 1
        elif result == "push":
            pushes += 1
        else:
            pending += 1

graded = wins + losses + pushes
win_rate = round((wins / (wins + losses)) * 100, 1) if wins + losses > 0 else 0

col1, col2, col3, col4, col5 = st.columns(5)
col1.metric("Total Runs", total_runs)
col2.metric("Total Picks", total_picks)
col3.metric("Wins", wins)
col4.metric("Losses", losses)
col5.metric("Win Rate", f"{win_rate}%")

st.divider()

st.subheader("📊 Status Breakdown")
c1, c2, c3 = st.columns(3)
c1.metric("Pending Picks", pending)
c2.metric("Pushes", pushes)
c3.metric("Graded Picks", graded)

st.divider()

st.subheader("📈 Dashboard Charts")
chart_col1, chart_col2 = st.columns(2)

status_data = pd.DataFrame({
    "Status": ["Pending", "Wins", "Losses", "Pushes"],
    "Count": [pending, wins, losses, pushes]
})

with chart_col1:
    st.write("Pick Status")
    st.bar_chart(status_data.set_index("Status"))

latest = history[-1] if history else {"plays": []}
plays = latest.get("plays", [])

run_data = pd.DataFrame({
    "Metric": ["Total Runs", "Latest Run Picks", "Total Picks"],
    "Count": [total_runs, len(plays), total_picks]
})

with chart_col2:
    st.write("Run Overview")
    st.bar_chart(run_data.set_index("Metric"))

st.divider()

st.subheader("🏆 Today's Best Bets")

best_bets = get_best_bets(plays)

for i, bet in enumerate(best_bets, start=1):
    rating, risk = rate_pick(bet)
    units, bet_style = recommend_units(bet)
    ev = expected_value(bet)

    st.success(
        f"#{i} {bet.get('team', 'Unknown')} | "
        f"{bet.get('market', 'Unknown')} | "
        f"Odds: {bet.get('odds', 'N/A')} | "
        f"Confidence: {bet.get('confidence', 0)}% | "
        f"Edge: +{bet.get('edge', 0)}% | "
        f"AI Score: {bet.get('ai_score', 0)} | "
        f"Rating: {rating} | "
        f"EV: {ev}% | "
        f"Risk: {risk} | "
        f"Units: {units} | "
        f"Bet Style: {bet_style}"
    )

    with st.expander("🧠 AI Analysis"):
        for reason in analyze_pick(bet):
            st.write(reason)

st.divider()

st.subheader("🔎 Filters")

filter_result = st.selectbox(
    "Filter by result",
    ["All", "Pending", "Win", "Loss", "Push"]
)

filtered_plays = plays

if filter_result != "All":
    filtered_plays = [
        play for play in plays
        if str(play.get("result", "pending")).lower() == filter_result.lower()
    ]

st.divider()
st.subheader("🔥 Latest Picks")

latest = history[-1] if history else {"plays": []}
plays = latest.get("plays", [])

for index, play in enumerate(plays, start=1):
    st.markdown(
        f"""
        <div style="padding:18px; border-radius:14px; background:#161b22; margin-bottom:14px; border:1px solid #30363d;">
            <h3>#{index} {play.get("team", "Unknown")}</h3>
            <p><b>Market:</b> {play.get("market", "Unknown")}</p>
            <p><b>Odds:</b> {play.get("odds", "N/A")}</p>
            <p><b>Confidence:</b> {play.get("confidence", "N/A")}%</p>
            <p><b>AI Score:</b> {play.get("ai_score", "N/A")}</p>
            <p><b>Edge:</b> +{play.get("edge", "N/A")}%</p>
            <p><b>Stars:</b> {play.get("stars", "N/A")}</p>
            <p><b>Result:</b> {str(play.get("result", "pending")).upper()}</p>
        </div>
        """,
        unsafe_allow_html=True
    )

    with st.expander("🧠 AI Analysis"):
        for reason in analyze_pick(play):
            st.write(reason)