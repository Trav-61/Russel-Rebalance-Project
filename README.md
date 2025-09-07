Russell 3000 Rebalance Analysis
Overview

This project analyzes the performance impact of Russell 3000 index reconstitutions by comparing securities added vs. deleted from the index around the rebalance date.

The workflow:

Extract index additions & deletions from PDFs published by FTSE Russell.

Convert to structured CSVs using pdfplumber and pandas.

Download historical data for additions, deletions, and the Russell 3000 index (^RUA) via yfinance.

Normalize prices to compare performance across tickers.

Aggregate & visualize median normalized performance of additions, deletions, and index over time.

This is designed as a quant-style research project that could be extended into a trading strategy.

Tech Stack

Python 3.11+

Libraries:

pdfplumber — extract tables from Russell rebalance PDFs

pandas — data manipulation

yfinance — pull market data

matplotlib — visualization

Custom modules:

Historical_Data_yfinance.py → fetch & clean OHLCV data

normal_price.py → normalize price series


Outputs:

R3000_additions.csv and R3000_deletions.csv → cleaned constituent lists

R3000_<StartDate>_to_<EndDate>.csv → combined OHLCV dataset

Normalized performance plot comparing:

Russell 3000 additions

Russell 3000 deletions

Russell 3000 index (^RUA)

Example Output

<img width="1000" height="600" alt="Figure_1" src="https://github.com/user-attachments/assets/8f7dd1e9-a1e4-4780-a029-d6eb58573d59" />




Next Steps / Extensions

Backtesting long/short strategies around index inclusions.

Creating a backtesting / portfolio managament tool to test strategy parameters

Adding risk-adjusted metrics (Sharpe, drawdowns, hit ratio).

Automating rebalance PDF ingestion across multiple years.


License

MIT License. Free to use and adapt with attribution.
