# 💎 The Conway Series: Ultimate Broker Dashboard

Welcome to the latest installment of the **"Conway Series"** my personal collection of computational "side-quests." This project is a high-performance, 3-panel interactive trading suite designed to deconstruct market momentum in real-time.


---

## 💡 The "Conway" Story
Why the name? It started as a fun code-name for my early scripts, and now it serves as an "Easter Egg" throughout my portfolio. It represents the transition from a physics student to a quant-engineer who builds high-end tools just for the thrill of the build.

## 🛠️ Technical Highlights

### 1. The 3-Panel Architecture
The dashboard is split into three distinct synchronized zones:
* **Zone 1 (Price):** 1-minute Candlestick charts with a 9-period Moving Average overlay.
* **Zone 2 (Momentum):** A professional **Relative Strength Index (RSI)** implementing Wilder’s Smoothing logic to identify overbought/oversold conditions.
* **Zone 3 (Volume):** Real-time bar charts to verify the strength of price moves.



### 2. Solving the "Market Gap" Problem
Standard time-series plots often show ugly blank spaces during weekends and nights. I solved this by forcing the X-axis to render as **Categorical Data**, ensuring a continuous, professional "Bloomberg-style" flow regardless of market closures.

### 3. Automated Broker Logic
The suite includes a "Broker Verdict" engine that cross-references price position against the MA9 and RSI levels to provide instant feedback:
* **Bullish Entry:** Price > MA9 + RSI under 70.
* **Mean Reversion:** RSI > 70 (Overbought) or < 30 (Oversold).

---

## 🧰 Tech Stack
* **Graphics Engine:** Plotly (Interactive WebGL)
* **Data Feed:** yfinance (Real-time REST API)
* **Math:** NumPy, Pandas (EMA/Wilder's Smoothing)

## 🧪 The "Fun" Part
The best part was implementing the **Live Price Annotation**. Using a paper-reference coordinate system, the current price "floats" on the right-hand axis in a cyan-colored tag, giving it that modern, digital-terminal feel.

---
*Developed for the fun of deconstructing the market.*
