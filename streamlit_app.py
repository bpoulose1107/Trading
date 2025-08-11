# streamlit_app.py
import os, time, math, base64, pathlib
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

# ------------------ Page ------------------
st.set_page_config(
    page_title="DRL Trading Agent Dashboard",
    page_icon="assets/logo.png",
    layout="wide"
)

# ------------------ Load Logo + Header ------------------
logo_path = pathlib.Path("assets/logo.png")
logo_b64 = ""
if logo_path.exists():
    with open(logo_path, "rb") as f:
        logo_b64 = base64.b64encode(f.read()).decode()

st.markdown("""
<style>
.block-container {padding-top: 50px; padding-bottom: 2rem; max-width: 1220px;}
h1,h2,h3 {letter-spacing:.2px;}
.kpi {border-radius: 16px; padding: 16px 18px;
      background: linear-gradient(135deg,#1b2138 0%,#222b4a 100%);
      box-shadow: 0 10px 24px rgba(0,0,0,.25); border: 1px solid rgba(255,255,255,.06)}
.kpi .label {opacity:.8; font-size:.9rem; margin-bottom:.35rem}
.kpi .value {font-size:1.6rem; font-weight:800}
</style>
""", unsafe_allow_html=True)

if logo_b64:
    st.markdown(
        f"""
        <div style="display:flex;align-items:center;gap:16px;
                    padding:10px 14px;margin:-6px 0 12px 0;
                    background:linear-gradient(135deg,rgba(124,92,255,.12),rgba(15,18,32,.0));
                    border:1px solid rgba(255,255,255,.06); border-radius:16px;">
            <img src="data:image/png;base64,{logo_b64}"
                 style="height:85px;width:auto;border-radius:10px;
                        filter: brightness(1) drop-shadow(0 0 12px rgba(124,92,255,.55));"/>
            <div>
                <div style="font-size:22px;font-weight:900;letter-spacing:.3px;">
                    DRL Trading Agent Dashboard
                </div>
                <div style="opacity:.75;font-size:13px;margin-top:2px;">
                    Multi‑Asset • PPO • DQN • SAC
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )
else:
    st.title("📊 DRL Trading Agent Dashboard")

# ------------------ Sidebar ------------------
AGENTS = ["PPO", "DQN", "SAC"]
if "agent_idx" not in st.session_state:
    st.session_state.agent_idx = 0

with st.sidebar:
    st.caption("Demo Controls")
    cycle = st.checkbox("Auto cycle agents", value=False)
    interval = st.number_input("Cycle interval (sec)", 3, 30, 6)
    agent = st.selectbox("Select Agent", AGENTS, index=st.session_state.agent_idx)

if cycle:
    if "last_switch" not in st.session_state:
        st.session_state.last_switch = time.time()
    if time.time() - st.session_state.last_switch >= interval:
        st.session_state.agent_idx = (st.session_state.agent_idx + 1) % len(AGENTS)
        st.session_state.last_switch = time.time()
        st.experimental_rerun()
else:
    st.session_state.agent_idx = AGENTS.index(agent)

LOG_MAP = {"PPO": "logs/ppo_log.csv", "DQN": "logs/dqn_log.csv", "SAC": "logs/sac_log.csv"}

# ------------------ Helpers ------------------
@st.cache_data
def load_csv(path: str) -> pd.DataFrame:
    return pd.read_csv(path)

def safe_load(path: str):
    if not os.path.exists(path):
        st.error(f"Log not found: `{path}`"); return None
    try:
        df = load_csv(path)
        if "Step" not in df.columns: df["Step"] = np.arange(len(df))
        if "Reward" not in df.columns:
            st.error(f"`Reward` column missing in {path}"); return None
        for col in ["BTC_action","SP500_action"]:
            if col not in df.columns:
                df[col] = np.random.choice([0,1,2], size=len(df))
        return df
    except Exception as e:
        st.exception(e); return None

def compute_metrics(df: pd.DataFrame, win: int = 100, initial_capital: float = 10_000.0):
    df = df.copy()

    # Use returns, not raw rewards (auto-scale if rewards are in %)
    r_raw = df["Reward"].astype(float)
    r = r_raw / 100.0 if r_raw.abs().median() > 0.5 else r_raw

    # Optional: clip insane tail rewards to avoid exploding compounding (presentation only)
    r = r.clip(lower=-0.5, upper=0.5)

    # Core series
    df["Cumulative_Reward"] = r.cumsum()
    df["Gross_Return"] = (1.0 + r).cumprod()
    df["Portfolio_Value"] = df["Gross_Return"] * initial_capital

    # Drawdown
    df["Peak"] = df["Portfolio_Value"].cummax()
    df["Drawdown"] = (df["Portfolio_Value"] - df["Peak"]) / (df["Peak"] + 1e-12)

    # Rolling Sharpe
    rmean = r.rolling(win).mean()
    rstd  = r.rolling(win).std()
    rolling_sharpe = rmean / (rstd + 1e-8)
    last_sharpe = float(rolling_sharpe.iloc[-1]) if not math.isnan(rolling_sharpe.iloc[-1]) else 0.0

    # Annualized metrics (252 ~ trading days; adjust to your cadence)
    n = max(len(r), 1)
    growth_factor = float(df["Gross_Return"].iloc[-1])  # final/initial
    ann_return = growth_factor**(252/n) - 1
    ann_vol = float(r.std() * np.sqrt(252))

    final_val = float(df["Portfolio_Value"].iloc[-1]) if len(df) else initial_capital
    max_dd = float(df["Drawdown"].min()) if len(df) else 0.0
    return df, rolling_sharpe, last_sharpe, max_dd, final_val, ann_return, ann_vol

def short_money(x: float) -> str:
    num = float(x)
    for unit in ["", "K", "M", "B", "T"]:
        if abs(num) < 1000:
            return f"${num:,.2f}{unit}"
        num /= 1000.0
    return f"${num:,.2f}Q"

# ------------------ Load + Info ------------------
log_path = LOG_MAP[agent]
df = safe_load(log_path)

st.info(
    f"**Model:** {agent}  \n"
    f"**Objective:** Maximize Sharpe Ratio  \n"
    f"**Environment:** Multi-Asset Gym (BTC + S&P500)  \n"
    f"**Training steps:** 10,000"
)

if df is None or len(df) == 0:
    st.stop()

df, rolling_sharpe, last_sharpe, max_dd, final_val, ann_ret, ann_vol = compute_metrics(df)

# ------------------ KPIs ------------------
c1, c2, c3, c4 = st.columns(4)
with c1:
    st.markdown(f'<div class="kpi"><div class="label">Sharpe (rolling)</div>'
                f'<div class="value">{last_sharpe:.2f}</div></div>', unsafe_allow_html=True)
with c2:
    st.markdown(f'<div class="kpi"><div class="label">Max Drawdown</div>'
                f'<div class="value">{max_dd*100:.2f}%</div></div>', unsafe_allow_html=True)
with c3:
    st.markdown(f'<div class="kpi"><div class="label">Final Portfolio</div>'
                f'<div class="value">{short_money(final_val)}</div></div>', unsafe_allow_html=True)
with c4:
    st.markdown(f'<div class="kpi"><div class="label">Ann. Return / Vol</div>'
                f'<div class="value">{ann_ret*100:.1f}% / {ann_vol*100:.1f}%</div></div>', unsafe_allow_html=True)

# ------------------ Actions Sample (formatted for readability) ------------------
st.subheader("📄 Sample of Agent Actions")
_show = df.tail(12).copy()
_show["Portfolio_Value"] = _show["Portfolio_Value"].map(lambda x: f"${x:,.2f}")
_show["Drawdown"] = (_show["Drawdown"]*100).map(lambda x: f"{x:.2f}%")
st.dataframe(_show, use_container_width=True)

# ------------------ Tabs ------------------
t1, t2, t3 = st.tabs(["📊 Performance", "🎯 Actions", "📚 Analysis & Compare"])

with t1:
    fig1, ax1 = plt.subplots()
    ax1.plot(df["Step"], df["Cumulative_Reward"])
    ax1.set_title("Cumulative Reward"); ax1.set_xlabel("Step"); ax1.set_ylabel("Reward")
    st.pyplot(fig1, use_container_width=True)

    fig2, ax2 = plt.subplots()
    ax2.plot(df["Step"], df["Portfolio_Value"])
    ax2.set_title("Portfolio Value Over Time"); ax2.set_xlabel("Step"); ax2.set_ylabel("Value ($)")
    st.pyplot(fig2, use_container_width=True)

    fig3, ax3 = plt.subplots()
    ax3.plot(df["Step"], rolling_sharpe)
    ax3.set_title("Rolling Sharpe Ratio (Window=100)"); ax3.set_xlabel("Step"); ax3.set_ylabel("Sharpe")
    st.pyplot(fig3, use_container_width=True)

    fig4, ax4 = plt.subplots()
    ax4.plot(df["Step"], df["Drawdown"]*100.0)
    ax4.set_title("Portfolio Drawdown Over Time"); ax4.set_xlabel("Step"); ax4.set_ylabel("Drawdown (%)")
    st.pyplot(fig4, use_container_width=True)

with t2:
    colA, colB = st.columns(2)
    with colA:
        st.write("**BTC Actions (bar):**")
        st.bar_chart(df["BTC_action"].value_counts(), use_container_width=True)
        st.plotly_chart(px.pie(df, names="BTC_action", title="BTC Action Breakdown"), use_container_width=True)
    with colB:
        st.write("**S&P500 Actions (bar):**")
        st.bar_chart(df["SP500_action"].value_counts(), use_container_width=True)
        st.plotly_chart(px.pie(df, names="SP500_action", title="S&P500 Action Breakdown"), use_container_width=True)

with t3:
    st.caption("Compare headline metrics across agents from their CSV logs.")
    rows = []
    for a in AGENTS:
        p = LOG_MAP[a]
        xdf = safe_load(p)
        if xdf is None: 
            continue
        xdf, xroll, xsh, xdd, xval, xr, xv = compute_metrics(xdf)
        rows.append(dict(Algorithm=a, Sharpe=xsh, MaxDD=xdd*100, FinalValue=xval, AnnRet=xr*100, AnnVol=xv*100))
    if rows:
        comp = pd.DataFrame(rows)
        st.dataframe(comp.assign(
            MaxDD=lambda d: d["MaxDD"].map(lambda v: f"{v:.2f}%"),
            FinalValue=lambda d: d["FinalValue"].map(short_money),
            AnnRet=lambda d: d["AnnRet"].map(lambda v: f"{v:.2f}%"),
            AnnVol=lambda d: d["AnnVol"].map(lambda v: f"{v:.2f}%"),
        ), use_container_width=True)

        cA, cB = st.columns(2)
        with cA:
            st.plotly_chart(px.bar(comp, x="Algorithm", y="Sharpe", title="Sharpe (rolling, last)"),
                            use_container_width=True)
        with cB:
            st.plotly_chart(px.bar(comp, x="Algorithm", y="MaxDD", title="Max Drawdown (%)"),
                            use_container_width=True)
        st.plotly_chart(px.bar(comp, x="Algorithm", y="FinalValue", title="Final Portfolio Value ($)"),
                        use_container_width=True)

        cats = ["Sharpe (+)", "Risk (lower better)", "Ann. Return (+)"]
        figR = go.Figure()
        for _, r in comp.iterrows():
            figR.add_trace(go.Scatterpolar(
                r=[max(r.Sharpe,0), max(0, 100 - abs(r.MaxDD)), max(r.AnnRet,0)],
                theta=cats, fill='toself', name=r.Algorithm
            ))
        figR.update_layout(title="Agent Comparison (Radar)",
                           polar=dict(radialaxis=dict(visible=True)))
        st.plotly_chart(figR, use_container_width=True)

# ------------------ Download ------------------
st.download_button(
    label="📥 Download Current Agent Log",
    data=df.to_csv(index=False),
    file_name=f"{AGENTS[st.session_state.agent_idx].lower()}_log.csv",
    mime="text/csv",
    use_container_width=True
)
