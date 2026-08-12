import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path


# --------------------------------------------------
# PAGE CONFIG
# --------------------------------------------------
st.set_page_config(
    page_title="Goalkeeper Analytics",
    page_icon="🧤",
    layout="wide"
)


# --------------------------------------------------
# DATA PATH
# --------------------------------------------------
DATA_DIR = Path(__file__).resolve().parents[2] / "data" / "raw"


# --------------------------------------------------
# LOAD GOALKEEPER DATA
# --------------------------------------------------
@st.cache_data
def load_gk():

    goalkeepers_df = pd.read_csv(
        DATA_DIR / "goalkeepers.csv"
    )

    # Convert date
    goalkeepers_df["Date"] = pd.to_datetime(
        goalkeepers_df["Date"],
        errors="coerce"
    )

    # Create full player name
    goalkeepers_df["Player"] = (
        goalkeepers_df["FirstName"]
        .fillna("")
        .astype(str)
        .str.strip()
        + " "
        + goalkeepers_df["LastName"]
        .fillna("")
        .astype(str)
        .str.strip()
    ).str.strip()

    # Numeric columns
    numeric = [
        "Min",
        "SoTA",
        "GA",
        "Saves",
        "PSxG",
        "PKatt",
        "PKA",
        "PKm",
        "PassAtt",
        "Throws",
        "GKAtt"
    ]

    for col in numeric:
        if col in goalkeepers_df.columns:
            goalkeepers_df[col] = pd.to_numeric(
                goalkeepers_df[col],
                errors="coerce"
            ).fillna(0)

    return goalkeepers_df


goalkeepers_df = load_gk()


# --------------------------------------------------
# HEADER
# --------------------------------------------------
st.title("🧤 Goalkeeper Analytics")

st.caption(
    "Goalkeeper shot-stopping, penalty and distribution analysis"
)


# --------------------------------------------------
# GOALKEEPER AGGREGATION
# --------------------------------------------------
agg = (
    goalkeepers_df
    .groupby("Player")
    .agg(
        Matches=("Date", "count"),
        Starts=("Start", "sum"),
        Minutes=("Min", "sum"),
        Shots_on_Target_Against=("SoTA", "sum"),
        Goals_Conceded=("GA", "sum"),
        Saves=("Saves", "sum"),
        PSxG=("PSxG", "sum"),
        Penalties_Attempted=("PKatt", "sum"),
        Penalties_Saved=("PKm", "sum"),
        Pass_Attempts=("PassAtt", "sum"),
        Throws=("Throws", "sum"),
        GK_Attempts=("GKAtt", "sum")
    )
    .reset_index()
)


# --------------------------------------------------
# SAVE PERCENTAGE
# --------------------------------------------------
save_attempts = (
    agg["Saves"]
    + agg["Goals_Conceded"]
)

agg["Save_%"] = (
    agg["Saves"]
    / save_attempts.replace(0, pd.NA)
    * 100
)

agg["Save_%"] = agg["Save_%"].fillna(0)


# --------------------------------------------------
# GOALS PREVENTED
# --------------------------------------------------
agg["Goals_Prevented"] = (
    agg["PSxG"]
    - agg["Goals_Conceded"]
)


# --------------------------------------------------
# PER 90 METRICS
# --------------------------------------------------
agg["Goals_Conceded_Per_90"] = (
    agg["Goals_Conceded"]
    / agg["Minutes"].replace(0, pd.NA)
    * 90
)

agg["Saves_Per_90"] = (
    agg["Saves"]
    / agg["Minutes"].replace(0, pd.NA)
    * 90
)

agg["Goals_Conceded_Per_90"] = (
    agg["Goals_Conceded_Per_90"]
    .fillna(0)
)

agg["Saves_Per_90"] = (
    agg["Saves_Per_90"]
    .fillna(0)
)


# --------------------------------------------------
# MINIMUM MINUTES FILTER
# --------------------------------------------------
max_minutes = int(agg["Minutes"].max())

min_minutes = st.slider(
    "Minimum goalkeeper minutes",
    min_value=0,
    max_value=max(90, max_minutes),
    value=min(900, max_minutes),
    step=90
)


ranking = agg[
    agg["Minutes"] >= min_minutes
].copy()


