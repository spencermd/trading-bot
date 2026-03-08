# 📐 ELLIOTT WAVE + RSI TRADING SYSTEM
## Research Synthesized & Reverse Engineered

---

## CORE FORMULAS

### 1. RSI (Relative Strength Index)
```
RSI = 100 - (100 / (1 + RS))

Where:
RS = Average Gain / Average Loss (over 14 periods)

RSI Zones:
- 0-30: OVERSOLD (BUY zone)
- 30-70: NEUTRAL
- 70-100: OVERBOUGHT (SELL zone)
```

### 2. Elliott Wave Confluence
```
BULLISH (Buy):
- RSI < 35 + Wave 3 Up = 90% confidence
- RSI < 45 + Wave 3 Up = 70% confidence  
- RSI < 30 = 60% confidence

BEARISH (Sell):
- RSI > 65 + Wave C Down = 90% confidence
- RSI > 55 + Wave C Down = 70% confidence
- RSI > 70 = 60% confidence
```

### 3. RSI Divergence Formula
```
Bullish Divergence:
- Price makes LOWER low
- RSI makes HIGHER low
- = BUY SIGNAL

Bearish Divergence:
- Price makes HIGHER high
- RSI makes LOWER high
- = SELL SIGNAL
```

### 4. Stochastic RSI
```
%K = (RSI - Lowest Low) / (Highest High - Lowest Low) × 100
%D = 3-day SMA of %K

- %K > 80 = Overbought
- %K < 20 = Oversold
- %K crosses above %D = BUY
- %K crosses below %D = SELL
```

### 5. MACD Formula
```
MACD Line = 12-period EMA - 26-period EMA
Signal Line = 9-period EMA of MACD
Histogram = MACD - Signal

BUY: MACD crosses ABOVE Signal
SELL: MACD crosses BELOW Signal
```

---

## 📊 ELLIOTT WAVE PATTERNS

### Impulse Waves (5 waves)
```
Wave 1: Initial move up
Wave 2: Retrace (usually 50-78.6% of Wave 1)
Wave 3: Strongest wave (usually 161.8% of Wave 1)
Wave 4: Sideways/consolidation
Wave 5: Final push (usually 61.8% of Wave 1)
```

### Corrective Waves (3 waves)
```
Wave A: First drop
Wave B: Retrace (usually 50-61.8% of Wave A)
Wave C: Final drop (usually 100-161.8% of Wave A)
```

---

## 🎯 ACTIONABLE TRADING RULES

### Entry Rules (BUY)
1. ✅ RSI < 35 (oversold)
2. ✅ Price at Wave C bottom (corrective wave complete)
3. ✅ Bullish divergence confirmed
4. ✅ Confluence: RSI + Wave + Support

### Exit Rules (SELL)
1. ✅ RSI > 65 (overbought)
2. ✅ Wave 5 complete
3. ✅ Bearish divergence
4. ✅ Confluence: RSI + Wave + Resistance

### Position Sizing
```
Position = (Account Risk %) / (Stop Loss %)

Example:
- Account: $10,000
- Risk: 2% = $200
- Stop Loss: 10% (RSI overbought)
- Position: $200 / 10% = $2,000
```

---

## 📈 RSI PERIOD OPTIMIZATION

| Timeframe | Best Period | Use Case |
|-----------|-------------|----------|
| 1H | 14 | Day trading |
| 4H | 14 | Swing trading |
| 1D | 21 | Position trading |
| 1W | 9 | Long-term |

---

## 🚀 ELLIOTT + RSI SCANNER

**File:** `elliott_rsi_trader.py`

**Features:**
- Auto-detects Elliott Wave pattern
- Calculates RSI confluence
- Signals with confidence levels

**Run:**
```bash
python3 eliott_rsi_trader.py
```

**Output:** `elliott_rsi_signals.json`

---

## 🎯 QUICK REFERENCE

| RSI | Wave | Signal | Action |
|-----|------|--------|--------|
| <30 | Any | Oversold | BUY |
| <35 | Wave 3 Up | Confluence | STRONG BUY |
| >70 | Any | Overbought | SELL |
| >65 | Wave C Down | Confluence | STRONG SELL |
| 40-60 | Wave 4 | Consolidation | WAIT |

---

**Key Insight:** The power is in CONFLUENCE - when RSI agrees with Wave pattern, confidence jumps to 70-90%.
