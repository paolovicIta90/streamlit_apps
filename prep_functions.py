import datetime
from datetime import date
import pandas as pd

import datetime as dt
from datetime import date


def create_df_from_transactions(transactions):
    df=pd.DataFrame(transactions)
    return df

def extract_last_purchase_year(df,year):
    df=df.copy()
    df_year = df[df['year'] <= year]
    year_last_purchase = df_year[df_year['action'] == 'buy']['year'].max()
    return year_last_purchase

def extract_last_year_rent_out(df, year):
    df=df.copy()
    df_year = df[df['year'] <= year]
    year_last_rent_out = df_year[df_year['action'] == 'rent_out']['year'].max()
    return year_last_rent_out

def assign_last_purchase_year_and_rent_out(df):
    df=df.copy()
    df['year_last_purchase'] = df['year'].apply(lambda x: extract_last_purchase_year(df, x))
    df['year_last_rent_out'] = df['year'].apply(lambda x: extract_last_year_rent_out(df, x))
    return df

def add_rent_actions(df):
    df=df.copy()
    df = df.set_index('year')
    # Identifying the 'sell' actions where the next action is 'buy'
    sell_indices = df[df['action'] == 'sell'].index
    buy_indices = df[df['action'] == 'buy'].index
    df=df.reset_index()

    # Create rows for 'rent' actions
    rent_rows = []
    if df['year'].min() > 1:
        for year in range(1, df['year'].min()):
           rent_rows.append({'action': 'rent', 'year': year, 'year_last_purchase': 0}) 

    for sell_index in sell_indices:
        next_buy_index = buy_indices[buy_indices > sell_index]
        
        if not next_buy_index.empty:            
            start_year = int(sell_index+1)
            end_year = int(next_buy_index[-1])            
            year_last_purchase = int(df[df['year'] == sell_index]['year_last_purchase'].iloc[0])  # Fixed to sell action's year_last_purchase
            for year in range(start_year, end_year):
                rent_rows.append({'action': 'rent', 'year': year, 'year_last_purchase': year_last_purchase})
    
    if sell_indices.max() < 45:
        year_last_purchase = int(df[df['action'] == 'buy']['year'].max())   
        for year in range(sell_indices.max()+1, 46):            
            rent_rows.append({'action': 'rent', 'year': year, 'year_last_purchase': year_last_purchase})
    
    # Append the new rows and sort
    df = pd.concat([df, pd.DataFrame(rent_rows)], ignore_index=True).sort_values(by='year')

    return df

    

def fill_years_and_ffill(df):
# Creating a DataFrame with continuous years
    min_year = int(df['year'].min())
    max_year = int(df['year'].max())
    all_years = pd.DataFrame({'year': range(min_year, max_year + 1)})
    
    # Merging the new DataFrame with the original one
    df_filled = pd.merge(all_years, df, on='year', how='left')

    # Forward filling the values
    df_filled = df_filled.ffill()

    return df_filled


def finalize_df_preparation(transactions):
    
    df_ingesting_transactions = create_df_from_transactions(transactions)
    df_including_last_purchase_year = assign_last_purchase_year_and_rent_out(df_ingesting_transactions)
    df_including_rent_action = add_rent_actions(df_including_last_purchase_year)
    df_fill_years_and_ffill = fill_years_and_ffill(df_including_rent_action)

    df_prepared = df_fill_years_and_ffill
    

    return df_prepared
    