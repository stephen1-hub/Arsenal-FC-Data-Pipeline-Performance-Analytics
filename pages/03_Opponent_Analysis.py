import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="Opponent Analysis",
    page_icon="🏟️",
    layout="wide"
)

# ============================================================
# DATA PATH
# ============================================================

# This file is inside /pages
# matches.csv is located in the repository root

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR

MATCHES_FILE = DATA_DIR / "matches.csv"

# ============================================================
# LOAD MATCH DATA
# ============================================================

@st.cache_data
def load_matches():

    match_df = pd.read_csv(MATCHES_FILE)

    # ========================================================
    # RESULT
    # ========================================================

    match_df["Result"] = match_df.apply(
        lambda r:
        "Win"
        if r["ArsenalScore"] > r["OpponentScore"]
        else (
            "Draw"
            if r["ArsenalScore"] == r["OpponentScore"]
            else "Loss"
        ),
        axis=1
    )

    # ========================================================
    # POINTS
    # ========================================================

    match_df["Points"] = match_df["Result"].map({
        "Win": 3,
        "Draw": 1,
        "Loss": 0
    })

    # ========================================================
    # GOAL DIFFERENCE
    # ========================================================

    match_df["GoalDifference"] = (
        match_df["ArsenalScore"]
        - match_df["OpponentScore"]
    )

    return match_df


# ============================================================
# LOAD DATA
# ============================================================

match_df = load_matches()

# ============================================================
# HEADER
# ============================================================

st.title("🏟️ Opponent Analysis")

st.caption(
    "Business Question 3 — "
    "Which opponents have Arsenal performed well or poorly against?"
)

# ============================================================
# CHECK REQUIRED COLUMN
# ============================================================

if "Opponent" not in match_df.columns:

    st.error(
        "The matches.csv file does not contain an 'Opponent' column."
    )

    st.stop()

# ============================================================
# OPPONENT SUMMARY
# ============================================================

summary = (
    match_df
    .groupby("Opponent")
    .agg(
        Matches=("Result", "size"),

        Wins=(
            "Result",
            lambda x: (x == "Win").sum()
        ),

        Draws=(
            "Result",
            lambda x: (x == "Draw").sum()
        ),

        Losses=(
            "Result",
            lambda x: (x == "Loss").sum()
        ),

        Goals_Scored=(
            "ArsenalScore",
            "sum"
        ),

        Goals_Conceded=(
            "OpponentScore",
            "sum"
        ),

        Points=(
            "Points",
            "sum"
        ),

        Goal_Difference=(
            "GoalDifference",
            "sum"
        )
    )
    .reset_index()
)

# ============================================================
# CALCULATED METRICS
# ============================================================

summary["Win_%"] = (
    summary["Wins"]
    / summary["Matches"]
    * 100
)

summary["PPM"] = (
    summary["Points"]
    / summary["Matches"]
)

summary["Goals_Scored_Per_Match"] = (
    summary["Goals_Scored"]
    / summary["Matches"]
)

summary["Goals_Conceded_Per_Match"] = (
    summary["Goals_Conceded"]
    / summary["Matches"]
)

# ============================================================
# FILTERS
# ============================================================

st.subheader("🔎 Opponent Filters")

max_matches = int(summary["Matches"].max())

default_matches = min(4, max_matches)

min_matches = st.slider(
    "Minimum matches against opponent",
    min_value=1,
    max_value=max_matches,
    value=default_matches,
    step=1
)

# Apply filter

filtered = summary[
    summary["Matches"] >= min_matches
].copy()

# ============================================================
# RANKING METRIC
# ============================================================

sort_metric = st.selectbox(
    "Rank opponents by",
    [
        "PPM",
        "Win_%",
        "Goal_Difference",
        "Goals_Scored_Per_Match",
        "Goals_Conceded_Per_Match"
    ]
)

filtered = filtered.sort_values(
    sort_metric,
    ascending=False
)

