# ⚽ Arsenal FC Data Pipeline & Performance Analytics

## 📌 Project Overview

This project develops an end-to-end football data pipeline to collect, clean, transform, analyze, and visualize Arsenal Football Club performance data from **2017/18 to 2022/23**.

The analysis combines three datasets:

* `matches.csv` — Arsenal match-level results and match context
* `player.csv` — player appearances, attacking, creative, defensive and progression statistics
* `goalkeepers.csv` — goalkeeper shot-stopping and distribution statistics

The objective is to transform raw football data into **actionable performance insights** that could support coaching, recruitment, scouting, performance analysis and strategic decision-making.

> **Note:** The 2022/23 season is incomplete in the available dataset, with player data extending to February 2023.

---

## 🎯 Business Objectives

The project addresses five key business questions:

### 1. How did Arsenal's performance change from season to season?

Analyze:

* Wins, draws and losses
* Goals scored and conceded
* Points
* Win percentage
* Points per match
* Goal difference
* Home and away performance

### 2. How did Arsenal perform under different coaches?

Compare:

* Arsène Wenger
* Unai Emery
* Freddie Ljungberg
* Mikel Arteta
* Albert Stuivenberg

Metrics include:

* Win percentage
* Points per match
* Goals scored per match
* Goals conceded per match
* Goal difference

### 3. Which opponents have Arsenal historically performed well or poorly against?

Evaluate Arsenal's record against individual opponents using:

* Win percentage
* Points per match
* Goals scored per match
* Goals conceded per match
* Goal difference

### 4. Which Arsenal players made the greatest contribution within their respective positions?

Analyze player contribution across:

* Forwards
* Attacking midfielders
* Central/defensive midfielders
* Full-backs
* Centre-backs
* Wing-backs
* Goalkeepers

Metrics include:

* Goals and assists
* xG and xAG
* Goals/90 and assists/90
* Progressive passes
* Progressive carries
* Tackles
* Interceptions
* Blocks
* Goalkeeper save percentage
* Goals prevented

### 5. How did player contribution change across Arsenal's different coaching periods?

Compare player contribution during the Wenger, Emery and Arteta eras to investigate how Arsenal's performance profile evolved.

---

# 🗂️ Project Structure

```text
ArsenalFC-Data-Pipeline-Project/
│
├── data/
│   ├── raw/
│   │   ├── matches.csv
│   │   ├── player.csv
│   │   └── goalkeepers.csv
│   │
│   └── processed/
│       ├── clean_matches.csv
│       ├── clean_players.csv
│       └── clean_goalkeepers.csv
│
├── notebooks/
│   ├── 01_data_cleaning.ipynb
│   ├── 02_season_analysis.ipynb
│   ├── 03_coach_analysis.ipynb
│   ├── 04_opponent_analysis.ipynb
│   ├── 05_player_analysis.ipynb
│   └── 06_coaching_era_analysis.ipynb
│
├── src/
│   ├── data_cleaning.py
│   ├── feature_engineering.py
│   ├── player_metrics.py
│   └── coach_analysis.py
│
├── dashboard/
│   └── app.py
│
├── outputs/
│   ├── figures/
│   └── tables/
│
├── requirements.txt
├── README.md
└── .gitignore
```

---

# 🛠️ Technologies Used

### Programming & Data Analysis

* Python
* Pandas
* NumPy

### Visualization

* Matplotlib
* Seaborn
* Plotly

### Database / Data Engineering

* SQL
* MySQL
* Data cleaning and transformation pipelines

### Dashboard

* Streamlit

### Development

* Jupyter Notebook
* Git
* GitHub

---

# 🔄 Data Pipeline

The project follows an end-to-end analytical pipeline:

```text
Raw Football Data
       ↓
Data Ingestion
       ↓
Data Cleaning
       ↓
Data Validation
       ↓
Feature Engineering
       ↓
Analytical Datasets
       ↓
Business Analysis
       ↓
Visualization
       ↓
Dashboard
       ↓
Football Insights
```

