"""
CORD-19 Data Analysis & Visualization
Author: Brayern Mwangi
Date: 2025

This script loads the CORD-19 dataset (metadata.csv),
cleans and prepares it, performs exploratory analysis,
creates visualizations, and provides an interactive
Streamlit app for exploration.
"""

# =====================================================
# Imports
# =====================================================
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from collections import Counter
import re
import streamlit as st

# =====================================================
# Part 1: Load & Explore Data
# =====================================================
# Path to local file (update <YourName> to your actual username)
file_path = r"C:/Users/Brayern/Downloads/PLP/Python/Week 8/metadata.csv"

# Load dataset
df = pd.read_csv(file_path, low_memory=False)

print("First 5 rows:")
print(df.head())

print("\nDataFrame dimensions:", df.shape)
print("\nColumn data types:")
print(df.dtypes)

important_cols = ["title", "abstract", "publish_time", "authors", "journal"]
print("\nMissing values in important columns:")
print(df[important_cols].isnull().sum())

print("\nBasic statistics for numerical columns:")
print(df.describe())

# =====================================================
# Part 2: Data Cleaning & Preparation
# =====================================================
# Drop rows missing essential info (title, publish_time)
cleaned_df = df.dropna(subset=["title", "publish_time"]).copy()

# Fill missing abstracts with empty string
cleaned_df["abstract"] = cleaned_df["abstract"].fillna("")

# Convert publish_time to datetime
cleaned_df["publish_time"] = pd.to_datetime(cleaned_df["publish_time"], errors="coerce")

# Extract publication year
cleaned_df["publish_year"] = cleaned_df["publish_time"].dt.year

# Add feature: abstract word count
cleaned_df["abstract_word_count"] = cleaned_df["abstract"].apply(lambda x: len(str(x).split()))

print("\nCleaned DataFrame dimensions:", cleaned_df.shape)
print(cleaned_df[["title", "publish_time", "publish_year", "abstract_word_count"]].head())

# =====================================================
# Part 3: Analysis & Visualization
# =====================================================
# Papers per year
papers_per_year = cleaned_df["publish_year"].value_counts().sort_index()
print("\nPapers per year:")
print(papers_per_year)

plt.figure(figsize=(10,6))
sns.lineplot(x=papers_per_year.index, y=papers_per_year.values, marker="o")
plt.title("Number of Publications per Year")
plt.xlabel("Year")
plt.ylabel("Count")
plt.show()

# Top journals
top_journals = cleaned_df["journal"].value_counts().head(10)
print("\nTop Journals:")
print(top_journals)

plt.figure(figsize=(10,6))
sns.barplot(x=top_journals.values, y=top_journals.index, palette="viridis")
plt.title("Top 10 Journals Publishing COVID-19 Research")
plt.xlabel("Number of Publications")
plt.ylabel("Journal")
plt.show()

# Word frequency in titles
titles = cleaned_df["title"].dropna().str.lower()
words = re.findall(r'\w+', " ".join(titles))
word_counts = Counter(words)
common_words = word_counts.most_common(20)
print("\nMost frequent words in titles:")
print(common_words)


# Sources
if "source_x" in cleaned_df.columns:
    source_counts = cleaned_df["source_x"].value_counts().head(10)
    plt.figure(figsize=(10,6))
    sns.barplot(x=source_counts.values, y=source_counts.index, palette="magma")
    plt.title("Top Sources of Papers")
    plt.xlabel("Number of Papers")
    plt.ylabel("Source")
    plt.show()

# =====================================================
# Part 4: Streamlit Application
# =====================================================
# Run this section only if executed via: streamlit run this_script.py

def run_app():
    st.title("CORD-19 COVID-19 Research Explorer")
    st.markdown("Explore trends, journals, and topics from the CORD-19 dataset.")

    # Sidebar filter: select year range
    year_filter = st.sidebar.slider(
        "Select Year Range",
        int(cleaned_df["publish_year"].min()),
        int(cleaned_df["publish_year"].max()),
        (2019, 2023)
    )
    filtered_df = cleaned_df[
        (cleaned_df["publish_year"] >= year_filter[0]) & 
        (cleaned_df["publish_year"] <= year_filter[1])
    ]

    # Show sample
    st.subheader("Sample Data")
    st.write(filtered_df.sample(5))

    # Publications per year
    st.subheader("Publications Over Time")
    papers_per_year = filtered_df["publish_year"].value_counts().sort_index()
    fig, ax = plt.subplots(figsize=(8,5))
    sns.lineplot(x=papers_per_year.index, y=papers_per_year.values, marker="o", ax=ax)
    st.pyplot(fig)

    # Top journals
    st.subheader("Top Journals")
    top_journals = filtered_df["journal"].value_counts().head(10)
    fig, ax = plt.subplots(figsize=(8,5))
    sns.barplot(x=top_journals.values, y=top_journals.index, ax=ax, palette="viridis")
    st.pyplot(fig)


    # Sources
    if "source_x" in filtered_df.columns:
        st.subheader("Top Sources of Papers")
        source_counts = filtered_df["source_x"].value_counts().head(10)
        fig, ax = plt.subplots(figsize=(8,5))
        sns.barplot(x=source_counts.values, y=source_counts.index, ax=ax, palette="magma")
        st.pyplot(fig)

# Detect if running under Streamlit
try:
    import streamlit.web.cli as stcli
    import sys
    if st._is_running_with_streamlit:
        run_app()
except:
    pass
"""
# =====================================================
# Part 5: Documentation & Reflection
# =====================================================

Findings:
---------
1. Research output spiked in 2020–2021 due to the COVID-19 pandemic.
2. Leading journals include BMJ, The Lancet, Nature, and Journal of Medical Virology.
3. Common words in titles: covid, coronavirus, sars, infection, health, pandemic.
4. Preprint servers (bioRxiv, medRxiv) were key sources for early dissemination.

Reflection:
-----------
- Challenge: Handling missing values and ensuring datetime consistency.
- Challenge: Large file size required careful memory handling.
- Learning: Feature engineering (abstract word count) and visualization 
  provided new insights into research patterns.
- Learning: Streamlit turned static analysis into an interactive tool 
  for broader accessibility.
"""