# ============================================================
# EMPTY DATA CHECK
# ============================================================

if filtered.empty:

    st.warning(
        "No opponents meet the selected minimum-match requirement."
    )

    st.stop()

# ============================================================
# KPI CARDS
# ============================================================

best_ppm = filtered.loc[
    filtered["PPM"].idxmax()
]

worst_ppm = filtered.loc[
    filtered["PPM"].idxmin()
]

best_goal_diff = filtered.loc[
    filtered["Goal_Difference"].idxmax()
]

worst_goal_diff = filtered.loc[
    filtered["Goal_Difference"].idxmin()
]

c1, c2, c3, c4 = st.columns(4)

c1.metric(
    "Best PPM",
    f"{best_ppm['PPM']:.2f}",
    str(best_ppm["Opponent"])
)

c2.metric(
    "Worst PPM",
    f"{worst_ppm['PPM']:.2f}",
    str(worst_ppm["Opponent"])
)

c3.metric(
    "Best Goal Difference",
    f"{best_goal_diff['Goal_Difference']:+.0f}",
    str(best_goal_diff["Opponent"])
)

c4.metric(
    "Worst Goal Difference",
    f"{worst_goal_diff['Goal_Difference']:+.0f}",
    str(worst_goal_diff["Opponent"])
)

# ============================================================
# SUMMARY TABLE
# ============================================================

st.subheader("📊 Opponent Performance Summary")

st.dataframe(
    filtered.style.format({
        "Win_%": "{:.2f}%",
        "PPM": "{:.2f}",
        "Goals_Scored_Per_Match": "{:.2f}",
        "Goals_Conceded_Per_Match": "{:.2f}"
    }),
    use_container_width=True
)

# ============================================================
# TOP & WORST OPPONENTS
# ============================================================

col1, col2 = st.columns(2)

# ============================================================
# TOP OPPONENTS BY PPM
# ============================================================

with col1:

    top_ppm = (
        filtered
        .sort_values("PPM", ascending=False)
        .head(10)
        .sort_values("PPM")
    )

    fig = px.bar(
        top_ppm,
        x="PPM",
        y="Opponent",
        orientation="h",
        text="PPM",
        title="Top Opponents by Points Per Match"
    )

    fig.update_traces(
        texttemplate="%{text:.2f}",
        textposition="outside"
    )

    fig.update_layout(
        xaxis_title="Points Per Match",
        yaxis_title=""
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

# ============================================================
# WORST GOAL DIFFERENCES
# ============================================================

with col2:

    worst_goal_diff_chart = (
        filtered
        .sort_values("Goal_Difference")
        .head(10)
        .sort_values("Goal_Difference", ascending=False)
    )

    fig = px.bar(
        worst_goal_diff_chart,
        x="Goal_Difference",
        y="Opponent",
        orientation="h",
        text="Goal_Difference",
        title="Largest Negative Goal Differences"
    )

    fig.update_traces(
        textposition="outside"
    )

    fig.update_layout(
        xaxis_title="Goal Difference",
        yaxis_title=""
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

# ============================================================
# TOUGHEST OPPONENTS
# ============================================================

st.subheader("⚠️ Toughest Opponents")

toughest = (
    filtered
    .sort_values("PPM")
    .head(5)
)

st.dataframe(
    toughest[
        [
            "Opponent",
            "Matches",
            "Wins",
            "Draws",
            "Losses",
            "Win_%",
            "PPM",
            "Goal_Difference"
        ]
    ].style.format({
        "Win_%": "{:.2f}%",
        "PPM": "{:.2f}",
        "Goal_Difference": "{:+.0f}"
    }),
    use_container_width=True
)

# ============================================================
# ANALYTICAL NOTE
# ============================================================

st.info(
    "Opponent comparisons should be interpreted alongside sample size. "
    "An opponent faced only a few times can have an extreme win rate "
    "or PPM that is less reliable than results against frequently "
    "faced opponents."
)
