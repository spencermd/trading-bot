# 📊 MARKET CIPHER TRADING SYSTEM
## Reverse Engineered from Research

---

## MARKET CIPHER A - COMPONENTS

### 1. EMA Crossover System
```
9 EMA + 21 EMA Crossover

- 9 EMA crosses ABOVE 21 EMA = BULLISH (LONG)
- 9 EMA crosses BELOW 21 EMA = BEARISH (SHORT)
```

### 2. RSI (Relative Strength Index)
```
RSI 70/30 Zones:
- RSI > 70 = OVERBOUGHT (SELL)
- RSI < 30 = OVERSOLD (BUY)
- RSI 50 = NEUTRAL
```

### 3. Stoch RSI (Stochastic RSI)
```
%K crosses above %D = BUY signal
%K crosses below %D = SELL signal
- <20 = Oversold
- >80 = Overbought
```

### 4. MACD (Moving Average Convergence Divergence)
```
MACD Line = 12 EMA - 26 EMA
Signal Line = 9 EMA of MACD
Histogram = MACD - Signal

- MACD crosses ABOVE Signal = BUY
- MACD crosses BELOW Signal = SELL
```

### 5. Trend Direction
```
- Price above EMA cloud = UPTREND
- Price below EMA cloud = DOWNTREND
- Price in EMA cloud = CONSOLIDATION
```

---

## MARKET CIPHER B - ADVANCED COMPONENTS

### 1. VWAP (Volume Weighted Average Price)
```
VWAP = Σ(Price × Volume) / Σ(Volume)

- Price ABOVE VWAP = BULLISH
- Price BELOW VWAP = BEARISH
```

### 2. CVD (Cumulative Volume Delta)
```
Volume Delta = Buy Volume - Sell Volume
CVD = Cumulative sum of Delta

- CVD rising = Buying pressure
- CVD falling = Selling pressure
```

### 3. Liquidity Zones
```
- High volume nodes = Support/Resistance
- Liquidity pools = Stop hunts occur here
- Smart money absorbs at these levels
```

### 4. Order Blocks
```
Order Block = Area where institutions placed orders
- Bullish OB = Recent green candle before drop
- Bearish OB = Recent red candle before pump
- Price returns to OB = High probability trade
```

### 5. Equilibrium (EQ)
```
EQ = VWAP line
- Price above EQ = Long bias
- Price below EQ = Short bias
```

### 6. Stop Hunt / Stop Loss Hunt
```
- Stop hunt = Price spikes to liquidate stops
- Usually precedes reversal
- Enter after stop hunt completes
```

---

## 🎯 MARKET CIPHER SIGNALS

### LONG (BUY) Signal - All must align:
1. ✅ 9 EMA > 21 EMA (crossover bullish)
2. ✅ RSI < 70, trending up
3. ✅ Stoch RSI crossing UP
4. ✅ MACD bullish crossover
5. ✅ Price above VWAP
6. ✅ CVD rising
7. ✅ Price above Equilibrium

### SHORT (SELL) Signal - All must align:
1. ✅ 9 EMA < 21 EMA (crossover bearish)
2. ✅ RSI > 30, trending down
3. ✅ Stoch RSI crossing DOWN
4. ✅ MACD bearish crossover
5. ✅ Price below VWAP
6. ✅ CVD falling
7. ✅ Price below Equilibrium

---

## 📐 CONFIDENCE SCORING

| Indicators Aligning | Confidence |
|---------------------|------------|
| 3/7 | Low (40%) |
| 4/7 | Medium (60%) |
| 5/7 | High (80%) |
| 6/7 | Very High (90%) |
| 7/7 | Maximum (99%) |

---

## 🚀 MARKET CIPHER SCANNER

```python
# Pseudocode
def market_cipher_signal():
    # Get indicators
    ema_9 = EMA(prices, 9)
    ema_21 = EMA(prices, 21)
    rsi = RSI(prices)
    stoch = StochasticRSI(prices)
    macd = MACD(prices)
    vwap = VWAP(prices)
    cvd = CVD(prices)
    
    # Score
    score = 0
    
    if ema_9 > ema_21: score += 1
    if rsi < 70 and rsi > 50: score += 1
    if stoch_crosses_up: score += 1
    if macd_bullish: score += 1
    if price > vwap: score += 1
    if cvd_rising: score += 1
    
    if score >= 5: return "LONG"
    elif score <= 1: return "SHORT"
    else: return "NEUTRAL"
```

---

## 🎯 ACTIONABLE RULES

### Entry Rules
1. Wait for EMA 9/21 crossover
2. Confirm RSI trending away from 50
3. Check Stoch RSI cross direction
4. Verify MACD alignment
5. Confirm VWAP position
6. Check CVD direction

### Exit Rules
1. RSI reaches 70/30
2. EMA反向 crossover
3. MACD divergence
4. Take profit at 2:1 R:R

### Risk Management
```
- Max risk per trade: 2%
- Stop loss: Recent swing low/high
- Take profit 1: 1.5R
- Take profit 2: 2R
- Take profit 3: 3R (trailing)
```

---

**Key Insight:** Market Cipher combines 7+ indicators. The more align, the higher the probability. Wait for confluence!