# --------------------------------------------------
# KPI CARDS
# --------------------------------------------------
if not ranking.empty:

    best_save = ranking.loc[
        ranking["Save_%"].idxmax()
    ]

    best_prevention = ranking.loc[
        ranking["Goals_Prevented"].idxmax()
    ]

    best_saves_90 = ranking.loc[
        ranking["Saves_Per_90"].idxmax()
    ]

    lowest_conceded_90 = ranking.loc[
        ranking["Goals_Conceded_Per_90"].idxmin()
    ]

    c1, c2, c3, c4 = st.columns(4)

    c1.metric(
        "Best Save %",
        f"{best_save['Save_%']:.1f}%",
        best_save["Player"]
    )

    c2.metric(
        "Most Goals Prevented",
        f"{best_prevention['Goals_Prevented']:+.1f}",
        best_prevention["Player"]
    )

    c3.metric(
        "Highest Saves / 90",
        f"{best_saves_90['Saves_Per_90']:.2f}",
        best_saves_90["Player"]
    )

    c4.metric(
        "Lowest Goals Conceded / 90",
        f"{lowest_conceded_90['Goals_Conceded_Per_90']:.2f}",
        lowest_conceded_90["Player"]
    )


# --------------------------------------------------
# DATA TABLE
# --------------------------------------------------
st.subheader("📊 Goalkeeper Performance")

display_columns = [
    "Player",
    "Matches",
    "Starts",
    "Minutes",
    "Shots_on_Target_Against",
    "Goals_Conceded",
    "Saves",
    "Save_%",
    "Goals_Prevented",
    "Goals_Conceded_Per_90",
    "Saves_Per_90"
]

st.dataframe(
    ranking[display_columns].style.format({
        "Save_%": "{:.2f}%",
        "Goals_Prevented": "{:+.2f}",
        "Goals_Conceded_Per_90": "{:.2f}",
        "Saves_Per_90": "{:.2f}"
    }),
    use_container_width=True
)


# --------------------------------------------------
# CHARTS
# --------------------------------------------------
col1, col2 = st.columns(2)


# --------------------------------------------------
# SAVE PERCENTAGE
# --------------------------------------------------
with col1:

    save_chart = (
        ranking
        .sort_values("Save_%")
    )

    fig = px.bar(
        save_chart,
        x="Save_%",
        y="Player",
        orientation="h",
        text="Save_%",
        title="Save Percentage"
    )

    fig.update_traces(
        texttemplate="%{text:.1f}%",
        textposition="outside"
    )

    fig.update_layout(
        xaxis_title="Save Percentage (%)",
        yaxis_title=""
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


# --------------------------------------------------
# GOALS PREVENTED
# --------------------------------------------------
with col2:

    prevention_chart = (
        ranking
        .sort_values("Goals_Prevented")
    )

    fig = px.bar(
        prevention_chart,
        x="Goals_Prevented",
        y="Player",
        orientation="h",
        text="Goals_Prevented",
        title="Goals Prevented (PSxG − Goals Conceded)"
    )

    fig.update_traces(
        texttemplate="%{text:.1f}",
        textposition="outside"
    )

    fig.update_layout(
        xaxis_title="Goals Prevented",
        yaxis_title=""
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


# --------------------------------------------------
# SAVES PER 90
# --------------------------------------------------
fig = px.bar(
    ranking.sort_values("Saves_Per_90"),
    x="Saves_Per_90",
    y="Player",
    orientation="h",
    text="Saves_Per_90",
    title="Saves Per 90"
)

fig.update_traces(
    texttemplate="%{text:.2f}",
    textposition="outside"
)

fig.update_layout(
    xaxis_title="Saves Per 90",
    yaxis_title=""
)

st.plotly_chart(
    fig,
    use_container_width=True
)


# --------------------------------------------------
# GOALS CONCEDED PER 90
# --------------------------------------------------
fig = px.bar(
    ranking.sort_values("Goals_Conceded_Per_90"),
    x="Goals_Conceded_Per_90",
    y="Player",
    orientation="h",
    text="Goals_Conceded_Per_90",
    title="Goals Conceded Per 90"
)

fig.update_traces(
    texttemplate="%{text:.2f}",
    textposition="outside"
)

fig.update_layout(
    xaxis_title="Goals Conceded Per 90",
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
    "Goalkeeper metrics should be interpreted alongside sample size, "
    "defensive context and the quality of shots faced. Save percentage "
    "alone does not fully measure goalkeeper performance."
)
