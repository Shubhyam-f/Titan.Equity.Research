import pandas as pd
import yfinance as yf

# Define the updated jewellery-focused ticker mapping
tickers = {
    "NIFTY 50": "^NSEI",
    "Titan Company": "TITAN.NS",
    "Kalyan Jewellers": "KALYANKJIL.NS",
    "Lalithaa Jewellery": "LALITHAA.NS",
    "Thangamayil Jewellery": "THANGAMAYL.NS",
    "PC Jeweller": "PCJEWELLER.NS",
    "Sky Gold & Diamonds": "SKYGOLD.NS",
    "BlueStone Jewellery": "BLUESTONE.NS"
}

# 5-Year window ending strictly on 31st March 2026
start_date = "2021-03-26"
end_date = "2026-04-01"

# Download adjusted closing prices
raw_data = yf.download(
    tickers=list(tickers.values()),
    start=start_date,
    end=end_date,
    interval="1d",
    auto_adjust=False,
)["Adj Close"]

# Rename columns from ticker symbols to company names
reverse_mapping = {symbol: name for name, symbol in tickers.items()}
data = raw_data.rename(columns=reverse_mapping)

# Resample to weekly close (Friday) and clamp explicitly to 31st March 2026
weekly_closes = data.resample("W-FRI").last()
weekly_closes = weekly_closes.loc[:"2026-03-31"]

# Compute weekly percentage returns
# We DO NOT use .dropna() here so we don't lose the 5-year history of established companies
# just because newer IPOs (like Lalithaa or BlueStone) have no data in the earlier years.
weekly_returns = weekly_closes.pct_change()

# Format index as YYYY-MM-DD
weekly_returns.index = weekly_returns.index.strftime("%Y-%m-%d")
weekly_returns.index.name = "Date"

# Arrange columns with benchmark and Titan first
column_order = [
    "NIFTY 50",
    "Titan Company",
    "Kalyan Jewellers",
    "Lalithaa Jewellery",
    "Thangamayil Jewellery",
    "PC Jeweller",
    "Sky Gold & Diamonds",
    "BlueStone Jewellery"
]
weekly_returns = weekly_returns[[
    col for col in column_order if col in weekly_returns.columns]]

# Export to CSV
output_filename = "jewellery_peers_weekly_returns_5yr_FY26.csv"
weekly_returns.to_csv(output_filename)

print(f"Weekly returns saved to {output_filename}")
print(f"Date range: {weekly_returns.index[0]} to {weekly_returns.index[-1]}")
print(f"Total periods: {len(weekly_returns)} weeks")
print(weekly_returns.tail())
