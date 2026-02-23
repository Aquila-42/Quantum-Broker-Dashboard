import yfinance as yf
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime

def run_ultimate_broker_suite():
    print("'"*100)
    print("💎 CONWAYS CONSULTANCY: ULTIMATE REAL-TIME QUANT SUITE 💎")
    print(f"    Market Session: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("."*100)
    
    ticker = input("\nEnter Stock Symbol (e.g., AAPL, RELIANCE.NS): ").upper().strip()
    cur = "₹" if ".NS" in ticker or ".BO" in ticker else "$"
    
    # 1. DATA FETCHING (Handling 2026 yfinance structure)
    # Fetching 5 days of 1-minute data
    df = yf.download(ticker, period="5d", interval="1m", progress=False)
    
    if df.empty: 
        return print(f"❌ Error: Feed Offline or Symbol '{ticker}' not found.")

    # Flatten columns if they are MultiIndex
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = [col[0] for col in df.columns.values]

    # 2. INDICATOR ENGINEERING
    # Moving Average (9-period)
    df['MA9'] = df['Close'].rolling(window=9).mean()

    # Professional RSI (Wilder’s Smoothing)
    window = 14
    delta = df['Close'].diff()
    gain = (delta.where(delta > 0, 0))
    loss = (-delta.where(delta < 0, 0))
    
    avg_gain = gain.ewm(alpha=1/window, min_periods=window, adjust=False).mean()
    avg_loss = loss.ewm(alpha=1/window, min_periods=window, adjust=False).mean()
    
    rs = avg_gain / avg_loss.replace(0, np.nan) 
    df['RSI'] = 100 - (100 / (1 + rs))
    
    # Drop rows with NaNs to ensure clean data for the verdict
    df.dropna(subset=['RSI', 'MA9'], inplace=True)

    # Convert Index to string format to prevent Plotly from trying to fill "time gaps"
    df['Time_Str'] = df.index.strftime('%Y-%m-%d %H:%M')

    # 3. 3-PANEL INTERACTIVE DASHBOARD
    fig = make_subplots(rows=3, cols=1, shared_xaxes=True, 
                        vertical_spacing=0.04, 
                        row_heights=[0.5, 0.2, 0.3],
                        subplot_titles=(f'{ticker} Price', 'RSI (Momentum)', 'Volume'))

    # PANEL 1: Candlesticks using Time_Str as X-axis to remove gaps
    fig.add_trace(go.Candlestick(x=df['Time_Str'], open=df['Open'], high=df['High'], 
                                 low=df['Low'], close=df['Close'], name='Price'), row=1, col=1)
    fig.add_trace(go.Scatter(x=df['Time_Str'], y=df['MA9'], line=dict(color='#00f2ff', width=1.5), name='MA9'), row=1, col=1)

    # PANEL 2: RSI
    fig.add_trace(go.Scatter(x=df['Time_Str'], y=df['RSI'], line=dict(color='#ffaa00', width=2), name='RSI'), row=2, col=1)
    fig.add_hline(y=70, line_dash="dash", line_color="#ef4f60", row=2, col=1) 
    fig.add_hline(y=30, line_dash="dash", line_color="#3dc985", row=2, col=1)

    # PANEL 3: Volume
    fig.add_trace(go.Bar(x=df['Time_Str'], y=df['Volume'], marker_color='#444444', name='Volume'), row=3, col=1)

    # STYLING & FIXING THE X-AXIS GAP
    fig.update_layout(
        template='plotly_dark', 
        xaxis_rangeslider_visible=False, 
        height=900,
        paper_bgcolor='#0b0d0f', 
        plot_bgcolor='#0b0d0f',
        margin=dict(l=10, r=80, t=50, b=10),
        hovermode='x unified'
    )
    
    # Force X-axis to be categorical to hide overnight/weekend gaps
    fig.update_xaxes(type='category', nticks=10)
    fig.update_yaxes(side='right', gridcolor='#1f2226')

    # LIVE PRICE ANNOTATION
    curr_p = float(df['Close'].iloc[-1])
    fig.add_annotation(xref="paper", yref="y1", x=1.02, y=curr_p, text=f"{cur}{curr_p:.2f}", 
                       showarrow=False, bgcolor="#00f2ff", font=dict(color="black", size=12, family="Arial Black"))

    fig.show()

    # 4. FINAL REPORT
    print_final_report(ticker, curr_p, cur, df)

def print_final_report(ticker, price, cur, df):
    rsi_val = df['RSI'].iloc[-1]
    ma9_val = df['MA9'].iloc[-1]
    
    print("\n" + "="*85)
    print(f"📊 BROKER VERDICT: {ticker}")
    print("="*85)
    
    if price > ma9_val and rsi_val < 70:
        verdict = "✅ BULLISH: Entry looks solid."
    elif rsi_val > 70:
        verdict = "⚠️ OVERBOUGHT: Risk of immediate correction."
    elif rsi_val < 30:
        verdict = "⚡ OVERSOLD: Potential bounce candidate."
    else:
        verdict = "Neutral: Sideways movement."

    print(f"VERDICT: {verdict}")
    print(f"Current Price: {cur}{price:.2f}")
    print(f"RSI Value: {rsi_val:.2f}")
    print("."*100)

if __name__ == "__main__":
    run_ultimate_broker_suite()
