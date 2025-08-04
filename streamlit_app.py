
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px

# Load the log file
@st.cache_data
def load_log():
    return pd.read_csv("action_log.csv")

# Set page layout
st.set_page_config(layout="wide")
st.title("\U0001F4C8 DRL Trading Agent Dashboard")

# Info box
st.info("""
**Model:** PPO  
**Objective:** Maximize Sharpe Ratio  
**Environment:** Multi-Asset Gym (BTC + S&P500)  
**Training steps:** 10,000  
""")

# Load and display raw data
log_df = load_log()
st.subheader("\U0001F4C4 Sample of Agent Actions")
st.dataframe(log_df.tail(10))

# Calculate Cumulative Reward
log_df["Cumulative_Reward"] = log_df["Reward"].cumsum()
fig_reward, ax_reward = plt.subplots(figsize=(10, 4))
ax_reward.plot(log_df["Step"], log_df["Cumulative_Reward"])
ax_reward.set_title("Agent Performance Over Time")
ax_reward.set_xlabel("Step")
ax_reward.set_ylabel("Cumulative Reward")

# Calculate Portfolio Value
log_df["Portfolio_Value"] = (1 + log_df["Reward"]).cumprod()
fig_portfolio, ax_portfolio = plt.subplots(figsize=(10, 4))
ax_portfolio.plot(log_df["Step"], log_df["Portfolio_Value"])
ax_portfolio.set_title("Simulated Portfolio Value Over Time")
ax_portfolio.set_xlabel("Step")
ax_portfolio.set_ylabel("Portfolio Value ($)")

# Rolling Sharpe Ratio
window = 100
rolling_mean = log_df["Reward"].rolling(window).mean()
rolling_std = log_df["Reward"].rolling(window).std()
rolling_sharpe = rolling_mean / (rolling_std + 1e-8)
fig_sharpe, ax_sharpe = plt.subplots(figsize=(10, 3))
ax_sharpe.plot(log_df["Step"], rolling_sharpe)
ax_sharpe.set_title(f"Rolling Sharpe Ratio (Window={window})")
ax_sharpe.set_xlabel("Step")
ax_sharpe.set_ylabel("Sharpe Ratio")

# Drawdown Analysis
log_df["Peak"] = log_df["Portfolio_Value"].cummax()
log_df["Drawdown"] = (log_df["Portfolio_Value"] - log_df["Peak"]) / log_df["Peak"]
fig_dd, ax_dd = plt.subplots(figsize=(10, 3))
ax_dd.plot(log_df["Step"], log_df["Drawdown"])
ax_dd.set_title("Portfolio Drawdown Over Time")
ax_dd.set_xlabel("Step")
ax_dd.set_ylabel("Drawdown")

# Tab layout
tab1, tab2, tab3 = st.tabs(["\U0001F4C8 Performance", "\U0001F4CA Actions", "\U0001F4D1 Analysis"])

with tab1:
    st.pyplot(fig_reward)
    st.pyplot(fig_portfolio)
    st.pyplot(fig_sharpe)
    st.pyplot(fig_dd)

with tab2:
    st.subheader("\U0001F9E0 Action Distribution")
    st.write("**BTC Actions:**")
    st.bar_chart(log_df["BTC_action"].value_counts())
    st.write("**S&P500 Actions:**")
    st.bar_chart(log_df["SP500_action"].value_counts())

    # Pie charts
    st.plotly_chart(px.pie(log_df, names="BTC_action", title="BTC Action Breakdown"))
    st.plotly_chart(px.pie(log_df, names="SP500_action", title="S&P500 Action Breakdown"))

with tab3:
    # Comparison Table (optional values - replace with real ones if multiple agents used)
    comparison = pd.DataFrame({
        "Algorithm": ["PPO", "DQN", "SAC"],
        "Sharpe Ratio": [14.88, 10.12, 12.76],
        "Final Portfolio Value": [log_df["Portfolio_Value"].iloc[-1], 9076, 9932],
        "Training Steps": [10000, 10000, 10000]
    })
    st.subheader("\U0001F4CA Algorithm Comparison")
    st.dataframe(comparison)

# Download CSV
st.download_button(
    label="\U0001F4E5 Download Action Log CSV",
    data=log_df.to_csv(index=False),
    file_name='drl_agent_log.csv',
    mime='text/csv'
)
