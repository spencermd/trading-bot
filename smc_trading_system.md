# 🎯 SMC & LIQUIDITY TRADING SYSTEM
## Smart Money Concepts + Market Structure

---

## 1. FAIR VALUE GAP (FVG)

### What is FVG?
```
FVG = Price gap between 3 candles where middle is lowest/highest

Bullish FVG:
[Green] [Green] [Green]
     GAP DOWN

Bearish FVG:
  [Red] [Red] [Red]
     GAP UP
```

### FVG Rules:
- **Bullish FVG**: Middle candle has lowest low, gap between candle 1 & 3
- **Bearish FVG**: Middle candle has highest high, gap between candle 1 & 3
- **FVG = Support/Resistance**: Price often returns to fill the gap

### Trading FVG:
```
BUY at Bullish FVG (Support)
SELL at Bearish FVG (Resistance)
```

---

## 2. MARKET STRUCTURE

### Swing Highs & Lows
```
Swing High = Candle with higher high than 2 candles on each side
Swing Low = Candle with lower low than 2 candles on each side
```

### Trend Identification:
```
UPTRAAD: Higher Highs (HH) + Higher Lows (HL)

     H
   H   H
 L     L   L

DOWNTREND: Lower Highs (LH) + Lower Lows (LL)

   L
 L   L   L
     H     H
```

### Market Structure Shift (MSS)
```
BULLISH MSS:
- Price breaks ABOVE previous swing high
- Trend changes from down to up

BEARISH MSS:
- Price breaks BELOW previous swing low
- Trend changes from up to down
```

---

## 3. LIQUIDITY ZONES

### What is Liquidity?
```
Liquidity = Areas where stop orders cluster
- Stop Loss Hunts happen here
- Smart Money takes liquidity then reverses
```

### Types of Liquidity:
```
1. EQUAL HIGHS (Resistance)
   - Multiple highs at same price level
   - Stops above = liquidity for sweep

2. EQUAL LOWS (Support)
   - Multiple lows at same price level
   - Stops below = liquidity for sweep

3. ORDER BLOCKS (OB)
   - Last green candle before drop (Bullish OB)
   - Last red candle before pump (Bearish OB)
   - Smart money orders = support/resistance
```

### Liquidity Hunt Pattern:
```
1. Price approaches liquidity zone
2. Stops get triggered (liquidity taken)
3. Smart money absorbs
4. Reversal occurs
5. Profit from the trap
```

---

## 4. ORDER BLOCKS (OB)

### Definition:
```
Bullish OB = Last green candle before significant drop
           = Institutional buy orders
           = Support when price returns

Bearish OB = Last red candle before significant pump
           = Institutional sell orders
           = Resistance when price returns
```

### Trading Order Blocks:
```
Entry: At OB zone
Stop: Below OB (bullish) / Above OB (bearish)
Target: Previous structure / next liquidity zone
```

---

## 🎯 SMC ENTRY RULES

### Bullish Entry (LONG):
1. ✅ Market Structure Shift (break above HH)
2. ✅ Price returns to FVG (support)
3. ✅ Bullish Order Block forms
4. ✅ Liquidity pool above (target)
5. ✅ Entry at FVG/OB confluence

### Bearish Entry (SHORT):
1. ✅ Market Structure Shift (break below LL)
2. ✅ Price returns to FVG (resistance)
3. ✅ Bearish Order Block forms
4. ✅ Liquidity pool below (target)
5. ✅ Entry at FVG/OB confluence

---

## 📊 SMC SCANNER

```python
def SMC_signal():
    # 1. Detect FVGs
    fvg_bullish = detect_bullish_fvg(prices)
    fvg_bearish = detect_bearish_fvg(prices)
    
    # 2. Market Structure
    trend = detect_trend(prices)  # HH/HL or LH/LL
    mss = detect_MSS(prices)  # Structure shift
    
    # 3. Liquidity
    liquidity_zones = find_liquidity(prices)
    
    # 4. Order Blocks
    order_blocks = detect_order_blocks(prices)
    
    # Combine for signal
    if fvg_bullish and mss == "BULLISH" and order_blocks:
        return "LONG"
    elif fvg_bearish and mss == "BEARISH" and order_blocks:
        return "SHORT"
```

---

## 🚀 QUICK REFERENCE

| Concept | Signal |
|---------|--------|
| Bullish FVG | Support - BUY |
| Bearish FVG | Resistance - SELL |
| HH + HL | Uptrend |
| LH + LL | Downtrend |
| Break above HH | Bullish MSS |
| Break below LL | Bearish MSS |
| Equal Highs | Liquidity zone |
| Order Block | Institutional orders |

---

**Key Insight:** Smart Money Concepts trade WITH the institutions, not against them. Find where they placed orders (Order Blocks) and trade the liquidity hunt.
