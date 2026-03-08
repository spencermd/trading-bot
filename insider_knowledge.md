# 📈 INSIDER TRADING KNOWLEDGE
## How to Read SEC Form 4 from openinsider.com

---

## WHAT IS INSIDER TRADING?

**Insiders** = Company executives, directors, 10%+ owners
- They know private information before public
- When THEY buy/sell, it's a signal

---

## TRANSACTION CODES

| Code | Meaning | Signal |
|------|---------|--------|
| **P** | Purchase | 🟢 BULLISH - Insider buying! |
| **S** | Sale | 🔴 BEARISH - Insider selling |
| **A** | Grant | ⚪ Neutral - Options grant |
| **D** | Sale | 🔴 BEARISH |
| **G** | Gift | ⚪ Neutral |
| **M** | Option Exercise | ⚪ Could be bullish or bearish |
| **X** | Option Exercise | ⚪ Check context |

---

## KEY INSIGHTS

### BULLISH Signals (Insider Buying):
- **P (Purchase)** - Insider using personal money to buy
- Multiple insiders buying same stock
- CEO/CFO buying = strong signal

### BEARISH Signals (Insider Selling):
- **S (Sale)** - Insider selling
- Large sales by executives
- Especially concerning if combined with bad news

### FILING DELAY:
- Insiders have 2 days to report
- "1" = Filed 1 day after trade
- "10" = Filed 10 days after (suspicious)

---

## HOW TO USE:

### 1. Find Recent "P" (Purchases)
- Go to openinsider.com/screener
- Filter by "P" in last 7 days
- Look for CEO/CFO purchases

### 2. Check Filing Delay
- Delay < 3 days = Fresh information
- Delay > 5 days = Less relevant

### 3. Position Size Matters
- $100K+ purchase = Serious signal
- $1M+ purchase = Very serious

### 4. Sector Rotation
- Insiders in same sector buying = sector momentum

---

## SCANNER CREATED

- `insider_scanner.py` - Monitors openinsider.com
- Runs daily scan
- Outputs tickers with insider activity

---

## ACTIONABLE STRATEGY:

1. Check openinsider.com daily
2. Filter for "P" (purchases) last 7 days
3. Look for CEO/CFO with $100K+ purchase
4. Research the company
5. If fundamentals align → Enter position

**Key Insight:** When insiders buy, they know something. Follow their money.
