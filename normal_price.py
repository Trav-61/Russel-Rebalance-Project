# Normalize prices relative to earliest available price

import pandas as pd
import datetime as dt


def normal_price(df, Date, format, price, ticker):
    """
    Normalizes a price column so that each ticker starts at 1 
    (relative to its earliest available price).

    Parameters
    ----------
    df : pandas.DataFrame
        The input DataFrame containing price data.
    Date : str
        Name of the column in `df` containing date values.
    format : str
        String format of the date column (e.g. "%Y-%m-%d").
    price : str
        Name of the column in `df` containing price values to normalize.
    ticker : str
        Name of the column in `df` identifying the ticker/symbol.

    Returns
    -------
    pandas.DataFrame
        The same DataFrame with an additional column:
        'Normalized_<price>' containing the normalized price series.
    """

    # Convert the Date column into datetime format
    df['dt'] = pd.to_datetime(df[Date], format=format)

    # Sort rows by Ticker and Date so the earliest price comes first
    df = df.sort_values([ticker, 'dt']).reset_index(drop=True)

    # Create a new column with normalized prices
    # (divide each price by the first price for that ticker)
    df[f'Normalized_{price}'] = df.groupby(ticker)[price].transform(
        lambda x: x / x.iloc[0]
    )

    # Return the DataFrame with the new normalized column
    return df
