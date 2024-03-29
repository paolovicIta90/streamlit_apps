import datetime
from datetime import date
import numpy as np
import pandas as pd
import re
import os
import json
from functions_cashflows_calculation import *
from prep_functions import *
from openai import OpenAI
from functions_cashflow_dataset import *

initial_parameters = {
    "purchase_year": 1,
    "horizon_year" : 10,
    "house_value_t0": 385000,
    "equity_contribution": 0,
    "mortgage_rate": 0.045,
    "loan_term": 30,
    "rent_amount": 1386,
    "energy_bills_rent": 120,
    "rent_increase": 0.03,
    "airbnb_net_yield": 0.001,
    "tax_shield": 0.72,
    "tax_shield_interest": 0.63,
    "house_value_increase": 0.02,
    "manteinance_cost": 2200,
    "energy_bills_purchase": 200,
    "service_cost": 150,
    "ground_lease": 0,
    "ground_lease_expiry": 30,
    "purchase_cost_net": 8000,
    "property_tax_percentage": 0.02,
    "selling_cost_percentage": 0.02,
    "discount_rate": 0.04,
    "rent_out_gross_income": 1600,
    "rent_out_operating_expense": 0.25,
    "months_no_rent": 24,
    "rent_out_income_tax_rate": 0.37
}

parameters_list = list(initial_parameters.keys())


purchase_year = 1
horizon_year = 10
house_value_t0 = 385000
equity_contribution = 0
mortgage_rate = 0.045
loan_term = 30 
rent_amount= 1386 
energy_bills_rent = 120
rent_increase = 0.03
airbnb_net_yield = 0.001
tax_shield = 0.72
tax_shield_interest = 0.63
house_value_increase = 0.02
manteinance_cost = 2200
energy_bills_purchase = 200
service_cost = 150
ground_lease = 0
ground_lease_expiry = 30
purchase_cost_net = 8000
property_tax_percentage = 0.02
selling_cost_percentage = 0.02
discount_rate = 0.04
 
rent_out_gross_income = 1600
rent_out_operating_expense = 0.25
months_no_rent = 24
rent_out_income_tax_rate = 0.37

parameter_ingestion_class_instance = CashFlowSimulator(purchase_year, horizon_year, house_value_t0, equity_contribution, mortgage_rate, loan_term, 
                 rent_amount, energy_bills_rent, rent_increase, airbnb_net_yield, 
                 tax_shield, tax_shield_interest, house_value_increase, 
                 manteinance_cost, energy_bills_purchase, service_cost, 
                 ground_lease, ground_lease_expiry, purchase_cost_net, 
                 property_tax_percentage, selling_cost_percentage, discount_rate,
                 rent_out_gross_income, rent_out_operating_expense, months_no_rent,
                 rent_out_income_tax_rate)

# Now create an instance of processing_dataframe
processing_instance = processing_dataframe(purchase_year,horizon_year, house_value_t0, equity_contribution, mortgage_rate, loan_term, 
                 rent_amount, energy_bills_rent, rent_increase, airbnb_net_yield, 
                 tax_shield, tax_shield_interest, house_value_increase, 
                 manteinance_cost, energy_bills_purchase, service_cost, 
                 ground_lease, ground_lease_expiry, purchase_cost_net, 
                 property_tax_percentage, selling_cost_percentage, discount_rate,
                 rent_out_gross_income, rent_out_operating_expense, months_no_rent,
                 rent_out_income_tax_rate)