import datetime
from datetime import date
import numpy as np
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns




import datetime as dt
from datetime import date

import numpy as np
import pandas as pd
import json

import os
import glob

import io
from functions_cashflow_dataset import *
from prep_functions import *
from functions_cashflow_for_transaction_action import *
from functions_cashflows_calculation import *
from parameters import *



Dict = dict
List = list
Any = any


def calculate_cashflow_benefit(transactions, updated_parameters_dict):
     
    processing_instance = processing_dataframe(**updated_parameters_dict)

    horizon_year = updated_parameters_dict['horizon_year']

    df = processing_transforming_df(transactions, processing_instance)
    
    df=df.set_index('year')    

    cash_flow_benefit = df.loc[:horizon_year]['final_cashflow'].sum()
    #json.dumps({"cash_flow_benefit": cash_flow_benefit})
    return cash_flow_benefit
    

def calculate_roe(transactions, updated_parameters_dict):
    

    processing_instance = processing_dataframe(**updated_parameters_dict)

    horizon_year = updated_parameters_dict['horizon_year']

    df = processing_transforming_df(transactions, processing_instance)

    df=df.set_index('year')
    df['actualized_final_cashflow'] = np.where(df['final_cashflow']>0,
                                                  df['discount_rate']/df.loc[horizon_year, 'discount_rate']*df['final_cashflow'],
                                                  df['discount_rate']*df['final_cashflow'])
    
    initial_investment = sum(x for x in df.loc[:horizon_year, 'actualized_final_cashflow'] if x < 0)
    net_investment_cash_return = sum(x for x in df.loc[:horizon_year, 'actualized_final_cashflow'] if x > 0)
    
    
    # Ensure initial_investment is not zero to avoid division by zero
    if initial_investment != 0:
        total_roe_pct = round(100 * ((net_investment_cash_return / -(initial_investment))**(1/horizon_year)) - 100,2)
    else:
        total_roe_pct = None  # or some default value, depending on your requirements

    return total_roe_pct 

def calculate_total_cashoutflow(transactions, updated_parameters_dict):

    processing_instance = processing_dataframe(**updated_parameters_dict)

    horizon_year = updated_parameters_dict['horizon_year']

    df = processing_transforming_df(transactions, processing_instance)
    
    df=df.set_index('year')    

    df['cash_outflow'] = np.where(df['final_cashflow'] <0,
                            df['final_cashflow'],
                            0)
    
    cash_outflow = df.loc[:horizon_year]['cash_outflow'].sum()    
    
    return cash_outflow

def calculate_annual_housing_cost(transactions, updated_parameters_dict):
    
    evaluation_year = updated_parameters_dict['horizon_year']
    processing_instance = processing_dataframe(**updated_parameters_dict)

    df = processing_transforming_df(transactions, processing_instance)
    
    df=df.set_index('year')

    monthly_housing_cost = round(df.loc[: evaluation_year, 'house_purchasing_cashflow'].mean()/12)    

    return monthly_housing_cost

def calculate_mortgage_payments_updated(transactions, updated_parameters_dict):
    
    evaluation_year = updated_parameters_dict['horizon_year']
    processing_instance = processing_dataframe(**updated_parameters_dict)

    df = processing_transforming_df(transactions, processing_instance)
    
    df=df.set_index('year')
    
    monthly_mortgage_payment = round(df.loc[: evaluation_year, 'mortgage_payments'].mean()/12)    

    return monthly_mortgage_payment

def calculate_equity_accumulation_update(transactions, updated_parameters_dict):
    
    evaluation_year = updated_parameters_dict['horizon_year']
    processing_instance = processing_dataframe(**updated_parameters_dict)

    df = processing_transforming_df(transactions, processing_instance)
    
    df=df.set_index('year')
    
    monthly_equity_accumulation = round(df.loc[: evaluation_year, 'equity_accumulation'].mean()/12)
    
    return monthly_equity_accumulation





