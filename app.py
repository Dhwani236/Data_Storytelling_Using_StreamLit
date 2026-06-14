import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np

# ---------------------------------------------------
# PAGE CONFIG
# ---------------------------------------------------

st.set_page_config(
    page_title="Global Layoffs Storytelling Dashboard",
    page_icon="",
    layout="wide"
)

# ---------------------------------------------------
# TITLE SECTION
# ---------------------------------------------------

st.title("Global Layoffs Storytelling Dashboard")
st.markdown("""
This interactive dashboard explores the global layoffs crisis across industries and companies.
Using storytelling techniques and visual analytics, we analyze:

- Which industries were affected the most
- Which companies laid off the highest number of employees
- Layoff trends over time
- Country-wise impact
- Funding vs layoffs relationship
""")

# ---------------------------------------------------
# LOAD DATA
# ---------------------------------------------------

@st.cache_data

def load_data():
    df = pd.read_csv("layoffs.csv")
    return df


df = load_data()

# ---------------------------------------------------
# DATA CLEANING
# ---------------------------------------------------

# Remove missing rows

df = df.dropna(subset=['total_laid_off'])

# Convert date column

df['date'] = pd.to_datetime(df['date'])

# Fill missing industry

df['industry'] = df['industry'].fillna('Unknown')

# Fill missing country

df['country'] = df['country'].fillna('Unknown')

# ---------------------------------------------------
# SIDEBAR FILTERS
# ---------------------------------------------------

st.sidebar.header("Filters")

selected_country = st.sidebar.multiselect(
    "Select Country",
    options=df['country'].unique(),
    default=df['country'].unique()
)

selected_industry = st.sidebar.multiselect(
    "Select Industry",
    options=df['industry'].unique(),
    default=df['industry'].unique()
)

filtered_df = df[
    (df['country'].isin(selected_country)) &
    (df['industry'].isin(selected_industry))
]

# ---------------------------------------------------
# KPI SECTION
# ---------------------------------------------------

st.subheader("Key Insights")

col1, col2, col3, col4 = st.columns(4)

with col1:
    total_layoffs = int(filtered_df['total_laid_off'].sum())
    st.metric("Total Layoffs", f"{total_layoffs:,}")

with col2:
    total_companies = filtered_df['company'].nunique()
    st.metric("Companies Affected", total_companies)

with col3:
    total_countries = filtered_df['country'].nunique()
    st.metric("Countries", total_countries)

with col4:
    avg_layoff = int(filtered_df['total_laid_off'].mean())
    st.metric("Average Layoffs", avg_layoff)

# ---------------------------------------------------
# STORY SECTION 1
# ---------------------------------------------------

st.markdown("---")
st.header("Story 1: Which Industries Were Hit the Hardest?")

industry_data = filtered_df.groupby('industry')['total_laid_off'].sum().reset_index()
industry_data = industry_data.sort_values(by='total_laid_off', ascending=False).head(10)

fig1 = px.bar(
    industry_data,
    x='industry',
    y='total_laid_off',
    color='total_laid_off',
    title='Top Industries by Layoffs'
)

st.plotly_chart(fig1, use_container_width=True)

st.markdown("""
### Observation

The technology sector dominates the layoffs landscape.
Rapid hiring during the post-pandemic boom created workforce expansion,
which later resulted in mass layoffs during economic slowdowns.
""")

# ---------------------------------------------------
# STORY SECTION 2
# ---------------------------------------------------

st.markdown("---")
st.header("Story 2: Which Companies Had the Largest Layoffs?")

company_data = filtered_df.groupby('company')['total_laid_off'].sum().reset_index()
company_data = company_data.sort_values(by='total_laid_off', ascending=False).head(15)

fig2 = px.pie(
    company_data,
    values='total_laid_off',
    names='company',
    title='Top Companies by Layoffs'
)

st.plotly_chart(fig2, use_container_width=True)

st.markdown("""
### Observation

Large multinational companies reduced workforce aggressively.
Many firms focused on cost-cutting strategies and operational efficiency.
""")

# ---------------------------------------------------
# STORY SECTION 3
# ---------------------------------------------------

st.markdown("---")
st.header("Story 3: Layoffs Over Time")

monthly = filtered_df.groupby(filtered_df['date'].dt.to_period('M'))['total_laid_off'].sum().reset_index()
monthly['date'] = monthly['date'].astype(str)

fig3 = px.line(
    monthly,
    x='date',
    y='total_laid_off',
    markers=True,
    title='Monthly Layoff Trend'
)

st.plotly_chart(fig3, use_container_width=True)

st.markdown("""
### Observation

Layoffs increased sharply during economic uncertainty periods.
The graph clearly shows waves of hiring corrections across industries.
""")

# ---------------------------------------------------
# STORY SECTION 4
# ---------------------------------------------------

st.markdown("---")
st.header("Story 4: Country-wise Impact")

country_data = filtered_df.groupby('country')['total_laid_off'].sum().reset_index()
country_data = country_data.sort_values(by='total_laid_off', ascending=False).head(10)

fig4 = px.scatter(
    country_data,
    x='country',
    y='total_laid_off',
    size='total_laid_off',
    color='total_laid_off',
    title='Country-wise Layoffs'
)

st.plotly_chart(fig4, use_container_width=True)

st.markdown("""
### Observation

The United States experienced the highest layoffs due to the concentration
of global technology companies and startups.
""")

# ---------------------------------------------------
# STORY SECTION 5
# ---------------------------------------------------

st.markdown("---")
st.header("Story 5: Funding vs Layoffs")

funding_df = filtered_df.dropna(subset=['funds_raised'])

fig5 = px.scatter(
    funding_df,
    x='funds_raised',
    y='total_laid_off',
    color='industry',
    hover_name='company',
    title='Funding Raised vs Layoffs'
)

st.plotly_chart(fig5, use_container_width=True)

st.markdown("""
### Observation

Even companies with high funding conducted layoffs.
This suggests that funding alone does not guarantee long-term workforce stability.
""")

# ---------------------------------------------------
# FINAL SUMMARY
# ---------------------------------------------------

st.markdown("---")
st.header("Final Conclusion")

st.success("""
This case study demonstrates how data storytelling can convert raw data
into meaningful business insights.

Key conclusions:

- Technology industry suffered the highest layoffs.
- Economic slowdowns strongly influenced workforce reductions.
- Layoffs occurred globally, but major impact was seen in the US.
- High funding does not always prevent layoffs.
- Interactive visualizations help communicate complex insights effectively.
""")

