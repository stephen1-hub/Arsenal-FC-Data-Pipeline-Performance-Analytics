import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path


# --------------------------------------------------
# PAGE CONFIG
# --------------------------------------------------
st.set_page_config(
    page_title="Player Analytics",
    page_icon="👤",
    layout="wide"
)


# --------------------------------------------------
# DATA PATH
# --------------------------------------------------
DATA_DIR = Path(__file__).resolve().parents[2] / "data" / "raw"


# --------------------------------------------------
# LOAD PLAYER DATA
# --------------------------------------------------
@st.cache_data
def load_players():

    players_df = pd.read_csv(
        DATA_DIR / "players.csv"
    )

    # Convert date
    players_df["Date"] = pd.to_datetime(
        players_df["Date"],
        errors="coerce"
    )

    # Create full player name
    players_df["Player"] = (
        players_df["FirstName"]
        .fillna("")
        .astype(str)
        .str.strip()
        + " "
        + players_df["LastName"]
        .fillna("")
        .astype(str)
        .str.strip()
    ).str.strip()

    # Numeric columns
    numeric = [
        "Min",
        "G",
        "A",
        "xG",
        "xAG",
        "PrgPas",
        "PrgCar",
        "Tackles",
        "Ints",
        "Blocks",
        "Touches",
        "S",
        "SoT"
    ]

    for col in numeric:
        if col in players_df.columns:
            players_df[col] = pd.to_numeric(
                players_df[col],
                errors="coerce"
            ).fillna(0)

    return players_df


players_df = load_players()


# --------------------------------------------------
# HEADER
# --------------------------------------------------
st.title("👤 Player Analytics")

st.caption(
    "Business Question 4 — "
    "Which players made the greatest contribution by position?"
)


# --------------------------------------------------
# POSITION FILTER
# --------------------------------------------------
positions = (
    ["All"]
    + sorted(
        players_df["Pos"]
        .dropna()
        .unique()
        .tolist()
    )
)

selected_pos = st.selectbox(
    "Position",
    positions
)


# --------------------------------------------------
# MINIMUM MINUTES FILTER
# --------------------------------------------------
min_minutes = st.slider(
    "Minimum minutes",
    min_value=0,
    max_value=int(players_df["Min"].max()),
    value=min(
        900,
        int(players_df["Min"].max())
    ),
    step=90
)


# --------------------------------------------------
# FILTER PLAYER DATA
# --------------------------------------------------
filtered_players_df = players_df.copy()

if selected_pos != "All":
    filtered_players_df = filtered_players_df[
        filtered_players_df["Pos"] == selected_pos
    ]

filtered_players_df = filtered_players_df[
    filtered_players_df["Min"] >= min_minutes
].copy()


# --------------------------------------------------
# PLAYER AGGREGATION
# --------------------------------------------------
agg = (
    filtered_players_df
    .groupby(["Player", "Pos"])
    .agg(
        Matches=("Date", "count"),
        Starts=("Start", "sum"),
        Minutes=("Min", "sum"),
        Goals=("G", "sum"),
        Assists=("A", "sum"),
        xG=("xG", "sum"),
        xAG=("xAG", "sum"),
        Progressive_Passes=("PrgPas", "sum"),
        Progressive_Carries=("PrgCar", "sum"),
        Tackles=("Tackles", "sum"),
        Interceptions=("Ints", "sum"),
        Blocks=("Blocks", "sum")
    )
    .reset_index()
)


# --------------------------------------------------
# PER 90 METRICS
# --------------------------------------------------
per_90_metrics = [
    "Goals",
    "Assists",
    "xG",
    "xAG",
    "Progressive_Passes",
    "Progressive_Carries",
    "Tackles",
    "Interceptions",
    "Blocks"
]

for metric in per_90_metrics:

    agg[f"{metric}_Per_90"] = (
        agg[metric]
        / agg["Minutes"]
        .replace(0, pd.NA)
        * 90
    )

    agg[f"{metric}_Per_90"] = (
        agg[f"{metric}_Per_90"]
        .fillna(0)
    )


