import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
import plotly.express as px

st.set_page_config(page_title="Portfolio Dashboard", layout="wide")

st.title(" Portfolio Dashboard")

# -----------------------------
# INPUT UTILISATEUR
# -----------------------------
st.sidebar.header("Configuration")

tickers = st.sidebar.text_input(
    "Tickers (séparés par une virgule)",
    "AAPL,MSFT,TSLA"
)

start_date = st.sidebar.date_input("Date de début", pd.to_datetime("2023-01-01"))

# convertir en liste
tickers_list = [t.strip() for t in tickers.split(",")]

# -----------------------------
# DATA
# -----------------------------
data = yf.download(tickers_list, start=start_date)["Close"]

returns = data.pct_change().dropna()

# -----------------------------
# KPIs
# -----------------------------
st.subheader(" Indicateurs")

mean_returns = returns.mean() * 252
volatility = returns.std() * np.sqrt(252)

sharpe_ratio = mean_returns / volatility

col1, col2, col3 = st.columns(3)

col1.metric("Rendement annuel moyen", f"{mean_returns.mean():.2%}")
col2.metric("Volatilité moyenne", f"{volatility.mean():.2%}")
col3.metric("Sharpe ratio", f"{sharpe_ratio.mean():.2f}")

# -----------------------------
# PERFORMANCE
# -----------------------------
st.subheader(" Performance du portefeuille")

normalized = data / data.iloc[0]

fig_perf = px.line(normalized, title="Performance normalisée")

st.plotly_chart(fig_perf, use_container_width=True)

# -----------------------------
# ALLOCATION (égale)
# -----------------------------
st.subheader(" Allocation")

weights = np.array([1/len(tickers_list)] * len(tickers_list))

alloc_df = pd.DataFrame({
    "Ticker": tickers_list,
    "Poids": weights
})

fig_pie = px.pie(alloc_df, values="Poids", names="Ticker")

st.plotly_chart(fig_pie, use_container_width=True)

# -----------------------------
# MATRICE DE CORRÉLATION
# -----------------------------
st.subheader("🔗 Corrélation")

corr = returns.corr()

fig_corr = px.imshow(corr, text_auto=True, title="Matrice de corrélation")

st.plotly_chart(fig_corr, use_container_width=True)

# -----------------------------
# DRAWDOWN
# -----------------------------
st.subheader("📉 Drawdown")

cum_returns = (1 + returns).cumprod()
peak = cum_returns.cummax()
drawdown = (cum_returns - peak) / peak

fig_dd = px.line(drawdown, title="Drawdown")

st.plotly_chart(fig_dd, use_container_width=True)
streamlit run app.py
                