---

# 🧹 Data Cleaning & Validation

The datasets were inspected for:

* Missing values
* Duplicate records
* Incorrect data types
* Date formatting
* Numerical consistency
* Invalid performance values
* Player-position consistency

For example, the match dataset contains **214 matches and 12 columns**, with no missing values across the available fields.

The player dataset contains **2,741 player-match records and 28 columns**.

The goalkeeper dataset contains **218 goalkeeper-match records and 19 columns**.

---

# 📊 Key Analysis

## 1. Season Performance

Arsenal's strongest season in the available sample based on win percentage was **2022/23**, although the season is incomplete in the dataset.

The available data shows:

| Season   | Matches | Wins | Draws | Losses |      Win % |      PPM |
| -------- | ------: | ---: | ----: | -----: | ---------: | -------: |
| 2017/18  |      38 |   19 |     6 |     13 |     50.00% |     1.66 |
| 2018/19  |      38 |   21 |     7 |     10 |     55.26% |     1.84 |
| 2019/20  |      38 |   14 |    14 |     10 |     36.84% |     1.47 |
| 2020/21  |      38 |   18 |     7 |     13 |     47.37% |     1.61 |
| 2021/22  |      38 |   22 |     3 |     13 |     57.89% |     1.82 |
| 2022/23* |      24 |   18 |     3 |      3 | **75.00%** | **2.38** |

*Incomplete season.

### Key insight

Arsenal's available 2022/23 data shows a substantial improvement in results, with **2.38 points per match** compared with **1.82 in 2021/22**.

---

# 🧑‍💼 2. Coaching Performance

| Coach              | Matches |      Win % |      PPM | Goals/Match | Conceded/Match |
| ------------------ | ------: | ---------: | -------: | ----------: | -------------: |
| Arsène Wenger      |      38 |     50.00% |     1.66 |        1.95 |           1.34 |
| Unai Emery         |      51 |     49.02% |     1.73 |        1.78 |           1.37 |
| Freddie Ljungberg  |       5 |     20.00% |     1.00 |        1.20 |           1.60 |
| Mikel Arteta       |     119 | **56.30%** | **1.85** |        1.67 |       **1.08** |
| Albert Stuivenberg |       1 |      0.00% |     0.00 |        1.00 |           2.00 |

### Key insight

Mikel Arteta recorded the strongest long-term coaching results in the available dataset:

* **56.3% win rate**
* **1.85 points per match**
* **1.08 goals conceded per match**

The defensive improvement is particularly notable.

---

# 🏟️ 3. Opponent Analysis

The opponent analysis identified significant differences in Arsenal's historical performance against individual teams.

### Strong records

Examples include:

* Huddersfield — **100% win rate**
* Fulham — **80%**
* Leeds — **80%**
* Newcastle — **72.73%**
* West Ham — **72.73%**
* Bournemouth — **71.43%**

### Difficult opponents

The most significant challenges in the dataset were:

#### Manchester City

* 11 matches
* 0 wins
* 11 losses
* 4 goals scored
* 29 goals conceded
* **-25 goal difference**

#### Liverpool

* 11 matches
* 2 wins
* 2 draws
* 7 losses
* 12 goals scored
* 31 conceded
* **-19 goal difference**

### Key insight

Arsenal's performance was highly opponent-dependent, with particularly difficult historical results against **Manchester City and Liverpool**.

---

# 🏠 4. Home Advantage

Arsenal played:

* **106 home matches**
* **108 away matches**

### Home

* 68 wins
* 19 draws
* 19 losses
* 64.15% win rate
* 2.10 PPM
* +106 goal difference

### Away

* 44 wins
* 21 draws
* 43 losses
* 40.74% win rate
* 1.42 PPM
* +5 goal difference

### Home advantage

The analysis identified:

* **+23.41 percentage points** in win rate
* **+0.69 PPM**
* **+0.95 goal-difference-per-match advantage**