# --------------------------------------------------
# RANKING METRIC
# --------------------------------------------------
sort_metric = st.selectbox(
    "Rank players by",
    [
        "Goals_Per_90",
        "Assists_Per_90",
        "xG_Per_90",
        "xAG_Per_90",
        "Progressive_Passes_Per_90",
        "Progressive_Carries_Per_90",
        "Tackles_Per_90",
        "Interceptions_Per_90"
    ]
)


# --------------------------------------------------
# PLAYER RANKING
# --------------------------------------------------
ranking = agg.sort_values(
    sort_metric,
    ascending=False
)


# --------------------------------------------------
# PLAYER TABLE
# --------------------------------------------------
st.subheader("📊 Player Performance Ranking")

display_columns = [
    "Player",
    "Pos",
    "Matches",
    "Starts",
    "Minutes",
    "Goals",
    "Assists",
    "Goals_Per_90",
    "Assists_Per_90",
    "xG_Per_90",
    "xAG_Per_90",
    "Progressive_Passes_Per_90",
    "Progressive_Carries_Per_90",
    "Tackles_Per_90",
    "Interceptions_Per_90"
]

st.dataframe(
    ranking[display_columns].style.format({
        "Goals_Per_90": "{:.3f}",
        "Assists_Per_90": "{:.3f}",
        "xG_Per_90": "{:.3f}",
        "xAG_Per_90": "{:.3f}",
        "Progressive_Passes_Per_90": "{:.2f}",
        "Progressive_Carries_Per_90": "{:.2f}",
        "Tackles_Per_90": "{:.2f}",
        "Interceptions_Per_90": "{:.2f}"
    }),
    use_container_width=True
)


# --------------------------------------------------
# TOP 10 PLAYERS
# --------------------------------------------------
top = (
    ranking
    .head(10)
    .sort_values(sort_metric)
)


fig = px.bar(
    top,
    x=sort_metric,
    y="Player",
    color="Pos",
    orientation="h",
    title=f"Top 10 Players — {sort_metric}"
)

fig.update_layout(
    xaxis_title=sort_metric.replace("_", " "),
    yaxis_title=""
)

st.plotly_chart(
    fig,
    use_container_width=True
)


# --------------------------------------------------
# PLAYER PROFILE
# --------------------------------------------------
st.subheader("🎯 Player Profile")

if not ranking.empty:

    selected_player = st.selectbox(
        "Select player",
        ranking["Player"].tolist()
    )

    profile = ranking[
        ranking["Player"] == selected_player
    ].iloc[0]


    # --------------------------------------------------
    # PLAYER KPIs
    # --------------------------------------------------
    c1, c2, c3, c4, c5 = st.columns(5)

    c1.metric(
        "Minutes",
        f"{profile['Minutes']:,.0f}"
    )

    c2.metric(
        "Goals",
        f"{profile['Goals']:.0f}"
    )

    c3.metric(
        "Assists",
        f"{profile['Assists']:.0f}"
    )

    c4.metric(
        "Goals / 90",
        f"{profile['Goals_Per_90']:.2f}"
    )

    c5.metric(
        "xG / 90",
        f"{profile['xG_Per_90']:.2f}"
    )


    # --------------------------------------------------
    # PERFORMANCE PROFILE
    # --------------------------------------------------
    metrics = pd.DataFrame({
        "Metric": [
            "Goals/90",
            "Assists/90",
            "xG/90",
            "xAG/90",
            "Progressive Passes/90",
            "Progressive Carries/90",
            "Tackles/90",
            "Interceptions/90"
        ],

        "Value": [
            profile["Goals_Per_90"],
            profile["Assists_Per_90"],
            profile["xG_Per_90"],
            profile["xAG_Per_90"],
            profile["Progressive_Passes_Per_90"],
            profile["Progressive_Carries_Per_90"],
            profile["Tackles_Per_90"],
            profile["Interceptions_Per_90"]
        ]
    })


    fig = px.bar(
        metrics,
        x="Value",
        y="Metric",
        orientation="h",
        title=f"{selected_player} — Performance Profile"
    )

    fig.update_layout(
        xaxis_title="Per 90",
        yaxis_title=""
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

else:

    st.warning(
        "No players match the selected filters."
    )