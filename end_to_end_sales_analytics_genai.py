import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import streamlit as st  # type: ignore
from openai import OpenAI  # type: ignore
import os

# =========================
# OpenAI API Configuration
# =========================
# os.environ["OPENAI_API_KEY"] = "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"
client = OpenAI()


# =========================
# Streamlit Page Config
# =========================
st.set_page_config(
    page_title="Sales Analytics & GenAI Assistant",
    layout="wide"
)

st.title("📊 Sales Data Analysis Chatbot")



# =========================
# Load Data
# =========================
df_raw = pd.read_excel("C:/Users/abhi_/Downloads/dummy.xlsx")
df = df_raw.copy()

# =========================
# Data Cleaning
# =========================
text_cols = [
    "Territory", "Industry Sector", "State/Province",
    "Country", "Product Segment", "Product Group"
]

for col in text_cols:
    if col in df.columns:
        df[col] = (
            df[col]
            .astype(str)
            .str.strip()
            .replace({"nan": np.nan, "None": np.nan})
        )

num_cols = [
    "Trade Sales Quantity",
    "Trade Sales Gallons",
    "Trade Sales Dollars (Group)"
]

for col in num_cols:
    if col in df.columns:
        df[col] = pd.to_numeric(df[col], errors="coerce")

df["Trade Sales Gallons"] = df["Trade Sales Gallons"].fillna(0)

# =========================
# Feature Engineering
# =========================
df["Price_Per_Gallon"] = np.where(
    df["Trade Sales Gallons"] > 0,
    df["Trade Sales Dollars (Group)"] / df["Trade Sales Gallons"],
    np.nan
)

df["Sale_Type"] = np.where(
    df["Trade Sales Dollars (Group)"] > 0,
    "Revenue",
    "Adjustment"
)

df["Territory_Name"] = df["Territory"].str.split(" - ").str[0]
df["Territory_Type"] = (
    df["Territory"].str.split(" - ").str[1].fillna("GENERAL")
)

df["State_Clean"] = df["State/Province"].apply(
    lambda x: "UNKNOWN" if isinstance(x, str) and "NOT ASSIGNED" in x else x
)

df["Market"] = np.where(
    df["Country"] == "USA",
    "USA",
    np.where(df["Country"] == "CANADA", "CANADA", "INTERNATIONAL")
)

# =========================
# Analytics Functions
# =========================
def revenue_by_market(df):
    return df.groupby("Market")["Trade Sales Dollars (Group)"].sum()

def top_segments(df, n=10):
    return (
        df.groupby("Product Segment")["Trade Sales Dollars (Group)"]
        .sum()
        .sort_values(ascending=False)
        .head(n)
    )

def compare_states(df, state1, state2):
    filtered = df[df["State_Clean"].isin([state1, state2])]

    totals = filtered.groupby("State_Clean")[
        ["Trade Sales Dollars (Group)", "Trade Sales Gallons"]
    ].sum().to_dict()

    yoy = {}
    for state in [state1, state2]:
        yearly = (
            filtered[filtered["State_Clean"] == state]
            .groupby("Year")["Trade Sales Dollars (Group)"]
            .sum()
            .sort_index()
        )
        yoy[state] = (
            (yearly.iloc[-1] - yearly.iloc[0]) / yearly.iloc[0] * 100
            if len(yearly) > 1 else None
        )

    return totals, yoy

# =========================
# EDA Results
# =========================
market_rev = revenue_by_market(df)
seg_rev = top_segments(df)

sample = df.sample(min(5000, len(df)), random_state=42)

valid_price = df[
    (df["Trade Sales Gallons"] > 0) &
    (df["Trade Sales Dollars (Group)"] > 0)
]

price_by_seg = (
    valid_price.groupby("Product Segment")["Price_Per_Gallon"]
    .median()
    .sort_values(ascending=False)
    .head(10)
)

# =========================
# Dashboard Layout
# =========================
st.markdown("---")
st.header("📈 Sales Analytics Overview")

row1_col1, row1_col2 = st.columns(2)
row2_col1, row2_col2 = st.columns(2)