### Key insight

Arsenal demonstrated a substantial home-performance advantage during the observed period.

---

# 👤 5. Player Performance

Player performance was analyzed according to **position rather than using one universal ranking**.

This prevents direct comparisons between players performing fundamentally different roles.

## Leading attacking profiles

### Pierre-Emerick Aubameyang

As a LW:

* 0.66 goals/90
* 0.16 assists/90
* 0.43 xG/90

As a FW:

* 0.55 goals/90
* 0.60 xG/90

**Profile:** Elite finisher.

### Alexandre Lacazette

* 0.49 goals/90
* 0.23 assists/90
* 0.48 xG/90

**Profile:** Finishing + creative contribution.

### Bukayo Saka

As RW:

* 0.41 goals/90
* 0.25 assists/90
* 0.32 xG/90
* 0.24 xAG/90

**Profile:** Scoring + creativity + progression.

---

# 🎯 Midfield Contribution

### Granit Xhaka

As CM:

* 10.26 progressive passes/90

As DM:

* 9.71 progressive passes/90
* 1.77 tackles/90
* 0.97 interceptions/90

**Profile:** High-volume progressive midfielder.

### Martin Ødegaard

* 0.26 goals/90
* 0.20 assists/90
* 0.24 xAG/90
* 7.40 progressive passes/90

**Profile:** Creative progression and attacking contribution.

### Mesut Özil

* 0.25 xAG/90
* 8.74 progressive passes/90
* 4.26 progressive carries/90

**Profile:** Elite creative midfielder.

---

# 🛡️ Defensive Contribution

### Ben White

As RB:

* 7.65 progressive passes/90
* 2.24 tackles/90
* 2.11 progressive carries/90

### Oleksandr Zinchenko

As LB:

* **9.87 progressive passes/90**
* 3.40 progressive carries/90
* 1.80 tackles/90

### Nacho Monreal

As CB:

* 2.46 interceptions/90
* 1.98 tackles/90

As LB:

* 0.20 assists/90
* 4.48 progressive passes/90

These results demonstrate the difference between **traditional defensive contribution** and the modern concept of **progressive defending/build-up contribution**.

---

# 🧤 Goalkeeper Analysis

### Bernd Leno

* 8,976 minutes
* 71.30% save rate
* 3.09 saves/90
* 1.27 goals conceded/90

### Aaron Ramsdale

* 5,220 minutes
* 70.30% save rate
* 1.07 goals conceded/90

### Emiliano Martínez

* 78.57% save rate
* +2.8 PSxG − GA

However, Martínez's sample was only **771 minutes**, so his efficiency should be interpreted cautiously.

### Key insight

Leno provides the strongest long-term goalkeeper sample, while Martínez recorded the strongest observed shot-stopping efficiency over a much smaller sample.

---

# 🔄 6. Coaching Era & Player Contribution

The analysis found an important difference between **player-level output** and **team-level results**.

| Coach     |  Goals/90 | Assists/90 |     xG/90 |    xAG/90 | Progressive Passes/90 |
| --------- | --------: | ---------: | --------: | --------: | --------------------: |
| Wenger    | **0.189** |  **0.162** | **0.178** | **0.142** |             **5.963** |
| Emery     |     0.171 |      0.124 |     0.154 |     0.115 |                 4.870 |
| Ljungberg |     0.120 |      0.080 |     0.108 |     0.064 |                 4.040 |
| Arteta    |     0.163 |      0.112 |     0.156 |     0.103 |                 4.655 |

### Key insight

Wenger's period recorded higher aggregate attacking and progression rates.

However, Arteta achieved:

* Higher win rate
* Higher PPM
* Lower goals conceded per match

This suggests that Arsenal's improvement under Arteta was **not simply a consequence of higher attacking volume**.

Instead, defensive efficiency, squad balance and broader player contribution appear to have played an important role.

---

# 💡 Executive Insights

### 1. Arsenal has a significant home advantage

