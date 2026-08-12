import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path


# --------------------------------------------------
# PAGE CONFIG
# --------------------------------------------------
st.set_page_config(
    page_title="Coach Analysis",
    page_icon="🧑‍💼",
    layout="wide"
)


# --------------------------------------------------
# DATA PATH
# --------------------------------------------------
DATA_DIR = Path(__file__).resolve().parents[2] / "data" / "raw"


# --------------------------------------------------
# LOAD MATCH DATA
# --------------------------------------------------
@st.cache_data
def load_matches():

    match_df = pd.read_csv(
        DATA_DIR / "matches.csv"
    )

    # Result
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

    # Points
    match_df["Points"] = match_df["Result"].map({
        "Win": 3,
        "Draw": 1,
        "Loss": 0
    })

    # Goal Difference
    match_df["GoalDifference"] = (
        match_df["ArsenalScore"]
        - match_df["OpponentScore"]
    )

    return match_df


match_df = load_matches()


# --------------------------------------------------
# HEADER
# --------------------------------------------------
st.title("🧑‍💼 Coach Analysis")

st.caption(
    "Business Question 2 — "
    "How did Arsenal perform under different coaches?"
)


# --------------------------------------------------
# COACH SUMMARY
# --------------------------------------------------
summary = (
    match_df
    .groupby("Coach")
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


# --------------------------------------------------
# CALCULATED METRICS
# --------------------------------------------------
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


# --------------------------------------------------
# KPI CARDS
# --------------------------------------------------
best_ppm = summary.loc[summary["PPM"].idxmax()]
best_win = summary.loc[summary["Win_%"].idxmax()]
best_gd = summary.loc[summary["Goal_Difference"].idxmax()]

c1, c2, c3, c4 = st.columns(4)

c1.metric(
    "Highest PPM",
    f"{best_ppm['PPM']:.2f}",
    best_ppm["Coach"]
)

c2.metric(
    "Highest Win Rate",
    f"{best_win['Win_%']:.1f}%",
    best_win["Coach"]
)

c3.metric(
    "Best Goal Difference",
    f"{best_gd['Goal_Difference']:+.0f}",
    best_gd["Coach"]
)

c4.metric(
    "Coaches Analysed",
    summary["Coach"].nunique()
)


# --------------------------------------------------
# SUMMARY TABLE
# --------------------------------------------------
st.subheader("📊 Coach Performance Summary")

st.dataframe(
    summary.style.format({
        "Win_%": "{:.2f}%",
        "PPM": "{:.2f}",
        "Goals_Scored_Per_Match": "{:.2f}",
        "Goals_Conceded_Per_Match": "{:.2f}"
    }),
    use_container_width=True
)


# --------------------------------------------------
# WIN RATE & PPM
# --------------------------------------------------
col1, col2 = st.columns(2)


with col1:

    fig = px.bar(
        summary.sort_values("Win_%"),
        x="Win_%",
        y="Coach",
        orientation="h",
        text="Win_%",
        title="Win Rate by Coach"
    )

    fig.update_traces(
        texttemplate="%{text:.1f}%",
        textposition="outside"
    )

    fig.update_layout(
        xaxis_title="Win Rate (%)",
        yaxis_title=""
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


with col2:

    fig = px.bar(
        summary.sort_values("PPM"),
        x="PPM",
        y="Coach",
        orientation="h",
        text="PPM",
        title="Points Per Match by Coach"
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


# --------------------------------------------------
# GOALS SCORED VS CONCEDED
# --------------------------------------------------
plot_df = summary.melt(
    id_vars="Coach",
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
    x="Coach",
    y="Goals per Match",
    color="Metric",
    barmode="group",
    title="Goals Scored vs Goals Conceded per Match"
)

st.plotly_chart(
    fig,
    use_container_width=True
)


# --------------------------------------------------
# GOAL DIFFERENCE
# --------------------------------------------------
fig = px.bar(
    summary.sort_values("Goal_Difference"),
    x="Goal_Difference",
    y="Coach",
    orientation="h",
    text="Goal_Difference",
    title="Goal Difference by Coach"
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


# --------------------------------------------------
# ANALYTICAL NOTE
# --------------------------------------------------
st.info(
    "Coach comparisons are observational rather than causal. "
    "Differences in sample size, squad quality, competition context, "
    "player availability and managerial tenure can influence the results. "
    "Very small samples, particularly Albert Stuivenberg and "
    "Freddie Ljungberg, should therefore be interpreted cautiously."
)
