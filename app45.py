import streamlit as st
import pandas as pd
from pathlib import Path

# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Arsenal FC Analytics",
    page_icon="⚽",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ============================================================
# PROJECT PATHS
# ============================================================

BASE_DIR = Path(__file__).resolve().parent

MATCHES_FILE = BASE_DIR / "matches.csv"
PLAYERS_FILE = BASE_DIR / "players.csv"
GOALKEEPERS_FILE = BASE_DIR / "goalkeepers.csv"

# ============================================================
# LOAD DATA
# ============================================================

@st.cache_data
def load_data():

    match_df = pd.read_csv(MATCHES_FILE)
    players_df = pd.read_csv(PLAYERS_FILE)
    goalkeepers_df = pd.read_csv(GOALKEEPERS_FILE)

    # Convert dates
    if "Date" in match_df.columns:
        match_df["Date"] = pd.to_datetime(
            match_df["Date"],
            errors="coerce"
        )

    if "Date" in players_df.columns:
        players_df["Date"] = pd.to_datetime(
            players_df["Date"],
            errors="coerce"
        )

    if "Date" in goalkeepers_df.columns:
        goalkeepers_df["Date"] = pd.to_datetime(
            goalkeepers_df["Date"],
            errors="coerce"
        )

    return match_df, players_df, goalkeepers_df


match_df, players_df, goalkeepers_df = load_data()

# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.title("⚽ Arsenal FC Analytics")

    st.caption("2017/18 – 2022/23")

    st.divider()

    st.markdown(
        """
        ### 📌 Dashboard

        Use the navigation menu above to explore:

        - 📅 Season Performance
        - 🧑‍💼 Coach Analysis
        - 🏟️ Opponent Analysis
        - 👤 Player Analytics
        - 🧤 Goalkeeper Analytics
        """
    )

    st.divider()

    st.caption(
        "Football Analytics Case Study"
    )

# ============================================================
# PAGE HEADER
# ============================================================

st.title(
    "⚽ Arsenal FC Data Pipeline & Performance Analytics"
)

st.markdown(
    """
    An interactive football analytics dashboard analysing
    Arsenal's team performance, coaching periods, opponents,
    player contributions and goalkeeper performance.
    """
)

# ============================================================
# DATASET NOTE
# ============================================================

st.info(
    "Use the pages in the sidebar to explore the analytical "
    "sections. The 2022/23 season is incomplete in the "
    "available dataset."
)

# ============================================================
# MATCH PERFORMANCE
# ============================================================

match_df = match_df.copy()

match_df["Result"] = match_df.apply(
    lambda row:
        "Win"
        if row["ArsenalScore"] > row["OpponentScore"]
        else (
            "Draw"
            if row["ArsenalScore"] == row["OpponentScore"]
            else "Loss"
        ),
    axis=1,
)

match_df["Points"] = match_df["Result"].map(
    {
        "Win": 3,
        "Draw": 1,
        "Loss": 0,
    }
)

match_df["GoalDifference"] = (
    match_df["ArsenalScore"]
    - match_df["OpponentScore"]
)

# ============================================================
# KPI CALCULATIONS
# ============================================================

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

goals_for = match_df["ArsenalScore"].sum()

goals_against = match_df["OpponentScore"].sum()

total_points = match_df["Points"].sum()

ppm = (
    total_points / total_matches
    if total_matches > 0
    else 0
)

win_rate = (
    wins / total_matches * 100
    if total_matches > 0
    else 0
)

goal_difference = (
    goals_for - goals_against
)

# ============================================================
# KPI CARDS
# ============================================================

st.subheader("📊 Arsenal Performance Overview")

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

# ============================================================
# DATASET OVERVIEW
# ============================================================

col1, col2 = st.columns(2)

with col1:

    st.subheader("📅 Seasons Covered")

    seasons = sorted(
        match_df["Season"]
        .dropna()
        .astype(str)
        .unique()
    )

    st.write(
        ", ".join(seasons)
    )

    st.subheader("📁 Data Assets")

    st.write(
        f"**Matches:** {len(match_df):,} records"
    )

    st.write(
        f"**Player-match records:** "
        f"{len(players_df):,} records"
    )

    st.write(
        f"**Goalkeeper-match records:** "
        f"{len(goalkeepers_df):,} records"
    )

with col2:

    st.subheader("🎯 Business Questions")

    st.markdown(
        """
        **1. Season Performance**

        How did Arsenal's performance change by season?

        **2. Coach Performance**

        How did Arsenal perform under different coaches?

        **3. Opponent Performance**

        Which opponents have Arsenal performed well
        or poorly against?

        **4. Player Contribution**

        Which players made the greatest contribution
        by position?

        **5. Goalkeeper Performance**

        Which goalkeepers performed best across
        shot-stopping and distribution metrics?

        **6. Coaching & Player Contribution**

        How did player contribution change across
        coaching periods?
        """
    )

st.divider()

# ============================================================
# DATASET SUMMARY
# ============================================================

st.subheader("📦 Dataset Summary")

summary_data = pd.DataFrame(
    {
        "Dataset": [
            "Matches",
            "Player Match Records",
            "Goalkeeper Match Records",
        ],
        "Records": [
            len(match_df),
            len(players_df),
            len(goalkeepers_df),
        ],
    }
)

st.dataframe(
    summary_data,
    hide_index=True,
    use_container_width=True,
)

st.divider()

# ============================================================
# FOOTER
# ============================================================

st.caption(
    "Arsenal FC Data Pipeline & Performance Analytics | "
    "Football Analytics Case Study | "
    "Created by Stephen Yaw Ayamah"
)