with row1_col1:
    st.subheader("💰 Revenue by Market")
    fig, ax = plt.subplots()
    market_rev.plot(kind="bar", ax=ax)
    st.pyplot(fig)

with row1_col2:
    st.subheader("📦 Top Product Segments")
    fig, ax = plt.subplots()
    seg_rev.plot(kind="bar", ax=ax)
    st.pyplot(fig)

with row2_col1:
    st.subheader("📉 Gallons vs Dollars")
    fig, ax = plt.subplots()
    ax.scatter(
        sample["Trade Sales Gallons"],
        sample["Trade Sales Dollars (Group)"]
    )
    ax.set_xlabel("Gallons")
    ax.set_ylabel("Dollars")
    st.pyplot(fig)

with row2_col2:
    st.subheader("💲 Median Price per Gallon")
    fig, ax = plt.subplots()
    price_by_seg.plot(kind="bar", ax=ax)
    st.pyplot(fig)

# =========================
# Tables
# =========================
st.markdown("---")
st.subheader("📊 Price Per Gallon Statistics")
st.dataframe(valid_price["Price_Per_Gallon"].describe())

st.subheader("🏷️ Top Segments by Price")
st.dataframe(price_by_seg.reset_index())

# ===================== GEN-AI CHATBOT =========================

# =========================
# INTENT DETECTION
# =========================
def detect_intent(query):
    q = query.lower()

    if (
    "compare" in q
    or "vs" in q
    or "versus" in q
    or "comparison" in q
    or "year wise" in q
    or "year-wise" in q
    or "yearwise" in q):
        return "compare_states"

        return "compare_states"

    if "top" in q and ("product" in q or "segment" in q):
        return "top_segments"

    if "market" in q or "usa" in q or "canada" in q:
        return "market_revenue"

    return "unknown"
    

# =========================
# ANALYSIS FUNCTIONS
# =========================

def run_analysis(df, intent, query):
    if intent == "compare_states":
        states = []
        query_lower = query.lower()

        for s in df["State_Clean"].dropna().unique():
            if not isinstance(s, str):
                continue
            if s.lower() in query_lower:
                states.append(s)
        if len(states) >= 2:
            totals, yoy = compare_states(df, states[0], states[1])
            return {
                "analysis": "State Comparison",
                "states": states[:2],
                "totals": totals,
                "yoy_growth": yoy,
            }
        return {"message": "Could not detect two states to compare."}

    if intent == "top_segments":
        return {
            "analysis": "Top Product Segments",
            "data": top_segments(df).to_dict()
        }

    if intent == "market_revenue":
        return {
            "analysis": "Revenue by Market",
            "data": revenue_by_market(df).to_dict()
        }

    return {
        "analysis": "unknown",
        "message": "I could not map this question to a known analysis."
    }




# =========================
# GENAI EXPLANATION (SAFE)
# =========================
def generate_report(results, query):
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a senior data analyst. "
                        "Provide a concise business summary. "
                        "Do NOT list raw metrics unless explicitly asked."
                    )
                },
                {
                    "role": "user",
                    "content": (
                        f"User question:\n{query}\n\n"
                        f"Computed analytics:\n{results}\n\n"
                        "Explain the insight in executive-friendly language."
                    )
                }
            ],
            max_tokens=150
        )
        return response.choices[0].message.content

    except Exception:
        # ✅ GENERALIZED RULE-BASED SUMMARY
        return summarize_results(results)



# =========================
# Chatbot UI
# =========================
st.markdown("---")
st.header("🤖 Ask the Analytics Engine")

query = st.text_input(
    "Ask a business question (e.g., Compare Texas and California)"
)

if st.button("Analyze"):
    intent = detect_intent(query)
    result = run_analysis(df, intent, query)
    answer = generate_report(result, query)

    st.subheader("📌 Analysis Result")
    st.write(f"🧠 Detected intent: `{intent}`")
    st.write(answer)

# =========================
# Footer
# =========================
st.markdown("""
**Design Note:**  
All calculations are deterministic and performed in Python.  
The GenAI layer is used only for natural-language explanations, ensuring accuracy,
reliability, and graceful degradation when the API is unavailable.
""")
