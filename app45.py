import streamlit as st
import pandas as pd
from pathlib import Path

# --------------------------------------------------
# PAGE CONFIG
# --------------------------------------------------

st.set_page_config(
    page_title="Arsenal FC Analytics",
    page_icon="⚽",
    layout="wide",
    initial_sidebar_state="expanded",
)

# --------------------------------------------------
# DATA PATH
# --------------------------------------------------

# app45.py is located at the repository root
BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data" / "raw"

# --------------------------------------------------
# LOAD DATA
# --------------------------------------------------

@st.cache_data
def load_data():

    match_df = pd.read_csv(
        DATA_DIR / "matches.csv"
    )

    players_df = pd.read_csv(
        DATA_DIR / "players.csv"
    )

    goalkeepers_df = pd.read_csv(
        DATA_DIR / "goalkeepers.csv"
    )

    # Convert dates
    match_df["Date"] = pd.to_datetime(
        match_df["Date"],
        errors="coerce"
    )

    players_df["Date"] = pd.to_datetime(
        players_df["Date"],
        errors="coerce"
    )

    goalkeepers_df["Date"] = pd.to_datetime(
        goalkeepers_df["Date"],
        errors="coerce"
    )

    return match_df, players_df, goalkeepers_df


match_df, players_df, goalkeepers_df = load_data()

# --------------------------------------------------
# SIDEBAR
# --------------------------------------------------

st.sidebar.title("⚽ Arsenal FC Analytics")

st.sidebar.caption(
    "2017/18 – 2022/23"
)

# --------------------------------------------------
# PAGE HEADER
# --------------------------------------------------

st.title(
    "⚽ Arsenal FC Data Pipeline & Performance Analytics"
)

st.markdown(
    """
    An interactive football analytics dashboard covering team performance,
    coaching periods, opponents, players and goalkeepers.
    """
)

# --------------------------------------------------
# DATASET NOTE
# --------------------------------------------------

st.info(
    "Use the pages in the sidebar to explore the five business questions. "
    "The 2022/23 season is incomplete in the available dataset."
)

# ==================================================
# MATCH PERFORMANCE CALCULATIONS
# ==================================================

match_df = match_df.copy()

# --------------------------------------------------
# RESULT
# --------------------------------------------------

match_df["Result"] = match_df.apply(
    lambda r:
    "Win"
    if r["ArsenalScore"] > r["OpponentScore"]
    else (
        "Draw"
        if r["ArsenalScore"] == r["OpponentScore"]
        else "Loss"
    ),
    axis=1,
)

# --------------------------------------------------
# POINTS
# --------------------------------------------------

match_df["Points"] = match_df["Result"].map({
    "Win": 3,
    "Draw": 1,
    "Loss": 0
})

# --------------------------------------------------
# GOAL DIFFERENCE
# --------------------------------------------------

match_df["GoalDifference"] = (
    match_df["ArsenalScore"]
    - match_df["OpponentScore"]
)

# ==================================================
# KPI CALCULATIONS
# ==================================================

total_matches = len(match_df)

wins = (
    match_df["Result"] == "Win"
).sum()

draws = (
    match_df["Result"] == "Draw"
).sum()

losses = (
    match_df["Result"] == "Loss"
).sum()

goals_for = match_df[
    "ArsenalScore"
].sum()

goals_against = match_df[
    "OpponentScore"
].sum()

total_points = match_df[
    "Points"
].sum()

ppm = (
    total_points / total_matches
    if total_matches
    else 0
)

win_rate = (
    wins / total_matches * 100
    if total_matches
    else 0
)

goal_difference = (
    goals_for - goals_against
)

# ==================================================
# KPI CARDS
# ==================================================

c1, c2, c3, c4, c5 = st.columns(5)

c1.metric(
    "Matches",
    f"{total_matches:,}"
)

c2.metric(
    "Wins",
    f"{wins:,}"
)

c3.metric(
    "Win Rate",
    f"{win_rate:.1f}%"
)

c4.metric(
    "Points / Match",
    f"{ppm:.2f}"
)

c5.metric(
    "Goal Difference",
    f"{goal_difference:+,}"
)

st.divider()

# ==================================================
# DATASET OVERVIEW
# ==================================================

col1, col2 = st.columns(2)

# --------------------------------------------------
# SEASONS & DATA ASSETS
# --------------------------------------------------

with col1:

    st.subheader("📊 Seasons Covered")

    seasons = sorted(
        match_df["Season"]
        .dropna()
        .unique()
    )

    st.write(
        ", ".join(seasons)
    )

    st.subheader("📁 Data Assets")

    st.write(
        f"Matches: **{len(match_df):,}** records"
    )

    st.write(
        f"Player-match records: **{len(players_df):,}** records"
    )

    st.write(
        f"Goalkeeper-match records: **{len(goalkeepers_df):,}** records"
    )

# --------------------------------------------------
# BUSINESS QUESTIONS
# --------------------------------------------------

with col2:

    st.subheader("🎯 Business Questions")

    st.markdown(
        """
        **1. Season Performance**  
        How did Arsenal's performance change by season?

        **2. Coach Performance**  
        How did Arsenal perform under different coaches?

        **3. Opponent Performance**  
        Which opponents have Arsenal performed well or poorly against?

        **4. Player Contribution**  
        Which players made the greatest contribution by position?

        **5. Coaching & Player Contribution**  
        How did player contribution change across coaching periods?
        """
    )

st.divider()

# ==================================================
# DASHBOARD GUIDE
# ==================================================

st.subheader("🚀 Dashboard Guide")

st.markdown(
    """
    Use the pages on the left to move through the analysis:

    **Team Performance → Coaching → Opponents → Players → Goalkeepers**

    The dashboard is designed as a football analytics case study,
    with emphasis on **decision-ready metrics rather than isolated statistics**.
    """
)

# ==================================================
# DATASET SUMMARY
# ==================================================

st.subheader("📦 Dataset Summary")

summary_data = pd.DataFrame({
    "Dataset": [
        "Matches",
        "Player Match Records",
        "Goalkeeper Match Records"
    ],
    "Records": [
        len(match_df),
        len(players_df),
        len(goalkeepers_df)
    ]
})

st.dataframe(
    summary_data,
    hide_index=True,
    use_container_width=True
)
