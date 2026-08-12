import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="Season Performance",
    page_icon="📅",
    layout="wide"
)

# ============================================================
# DATA PATH
# ============================================================

# This file is inside /pages
# CSV files are in the repository root

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR

MATCHES_FILE = DATA_DIR / "matches.csv"

# ============================================================
# LOAD MATCH DATA
# ============================================================

@st.cache_data
def load_matches():

    match_df = pd.read_csv(MATCHES_FILE)

    # Convert date
    if "Date" in match_df.columns:
        match_df["Date"] = pd.to_datetime(
            match_df["Date"],
            errors="coerce"
        )

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

matches = load_matches()

# ============================================================
# HEADER
# ============================================================

st.title("📅 Season Performance")

st.caption(
    "Business Question 1 — "
    "How did Arsenal's performance change from season to season?"
)

# ============================================================
# SEASON SUMMARY
# ============================================================

summary = (
    matches
    .groupby("Season")
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
# KPI CARDS
# ============================================================

c1, c2, c3, c4 = st.columns(4)

best_win = summary.loc[
    summary["Win_%"].idxmax()
]

best_ppm = summary.loc[
    summary["PPM"].idxmax()
]

best_attack = summary.loc[
    summary["Goals_Scored_Per_Match"].idxmax()
]

best_goal_difference = summary.loc[
    summary["Goal_Difference"].idxmax()
]

c1.metric(
    "Best Win Rate",
    f"{best_win['Win_%']:.1f}%",
    str(best_win["Season"])
)

c2.metric(
    "Best PPM",
    f"{best_ppm['PPM']:.2f}",
    str(best_ppm["Season"])
)

c3.metric(
    "Highest Goals/Match",
    f"{best_attack['Goals_Scored_Per_Match']:.2f}",
    str(best_attack["Season"])
)

c4.metric(
    "Best Goal Difference",
    f"{best_goal_difference['Goal_Difference']:+.0f}",
    str(best_goal_difference["Season"])
)

# ============================================================
# SEASON SUMMARY TABLE
# ============================================================

st.subheader("📊 Season Summary")

display_summary = summary.copy()

st.dataframe(
    display_summary.style.format({
        "Win_%": "{:.2f}%",
        "PPM": "{:.2f}",
        "Goals_Scored_Per_Match": "{:.2f}",
        "Goals_Conceded_Per_Match": "{:.2f}"
    }),
    use_container_width=True
)

# ============================================================
# CHARTS
# ============================================================

col1, col2 = st.columns(2)

# ============================================================
# POINTS PER MATCH
# ============================================================

with col1:

    fig = px.line(
        summary,
        x="Season",
        y="PPM",
        markers=True,
        title="Points Per Match by Season"
    )

    fig.update_layout(
        yaxis_title="Points Per Match",
        xaxis_title=""
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

# ============================================================
# GOALS SCORED VS CONCEDED
# ============================================================

with col2:

    plot_df = summary.melt(
        id_vars="Season",
        value_vars=[
            "Goals_Scored_Per_Match",
            "Goals_Conceded_Per_Match"
        ],
        var_name="Metric",
        value_name="Goals per Match"
    )

    plot_df["Metric"] = plot_df["Metric"].replace({
        "Goals_Scored_Per_Match": "Goals Scored",
        "Goals_Conceded_Per_Match": "Goals Conceded"
    })

    fig = px.bar(
        plot_df,
        x="Season",
        y="Goals per Match",
        color="Metric",
        barmode="group",
        title="Goals Scored vs Goals Conceded"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

# ============================================================
# WIN RATE
# ============================================================

fig = px.bar(
    summary,
    x="Season",
    y="Win_%",
    text="Win_%",
    title="Arsenal Win Rate by Season"
)

fig.update_traces(
    texttemplate="%{text:.1f}%",
    textposition="outside"
)

fig.update_layout(
    yaxis_title="Win Rate (%)",
    xaxis_title=""
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# ============================================================
# GOAL DIFFERENCE
# ============================================================

fig = px.bar(
    summary,
    x="Season",
    y="Goal_Difference",
    text="Goal_Difference",
    title="Goal Difference by Season"
)

fig.update_traces(
    textposition="outside"
)

fig.update_layout(
    yaxis_title="Goal Difference",
    xaxis_title=""
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# ============================================================
# DATASET NOTE
# ============================================================

st.warning(
    "The 2022/23 season is incomplete in this dataset, "
    "so its metrics should not be compared directly "
    "with the completed 38-match seasons."
)
