import streamlit as st
import pandas as pd
import altair as alt

# ------------------------------------------
# LOAD CSV
# ------------------------------------------
@st.cache_data
def load_data():
    df = pd.read_csv("fraud_analysis_final.csv")

    # Clean and standardize the timestamp
    df["timestamp"] = pd.to_datetime(df["timestamp"], errors="coerce").dt.floor("D")

    # Create daily date column
    df["date"] = df["timestamp"].dt.date

    # Clean keyword column (split comma-separated keywords)
    df["keywords"] = df["keywords"].fillna("").apply(lambda x: [k.strip().lower() for k in x.split(",") if k.strip()])

    return df

df = load_data()

st.title("📊 Fraud Intelli Analytics Dashboard")

st.markdown("### Explore trends in fraud-related articles using your scraped dataset.")

# ------------------------------------------
# DAILY ARTICLE VOLUME
# ------------------------------------------
st.header("📅 Article Volume Over Time")

daily_counts = (
    df.groupby("date")
      .size()
      .reset_index(name="count")
)

line_chart = (
    alt.Chart(daily_counts)
    .mark_line(point=True, strokeWidth=2)
    .encode(
        x=alt.X("date:T", title="Date"),
        y=alt.Y("count:Q", title="Article Count"),
        tooltip=["date", "count"]
    )
    .properties(height=350)
)

st.altair_chart(line_chart, use_container_width=True)

# ------------------------------------------
# KEYWORD FREQUENCY TREND
# ------------------------------------------
st.header("🔥 Top Trending Fraud Keywords")

# Turn list of keywords into individual rows
keyword_rows = []

for _, row in df.iterrows():
    for kw in row["keywords"]:
        keyword_rows.append({"date": row["date"], "keyword": kw})

keyword_df = pd.DataFrame(keyword_rows)

if not keyword_df.empty:
    keyword_counts = (
        keyword_df.groupby(["date", "keyword"])
                  .size()
                  .reset_index(name="count")
    )

    keyword_chart = (
        alt.Chart(keyword_counts)
        .mark_line(point=True)
        .encode(
            x=alt.X("date:T", title="Date"),
            y=alt.Y("count:Q", title="Keyword Count"),
            color=alt.Color("keyword:N", title="Keyword"),
            tooltip=["date", "keyword", "count"]
        )
        .properties(height=350)
    )

    st.altair_chart(keyword_chart, use_container_width=True)
else:
    st.info("No keyword data found in the CSV.")
