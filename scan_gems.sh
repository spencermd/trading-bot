#!/bin/bash

# Fetch data from CryptoCompare
DATA=$(curl -s --max-time 20 "https://min-api.cryptocompare.com/data/top/mktcapfull?limit=200&tsym=USD")

# Use node to filter
node << 'NODESCRIPT'
const data = JSON.parse(process.env.DATA);
const gems = [];

data.Data.forEach(coin => {
  if (!coin.RAW?.USD) return;
  
  const mcap = coin.RAW.USD.MKTCAP;
  const change24h = coin.RAW.USD.CHANGEPCT24HOUR;
  
  // Filter: market cap $100K - $10M AND down 15%+ in 24h
  if (mcap >= 100000 && mcap <= 10000000 && change24h <= -15) {
    gems.push({
      name: coin.CoinInfo.FullName,
      symbol: coin.CoinInfo.Internal,
      mcap: mcap,
      change24h: change24h,
      price: coin.RAW.USD.PRICE
    });
  }
});

// Sort by market cap (smallest first)
gems.sort((a, b) => a.mcap - b.mcap);

console.log(JSON.stringify(gems.slice(0, 20), null, 2));
NODESCRIPT
