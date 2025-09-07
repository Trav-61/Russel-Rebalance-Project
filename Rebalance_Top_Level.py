# ================================================================
# Import Required Libraries and Custom Modules
# ================================================================
import pandas as pd
import datetime as dt
import yfinance as yf
import Historical_Data_yfinance   # custom module to pull yfinance data
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import normal_price               # custom module to normalize prices
import sys


# ================================================================
# Script Keys and Config
# ================================================================
# Key to control whether to pull fresh yfinance historical data
# (set to >0 to pull, =0 to skip and use existing file)
key_his_y = 1

# Base location of input/output files
File_Location = 'C:\\Users\\trav6\\OneDrive\\Documents\\Personal Learning\\Coding Projects\\Russel Rebalance Code\\Data\\'

# Input CSVs that contain Russell 3000 additions and deletions
File_Names = ['R3000_additions.csv','R3000_deletions.csv']

# Date strings must be in ISO format (YYYY-MM-DD)
Start_Date = '2025-01-27'
End_Date = '2025-09-05'


# ================================================================
# Historical Data Pull (yfinance)
# ================================================================
# Only pull new data if key is turned on
if key_his_y > 0:
    Historic_Data = Historical_Data_yfinance.Historic_Data_y(
        File_Location, File_Names, Start_Date, End_Date
    )

# Read in the combined R3000 historic data previously created
historic_data = pd.read_csv(
    f'C:\\Users\\trav6\\OneDrive\\Documents\\Personal Learning\\Coding Projects\\Russel Rebalance Code\\Data\\R3000_{Start_Date}_to_{End_Date}.csv'
)

# Normalize historical close prices by ticker
historic_normal_close = normal_price.normal_price(
    historic_data, 'Date', '%Y-%m-%d', 'Close', 'Ticker'
)


# ================================================================
# Add Additions/Deletions Labels to Historic Data
# ================================================================
# Load additions and label them
R3000_additions = pd.read_csv(
    File_Location + 'R3000_additions.csv', index_col=0
)
R3000_additions['A/D'] = 'Add'

# Load deletions and label them
R3000_deletions = pd.read_csv(
    File_Location + 'R3000_deletions.csv', index_col=0
)
R3000_deletions['A/D'] = 'Del'

# Combine into one lookup DataFrame with Ticker + Add/Delete flag
R3000_AD = pd.concat([
    R3000_additions[['Symbol','A/D']],
    R3000_deletions[['Symbol','A/D']]
]).rename(columns={"Symbol": "Ticker"})

# Merge into the normalized close dataset
historic_normal_close = pd.merge(
    left=historic_normal_close, right=R3000_AD, 
    on='Ticker', how='left'
)

print(historic_normal_close)


# ================================================================
# Group Additions/Deletions by Date (median normalized close)
# ================================================================
# Filter for additions and group by date
additions = historic_normal_close[['Date','Normalized_Close']][
    historic_normal_close['A/D']=='Add'
]
additions_grouped = additions.groupby('Date')[['Normalized_Close']].median().reset_index()

# Filter for deletions and group by date
deletions = historic_normal_close[['Date','Normalized_Close']][
    historic_normal_close['A/D']=='Del'
]
deletions_grouped = deletions.groupby('Date')[['Normalized_Close']].median().reset_index()

print(deletions_grouped)
print(additions_grouped)


# ================================================================
# Russell 3000 Index (^RUA) Data from yfinance
# ================================================================
# Define index ticker
RUAT = "^RUA" 

# Download raw data for the index
RUAT_data = yf.download(RUAT, start=Start_Date, end=End_Date, group_by='ticker')

# Reshape into long format with Date, Ticker, Close
RUAT_data = RUAT_data.stack(level=0).rename_axis(['Date', 'Ticker']).reset_index()
RUAT_data = RUAT_data[['Date','Close','Ticker']]

# Normalize index close prices
RUAT_normal_close = normal_price.normal_price(
    RUAT_data , 'Date' , '%Y-%m-%d' , 'Close' , 'Ticker'
)
RUAT_normal_close = RUAT_normal_close[['Date','Normalized_Close']]


# ================================================================
# Plot Normalized Performance: Additions vs Deletions vs Index
# ================================================================
# Ensure datetime format
deletions_grouped['Date'] = pd.to_datetime(deletions_grouped['Date'])
additions_grouped['Date'] = pd.to_datetime(additions_grouped['Date'])
RUAT_normal_close['Date'] = pd.to_datetime(RUAT_normal_close['Date'])

plt.figure(figsize=(10,6))

# Plot deletions
plt.plot(
    deletions_grouped['Date'], deletions_grouped['Normalized_Close'],
    label='Deletions', color='red', marker='o'
)

# Plot additions
plt.plot(
    additions_grouped['Date'], additions_grouped['Normalized_Close'],
    label='Additions', color='green', marker='x'
)

# Plot Russell 3000 index
plt.plot(
    RUAT_normal_close['Date'], RUAT_normal_close['Normalized_Close'],
    label='RUAT', color='blue', marker='s'
)

# Chart formatting
plt.title('Normalized Close Comparison')
plt.xlabel('Date')
plt.ylabel('Normalized Close')
plt.grid(True)
plt.legend()
plt.tight_layout()

# Format x-axis ticks as dates
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
plt.gca().xaxis.set_major_locator(mdates.AutoDateLocator(maxticks=6))
plt.xticks(rotation=45, ha='right')  # rotate labels for readability

# Display the plot
plt.show()
