from functions_cashflow_dataset import *




def calculate_sales_value(df,year):
    regular_house_purchasing_cashflow = df.loc[year, 'house_purchasing_cashflow']
    house_value = df.loc[year, 'house_value_over_years']
    house_purchase_price = df.loc[df.loc[year, 'year_last_purchase'], 'house_value_over_years']
    total_equity_accumulated = df.loc[df.loc[year, 'year_last_purchase']:year+1,'equity_accumulation'].sum()
    selling_costs = df.loc[year, 'selling_costs']
    
    sales_value = -regular_house_purchasing_cashflow + house_value - house_purchase_price + total_equity_accumulated - selling_costs
    
    return sales_value



def cashflow_attribution(row, df):
    
    cashflow_attribution_dict = {
        'buy': lambda df, year: -df.loc[year, 'house_purchasing_cashflow'] + df.loc[year, 'renting_cashflow'],
        'sell': lambda df, year: calculate_sales_value(df, year) + df.loc[year, 'renting_cashflow'],
        'rent_out': lambda df, year: df.loc[year, 'cash_flow_renting_out'],
        'stop_rent_out': lambda df, year: -df.loc[year, 'house_purchasing_cashflow'] + df.loc[year, 'renting_cashflow'],  # Same as 'buy'
        'rent': lambda df, year: 0
    }
    action = row['action']
    year = row.name  # Assuming the index of df is 'year'
    if action in cashflow_attribution_dict:
        return cashflow_attribution_dict[action](df, year)
    return None

def apply_cashflow_attribution(df):
    df=df.set_index('year')
    # Applying the cashflow_attribution function row-wise
    df['final_cashflow'] = df.apply(lambda row: cashflow_attribution(row, df), axis=1)
    return df.reset_index()



def processing_transforming_df(transactions, processing_instance):
    
    df_prepared = finalize_df_preparation(transactions)
    

# Now call the calculate_processed_df method on the processing_instance
    df_processed = processing_instance.calculate_processed_df(df_prepared)
    df_cashflow_attributed = apply_cashflow_attribution(df_processed)
    

    return df_cashflow_attributed