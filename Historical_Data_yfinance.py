# Create a portfolio of all additions and deletions 
# and grab historical data between two timeframes

import pandas as pd
import datetime as dt
import yfinance as yf


def Historic_Data_y(File_Location, File_Names, Start_Date, End_Date):
    """
    Pulls tickers from CSV files, downloads historical data via yfinance,
    calculates extra metrics, and saves the result as a combined CSV.

    Parameters
    ----------
    File_Location : str
        The folder path where the input CSV files are stored.
    File_Names : list of str
        A list of CSV file names to read (e.g. 
        ["R3000_additions.csv", "R3000_deletions.csv"]).
        Each file must have a 'Symbol' column containing ticker symbols.
    Start_Date : str
        The start date for the historical data pull, in ISO format "YYYY-MM-DD".
    End_Date : str
        The end date for the historical data pull, in ISO format "YYYY-MM-DD".

    Returns
    -------
    None
        Saves a CSV file to `File_Location` named:
        "R3000_<Start_Date>_to_<End_Date>.csv"

    Notes
    -----
    - The saved CSV contains:
        * Date
        * Ticker
        * OHLCV (Open, High, Low, Close, Volume)
        * Typical Price = (High + Low + Close) / 3
        * Value Traded = Typical Price * Volume
    - Uses yfinance under the hood to download market data.
    """


    # Empty DataFrame to hold combined additions and deletions
    file_all = pd.DataFrame()

    # Loop through all input CSV files and append their contents
    for i in range(len(File_Names)):
        file_loop = pd.read_csv(File_Location + File_Names[i], index_col=0)
        file_all = pd.concat([file_all, file_loop]).reset_index(drop=True)

    # Extract ticker symbols into a list
    tickers = file_all[['Symbol']]
    tickers_list = list(tickers['Symbol'])

    # Download OHLCV data for all tickers between start and end dates
    data_yf_download = yf.download(
        tickers_list, start=Start_Date, end=End_Date, group_by='ticker'
    )

    # Flatten the multi-index DataFrame so Ticker is a column
    data_df = data_yf_download.stack(level=0).rename_axis(['Date', 'Ticker']).reset_index()

    # Calculate typical price as the mean of high, low, and close
    data_df['Typical Price'] = (data_df['High'] + data_df['Low'] + data_df['Close']) / 3

    # Calculate value traded as typical price multiplied by volume
    data_df['Value Traded'] = data_df['Typical Price'] * data_df['Volume']

    # Save final dataset to CSV in the specified folder
    data_df.to_csv(
        f'C:\\Users\\trav6\\OneDrive\\Documents\\Personal Learning\\Coding Projects\\Russel Rebalance Code\\Data\\R3000_{Start_Date}_to_{End_Date}.csv',
        index=False
    )