The team won **64.15% of home matches** compared with **40.74% away matches**.

### 2. Manchester City was Arsenal's most difficult opponent

Arsenal recorded **0 wins in 11 matches**, with a -25 goal difference.

### 3. Arteta delivered the strongest long-term results

His **1.85 PPM and 56.3% win rate** were the strongest among the major coaching periods analyzed.

### 4. Defensive efficiency was a major differentiator

Arteta's Arsenal conceded **1.08 goals per match**, compared with:

* Wenger: 1.34
* Emery: 1.37

### 5. Saka developed into a multidimensional contributor

His contribution extends beyond goals and assists into **progressive passing and carrying**.

### 6. Arsenal's player contribution became more distributed

Under Arteta, players such as **Saka, Ødegaard, Martinelli, Gabriel and Partey** contributed across different phases of play.

---

# 📈 Recommended Dashboard

The final Streamlit dashboard should contain:

```text
Arsenal FC Analytics
│
├── 🏠 Overview
│
├── 📅 Season Performance
│
├── 🧑‍💼 Coach Analysis
│
├── 🏟️ Opponent Analysis
│
├── 👤 Player Analytics
│
├── 🧤 Goalkeeper Analytics
│
└── 🔄 Coaching Era Comparison
```

### Overview

Display:

* Matches
* Wins
* Win %
* PPM
* Goals scored
* Goals conceded
* Goal difference
* Home advantage

### Player Analytics

Filters:

```text
Position
Player
Minimum Minutes
```

Visualizations:

* Goals/90
* Assists/90
* xG/90
* xAG/90
* Progressive passes/90
* Progressive carries/90
* Tackles/90
* Interceptions/90

### Coach Analysis

Interactive comparison of:

* Win %
* PPM
* Goals scored
* Goals conceded
* Goal difference

### Coaching Era Comparison

Compare:

**Wenger → Emery → Arteta**

across:

* Team results
* Player contribution
* Attacking output
* Defensive output
* Progression

---

# 🚀 Future Improvements

Potential extensions include:

* Expected points modelling
* Opponent-strength adjustment
* Player contribution index
* Rolling performance trends
* Player age analysis
* Transfer/recruitment analysis
* Formation analysis
* Home vs away player performance
* Match-state analysis
* Predictive match modelling
* Player scouting reports
* Automated data ingestion

---

# 📌 Limitations

Several limitations should be considered:

1. The **2022/23 season is incomplete**.
2. Some players have relatively small samples.
3. Per-90 metrics can be unstable with limited minutes.
4. Coach comparisons are observational and should not be interpreted as causal proof.
5. `PSxG - GA` is model-dependent and should be treated as supporting goalkeeper evidence.
6. Historical opponent samples differ substantially in size.
7. Player roles can change between positions during their Arsenal careers.

---

# 🏁 Conclusion

This project demonstrates how football data can be transformed from raw match and player records into actionable performance intelligence.

The analysis shows that Arsenal's performance between 2017 and 2023 was influenced by several dimensions:

**team results → opponent strength → home advantage → player roles → coaching periods → defensive efficiency → player development.**

The most important finding is that **better team performance does not necessarily mean higher aggregate attacking output**.

Arsenal's Arteta-era improvement was accompanied by stronger results and a significantly better defensive record, while individual contribution became increasingly distributed across a developing group of players.

This demonstrates the value of combining **match data, player analytics and coaching-period analysis** rather than evaluating football performance through a single metric.

---

## 👨‍💻 Author

**Stephen Yaw Ayamah**

Football Data Analyst | Data Analyst | Sports Analytics

### Technical Skills

`Python` `SQL` `Pandas` `NumPy` `Power BI` `Streamlit` `Data Visualization` `Football Analytics`

---

## ⭐ Project Objective

The ultimate goal of this project is to demonstrate how football data engineering and analytics can support:

* Performance analysis
* Recruitment
* Scouting
* Tactical analysis
* Player evaluation
* Coaching decisions
* Strategic decision-making
