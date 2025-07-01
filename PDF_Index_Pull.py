# Pull index rebalance data via PDFs published on the website

import pdfplumber
import pandas as pd
import sys

with pdfplumber.open('C:\\Users\\trav6\\OneDrive\\Documents\\Personal Learning\\Coding Projects\\Russel Rebalance Code\\ru3000-deletions-20250627.pdf') as pdf:
    for page_num, page in enumerate(pdf.pages):
        tables = page.extract_tables()
        print(tables)
        if not tables:
              continue
        for table_num, table in enumerate(tables, start=0):
            if page_num == 0 and table_num == 0:
                R3000_deletions = pd.DataFrame(columns=tables[0][0]) 
            for row in table: 
                if table_num > 0 :
                    R3000_deletions.loc[len(R3000_deletions)] = row


with pdfplumber.open('C:\\Users\\trav6\\OneDrive\\Documents\\Personal Learning\\Coding Projects\\Russel Rebalance Code\\ru3000-additions-20250627.pdf') as pdf:
    for page_num, page in enumerate(pdf.pages):
        tables = page.extract_tables()
        if not tables:
              continue
        
        for table_num, table in enumerate(tables, start=0):
            if page_num == 0 and table_num == 0:
                R3000_additions = pd.DataFrame(columns=tables[0][0])
                
            for row in table: 
                if table_num > 0 :
                    R3000_additions.loc[len(R3000_additions)] = row



print(R3000_additions)
print(R3000_deletions)
R3000_additions.to_csv('C:\\Users\\trav6\\OneDrive\\Documents\\Personal Learning\\Coding Projects\\Russel Rebalance Code\\R3000_additions.csv')
R3000_deletions.to_csv('C:\\Users\\trav6\\OneDrive\\Documents\\Personal Learning\\Coding Projects\\Russel Rebalance Code\\R3000_deletions.csv')




