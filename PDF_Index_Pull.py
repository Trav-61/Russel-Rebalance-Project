# Pull index rebalance data via PDFs published on the website

import pdfplumber
import pandas as pd
import sys

# Open the deletions PDF with pdfplumber
with pdfplumber.open('C:\\Users\\trav6\\OneDrive\\Documents\\Personal Learning\\Coding Projects\\Russel Rebalance Code\\ru3000-deletions-20250627.pdf') as pdf:
    
    # Loop through all pages in the PDF
    for page_num, page in enumerate(pdf.pages):
        # Extract tables from the current page
        tables = page.extract_tables()
        # Print extracted tables (useful for debugging/validation)
        print(tables)

        # If no tables were found on the page, skip it
        if not tables:
            continue

        # Loop through all tables on the page
        for table_num, table in enumerate(tables, start=0):
            # If this is the very first table (page 0, table 0),
            # create a DataFrame with the first row as the column headers
            if page_num == 0 and table_num == 0:
                R3000_deletions = pd.DataFrame(columns=tables[0][0]) 

            # For all following tables, loop through rows and append them
            for row in table: 
                if table_num > 0:
                    R3000_deletions.loc[len(R3000_deletions)] = row



# Open the additions PDF with pdfplumber
with pdfplumber.open('C:\\Users\\trav6\\OneDrive\\Documents\\Personal Learning\\Coding Projects\\Russel Rebalance Code\\ru3000-additions-20250627.pdf') as pdf:
    
    # Loop through all pages
    for page_num, page in enumerate(pdf.pages):
        # Extract tables from the current page
        tables = page.extract_tables()
        # If no tables found, skip this page
        if not tables:
            continue
        
        # Loop through all tables on the page
        for table_num, table in enumerate(tables, start=0):
            # If this is the very first table (page 0, table 0),
            # use the first row as column headers to initialize the DataFrame
            if page_num == 0 and table_num == 0:
                R3000_additions = pd.DataFrame(columns=tables[0][0])
                
            # Append each row from subsequent tables into the DataFrame
            for row in table: 
                if table_num > 0:
                    R3000_additions.loc[len(R3000_additions)] = row



R3000_additions.to_csv('C:\\Users\\trav6\\OneDrive\\Documents\\Personal Learning\\Coding Projects\\Russel Rebalance Code\\Data\\R3000_additions.csv')
R3000_deletions.to_csv('C:\\Users\\trav6\\OneDrive\\Documents\\Personal Learning\\Coding Projects\\Russel Rebalance Code\\Data\\R3000_deletions.csv')




