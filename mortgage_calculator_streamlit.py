
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

import os
import glob

import io



#@title BASIC FUNCTIONS



def calculate_monthly_mortgage_payment(loan_value, mortgage_rate, loan_term):
    monthly_rate = mortgage_rate / 12
    n_payments = loan_term * 12
    M = loan_value * (monthly_rate * (1 + monthly_rate) ** n_payments) / ((1 + monthly_rate) ** n_payments - 1)
    return round(M)

def average_monthly_interest(loan_value, mortgage_rate, loan_term, tax_shield, valuation_year):
    M = calculate_monthly_mortgage_payment(loan_value, mortgage_rate, loan_term)
    remaining_balance = loan_value
    total_interest = 0
    monthly_rate = mortgage_rate / 12
    for month in range(1, valuation_year * 12 + 1):
        interest_for_month = remaining_balance * monthly_rate
        principal_for_month = M - interest_for_month
        total_interest += interest_for_month
        remaining_balance -= principal_for_month
    total_interest_adjusted = total_interest * tax_shield
    return round(total_interest_adjusted / (12 * valuation_year))

def net_cash_flow_analysis(loan_value, mortgage_rate, loan_term, tax_shield,
                           tax_shield_interest, ground_lease_input,
                           rent_expense, rent_increase, service_charge,
                           energy_bills_rent, energy_bills_purchase,
                           valuation_year, maintenance_cost,
                           airbnb_net_income):

    monthly_mortgage = round(calculate_monthly_mortgage_payment(loan_value, mortgage_rate, loan_term) * tax_shield)
    monthly_interest = average_monthly_interest(loan_value, mortgage_rate, loan_term, tax_shield_interest, valuation_year)

    total_rent_expense = rent_expense * 12 * (1 - (1 + rent_increase) ** valuation_year) / (-rent_increase)
    monthly_rent_cash_flow = round(total_rent_expense / (12 * valuation_year) + energy_bills_rent)
    monthly_purchase_cash_flow = monthly_mortgage + maintenance_cost / 12 - airbnb_net_income / 12 + energy_bills_purchase + service_charge + ground_lease_input/12*tax_shield_interest
    monthly_interest_cash_flow = monthly_interest + maintenance_cost / 12 - airbnb_net_income / 12 + energy_bills_purchase + service_charge + ground_lease_input/12*tax_shield_interest

    return monthly_rent_cash_flow - monthly_purchase_cash_flow, monthly_rent_cash_flow - monthly_interest_cash_flow

def multiple_cash_flow_analysis(loan_value, mortgage_rate, loan_term, tax_shield,
                                tax_shield_interest, ground_lease_input,
                           rent_expense, rent_increase, service_charge,
                           energy_bills_rent, energy_bills_purchase,
                           valuation_year, maintenance_cost,
                           airbnb_net_income):

    monthly_mortgage = round(calculate_monthly_mortgage_payment(loan_value, mortgage_rate, loan_term) * tax_shield)
    monthly_interest = average_monthly_interest(loan_value, mortgage_rate, loan_term, tax_shield_interest, valuation_year)

    total_rent_expense = rent_expense * 12 * (1 - (1 + rent_increase) ** valuation_year) / (-rent_increase)
    monthly_rent_cash_flow = round(total_rent_expense / (12 * valuation_year) + energy_bills_rent)
    monthly_purchase_cash_flow = monthly_mortgage + maintenance_cost / 12 - airbnb_net_income / 12 + energy_bills_purchase + service_charge + ground_lease_input/12*tax_shield_interest
    monthly_interest_cash_flow = monthly_interest + maintenance_cost / 12 - airbnb_net_income / 12 + energy_bills_purchase + service_charge + ground_lease_input/12*tax_shield_interest

    return monthly_mortgage, monthly_interest, monthly_rent_cash_flow, maintenance_cost / 12, -airbnb_net_income / 12, service_charge, energy_bills_purchase, round(ground_lease_input/12*tax_shield_interest), (monthly_mortgage+maintenance_cost / 12 - airbnb_net_income / 12+energy_bills_purchase+service_charge+round(ground_lease_input/12*tax_shield_interest))

#def ground_lease_calculation(ground_lease_year_input, discount_rate_input, valutation_year_input)




















def cash_flow_simulation(valuation_year_input, house_value_t0, mortgage_rate_input,
                         loan_term_input, rent_amount_input, energy_bills_rent,
                         rent_increase_input, airbnb_net_yield, 
                         tax_shield_input,tax_shield_interest_input,
                         house_value_increase_input, manteinance_cost_input,
                         energy_bills_purchase_input, service_cost_input, ground_lease_input,
                         ground_lease_expiry, purchase_cost_net, property_tax_percentage, selling_cost_percentage,
                        discount_rate_input):
  
  mortgage_repayment_year=loan_term_input + valuation_year_input
  house_value = house_value_t0*(1+house_value_increase_input)**valuation_year_input
  house_terminal_discounted_value = round((house_value_t0*(1+house_value_increase_input)**46)/((1+discount_rate_input)**46))


  mortgage_payment = round(calculate_monthly_mortgage_payment(house_value, mortgage_rate_input, loan_term_input) * tax_shield_input)*12
  interest_payment = round(average_monthly_interest(house_value, mortgage_rate, loan_term, tax_shield_interest_input, valuation_year_input)*12)

  purchase_cost_future = round(purchase_cost_net*(1+house_value_increase_input/2)**valuation_year_input)
  property_tax= round(property_tax_percentage*house_value)

  year_values = [year for year in range(1,46)]
  energy_bills_year_values = [round((12*energy_bills_purchase_input)*(1+house_value_increase_input/2)**year) for year in range(1,46)]
  service_costs_year_values = [round((12*service_cost_input)*(1+house_value_increase_input/2)**year) for year in range(1,46)]
  maintenance_cost_values = [round(manteinance_cost_input*(1+house_value_increase_input)**year) for year in range(1,46)]
  
  rent_values = [round(12*rent_amount_input*(1+rent_increase_input)**year) for year in range(1,46)]
  energy_bills_rent_values = [round(12*energy_bills_rent*(1+house_value_increase_input/2)**year) for year in range (1,46)]
  ground_lease_values = [round(0) for year in range(1,ground_lease_expiry+1)]  + [round(ground_lease_input/12*tax_shield_interest_input) for year in range(ground_lease_expiry+1, 46)]
  purchase_cost_net_values = [purchase_cost_future for year in range(1,3)] + [purchase_cost_future + property_tax for year in range(3,46)]
  discount_factor_values = [1/(1+discount_rate_input)**year for year in range(1,46)]
  mortgage_payment_year_values = [mortgage_payment for year in range(1,46)]
  interest_payment_year_values = [interest_payment for year in range(1,46)]
  airbnb_income_values = [0 for year in range(1,valuation_year_input)] + [round((airbnb_net_yield*house_value)*(1+house_value_increase_input)**year) for year in range (valuation_year_input,46)]
   
  df_cash_flow=pd.DataFrame()

  df_cash_flow['year'] = year_values
  df_cash_flow['discount_factor_values'] = discount_factor_values
  df_cash_flow['energy_bills_year_values'] = energy_bills_year_values
  df_cash_flow['service_costs_year_values'] = service_costs_year_values
  df_cash_flow['maintenance_cost_values'] = maintenance_cost_values
  df_cash_flow['rent_values'] = rent_values
  df_cash_flow['energy_bills_rent_values'] = energy_bills_rent_values
  df_cash_flow['ground_lease_values'] = ground_lease_values
  df_cash_flow['purchase_cost_net_values'] = purchase_cost_net_values
  df_cash_flow['mortgage_payment_year_values'] = mortgage_payment_year_values
  df_cash_flow['interest_payment_year_values'] = interest_payment_year_values
  df_cash_flow['airbnb_income_values'] = airbnb_income_values

  col_list=['year', 'discount_factor_values']
  
  for col in df_cash_flow.columns[2:]:
    col_name = f"discounted_{col}"
    df_cash_flow[col_name] = round(df_cash_flow[col]*df_cash_flow['discount_factor_values'])
    col_list.append(col_name)

  df_cash_flow['discounted_equity_accumulation'] = df_cash_flow['discounted_mortgage_payment_year_values'] - df_cash_flow['discounted_interest_payment_year_values']

  df_cash_flow['effective_discounted_purchase_cost'] = np.where(df_cash_flow['year'] == valuation_year_input,
                                                                df_cash_flow['discounted_purchase_cost_net_values'],
                                                                0) 
  
  df_cash_flow['house_terminal_value'] = np.where(df_cash_flow['year'] < 45,
                                                        0,
                                                        house_terminal_discounted_value)
  
  df_cash_flow['total_renting_cashflow'] = df_cash_flow['discounted_rent_values'] + df_cash_flow['discounted_energy_bills_rent_values']
  df_cash_flow['total_purchasing_cashflow'] = df_cash_flow['discounted_mortgage_payment_year_values'] + df_cash_flow['discounted_energy_bills_year_values'] + df_cash_flow['discounted_service_costs_year_values'] + df_cash_flow['discounted_maintenance_cost_values'] + df_cash_flow['discounted_ground_lease_values'] + df_cash_flow['effective_discounted_purchase_cost'] - df_cash_flow['discounted_airbnb_income_values'] - df_cash_flow['house_terminal_value']
  
  df_cash_flow['mortgage_paid_cashflow'] = df_cash_flow['discounted_energy_bills_year_values'] + df_cash_flow['discounted_service_costs_year_values'] + df_cash_flow['discounted_maintenance_cost_values'] + df_cash_flow['discounted_ground_lease_values'] + df_cash_flow['effective_discounted_purchase_cost'] - df_cash_flow['discounted_airbnb_income_values'] - df_cash_flow['house_terminal_value']
  
  
  
  df_cash_flow['effective_discounted_housing_cost'] = np.where(df_cash_flow['year'] < valuation_year_input,
                                                                df_cash_flow['total_renting_cashflow'],
                                                                np.where(df_cash_flow['year'] < mortgage_repayment_year,
                                                                df_cash_flow['total_purchasing_cashflow'],
                                                                df_cash_flow['mortgage_paid_cashflow']))
  
  df_cash_flow['net_benefit_over_rent'] =df_cash_flow['total_renting_cashflow'] - df_cash_flow['effective_discounted_housing_cost']



  col_list=col_list + ['discounted_equity_accumulation','house_terminal_value', 'effective_discounted_purchase_cost', 'total_renting_cashflow', 'total_purchasing_cashflow', 'effective_discounted_housing_cost', 'net_benefit_over_rent']

  






  

  
    
  
  
  
  
  return df_cash_flow[col_list]


#################### THE APP ###################################################################################

st.title('HOUSE PURCHASE EVALUATION')


  






# Creating the sidebar form called "Inputs Selection"
with st.sidebar.form(key='inputs_form'):
    st.write("Inputs Selection")

    # House-related variables
    house_value_t0 = st.number_input('House Value at Time 0', value=425000)
    equity_portion = st.number_input('Equity Portion', value=0)
    mortgage_rate = st.number_input('Mortgage Rate', min_value=0.0, max_value=1.0, value=0.051)
    loan_term = st.number_input('Loan Term (years)', value=30, min_value=0, max_value=100, format='%d')

    # Tax-related variables
    tax_shield = st.number_input('Tax Shield', min_value=0.0, max_value=1.0, value=0.72)
    tax_shield_interest = st.number_input('Tax Shield Interest', min_value=0.0, max_value=1.0, value=0.63)

    # Purchase-related variables
    house_purchase_year = st.number_input('House Purchase Year', value=1, format='%d')
    purchase_cost = st.number_input('Purchase Cost', value=10000)
    property_tax_percentage = st.number_input('Property Tax Percentage', min_value=0.0, max_value=1.0, value=0.02)
    selling_cost_percentage = st.number_input('Selling Cost Percentage', min_value=0.0, max_value=1.0, value=0.0115)

    # Rent and related costs
    rent_expense = st.number_input('Rent Expense', value=1386)
    rent_increase = st.number_input('Rent Increase', min_value=0.0, max_value=1.0, value=0.02)
    service_charge = st.number_input('Service Charge', value=150)
    energy_bills_rent = st.number_input('Energy Bills (Rent)', value=120)
    energy_bills_purchase = st.number_input('Energy Bills (Purchase)', value=200)
    manteinance_cost = st.number_input('Maintenance Cost', value=2200)

    # Airbnb-related variables
    airbnb_yield_year = st.number_input('Airbnb Yield per Year', min_value=0.0, max_value=1.0, value=0.009)
    airbnb_net_income_pct = st.number_input('Airbnb Net Income Percentage', min_value=0.0, max_value=1.0, value=0.2)
    airbnb_net_yield = airbnb_yield_year*airbnb_net_income_pct

    # Ground lease variables
    ground_lease = st.number_input('Ground Lease', value=0)
    ground_lease_expiry = st.number_input('Ground Lease Expiry (years)', value=45)

    # Other variables
    house_nominal_price_increase = st.number_input('House Nominal Price Increase', value=0.03)
    discount_cashflow_rate = st.number_input('Discount Cashflow Rate', min_value=0.0, max_value=1.0, value=0.04)

    #Inputs for scenario analysis
    #Scenario_one
    purchase_year_first_house_scenario_one = st.number_input('For the first Scenario what is the Purchase year of the first appartment', min_value=1, value=1)
    purchase_year_second_house_scenario_one = st.number_input('For the first Scenario what is the Purchase year of the first appartment', min_value=3, value=7)
    keep_proceeding_first_sale_scenario_one = st.selectbox('Would you keep the proceeds of the sale in the first scenario?', ['yes', 'no'], index=0)
    purchase_year_first_house_scenario_two = st.number_input('For the second Scenario what is the Purchase year of the first appartment', min_value=1, value=7)
    purchase_year_second_house_scenario_two = st.number_input('For the second Scenario what is the Purchase year of the first appartment', min_value=3, value=45)
    keep_proceeding_first_sale_scenario_two = st.selectbox('Would you keep the proceeds of the sale in the second scenario?', ['yes', 'no'], index=1)







    # Submit button
    submitted = st.form_submit_button("Confirm Input Selection")

if submitted:
    st.write("Inputs have been confirmed!")






df_results = cash_flow_simulation(house_purchase_year, house_value_t0, mortgage_rate,
                         loan_term, rent_expense, energy_bills_rent,
                         rent_increase, airbnb_net_yield, 
                         tax_shield,tax_shield_interest,
                         house_nominal_price_increase, manteinance_cost,
                         energy_bills_purchase, service_charge, ground_lease,
                         ground_lease_expiry, purchase_cost, property_tax_percentage,selling_cost_percentage,
                        discount_cashflow_rate)


    
def compare_purchase_years(house_purchase_year_input, investment_horizon, sell_year_first_house, keep_proceeding_first_sale):

    df_first_house_purchase = cash_flow_simulation(house_purchase_year_input, house_value_t0, mortgage_rate,
                        loan_term, rent_expense, energy_bills_rent,
                        rent_increase, airbnb_net_yield, 
                        tax_shield,tax_shield_interest,
                        house_nominal_price_increase, manteinance_cost,
                        energy_bills_purchase, service_charge, ground_lease,
                        ground_lease_expiry, purchase_cost, property_tax_percentage, selling_cost_percentage,
                    discount_cashflow_rate)
    
    df_second_house_purchase = cash_flow_simulation(sell_year_first_house, house_value_t0, mortgage_rate,
                        loan_term, rent_expense, energy_bills_rent,
                        rent_increase, airbnb_net_yield, 
                        tax_shield,tax_shield_interest,
                        house_nominal_price_increase, manteinance_cost,
                        energy_bills_purchase, service_charge, ground_lease,
                        ground_lease_expiry, purchase_cost, property_tax_percentage, selling_cost_percentage,
                    discount_cashflow_rate)
    
       

    
        
    discount_factor = 1/((1+discount_cashflow_rate)**sell_year_first_house)

    house_value = round(house_value_t0*(1+house_nominal_price_increase)**sell_year_first_house)

    discounted_house_capital_gain = (house_value - house_value_t0)*discount_factor

    equity_accumulated = df_first_house_purchase['discounted_equity_accumulation'][:sell_year_first_house].sum()

    

    property_tax= round(property_tax_percentage*house_value)

    selling_cost = round(house_value*selling_cost_percentage)

    purchase_cost_future = round(purchase_cost*(1+house_nominal_price_increase/2)**sell_year_first_house)

    

    

    df_sales_proceeds = pd.DataFrame()
    df_sales_proceeds['first_house_net_beneift_over_rent'] = df_first_house_purchase['net_benefit_over_rent']
    df_sales_proceeds['year'] = [year for year in range(1,46)]
    df_sales_proceeds['net_beneift_over_rent_before_sale'] = np.where(df_sales_proceeds['year'] < sell_year_first_house,
                                                       df_sales_proceeds['first_house_net_beneift_over_rent'],
                                                       0)


    

    if sell_year_first_house==45:

        df_sales_proceeds['cost_sell_first_house'] = np.where(df_sales_proceeds['year'] == sell_year_first_house,
                                                              round(selling_cost*discount_factor),
                                                              0)
        
        
        
    else:
        df_sales_proceeds['cost_sell_first_house'] = np.where(df_sales_proceeds['year'] == sell_year_first_house,
                                                             round((selling_cost)*discount_factor),
                                                              0)
       


    if (keep_proceeding_first_sale == 'yes') & (sell_year_first_house < 45):
        df=df_second_house_purchase
        df_sales_proceeds['cash_proceed_sale'] =  np.where(df_sales_proceeds['year'] ==sell_year_first_house,
                                                            discounted_house_capital_gain + equity_accumulated,
                                                            0) 

        df_sales_proceeds['net_beneift_over_rent_before_sale'] = np.where(df_sales_proceeds['year'] < sell_year_first_house,
                                                       df_sales_proceeds['first_house_net_beneift_over_rent'],
                                                       0)        

        
    else:
        df=df_first_house_purchase
                     
        df_sales_proceeds['cash_proceed_sale'] = [0 for year in range(1,46)]

        df_sales_proceeds['net_beneift_over_rent_before_sale'] = [0 for year in range(1,46)]
    
                                            
                                            
                                            
    
    
    
    
    return round(df['net_benefit_over_rent'][:investment_horizon].sum()/1000 - df_sales_proceeds['cost_sell_first_house'][:investment_horizon].sum()/1000 +df_sales_proceeds['cash_proceed_sale'][:investment_horizon].sum()/1000 +  df_sales_proceeds['net_beneift_over_rent_before_sale'][:investment_horizon].sum()/1000,2)

def generate_comparative_benefit_over_years_purchase (investment_horizon, sell_year_first_house, keep_proceeding_first_sale):
    df=pd.DataFrame()    

    df['purchase_year'] =  [year for year in range(1,16)] 

    df['net_benefit_over_rent(000s)'] = df['purchase_year'].apply(lambda x: compare_purchase_years(x, investment_horizon, sell_year_first_house, keep_proceeding_first_sale))

    return df

def generate_comparative_benefit_over_years_horizon (house_purchase_year_input, sell_year_first_house, keep_proceeding_first_sale):
    df=pd.DataFrame()    

    df['investment_horizon'] =  [year for year in range(1,46)] 

    df['net_benefit_over_rent(000s)'] = df['investment_horizon'].apply(lambda x: compare_purchase_years(house_purchase_year_input,x, sell_year_first_house,  keep_proceeding_first_sale))

    return df


# print(compare_purchase_years(5, 5,45))

# print(compare_purchase_years(1, 5,5))





scenario_1 = generate_comparative_benefit_over_years_horizon(purchase_year_first_house_scenario_one,purchase_year_second_house_scenario_one, keep_proceeding_first_sale_scenario_one)
scenario_2 = generate_comparative_benefit_over_years_horizon(purchase_year_first_house_scenario_two,purchase_year_second_house_scenario_two, keep_proceeding_first_sale_scenario_one)

scenario_1['benefit_buy&sell_vs_wait_buy'] = scenario_1['net_benefit_over_rent(000s)'] - scenario_2['net_benefit_over_rent(000s)']

scenario_one_analysis_recap=f"Overall Discounted Cash Flow Benefit of buying (after {purchase_year_first_house_scenario_one} years) and selling (after {purchase_year_second_house_scenario_one} years) the first house and then buy again vs rent all your life"

scenario_two_analysis_recap=f"Overall Discounted Cash Flow Benefit of buying (after {purchase_year_first_house_scenario_one} years) and selling (after {purchase_year_second_house_scenario_two} years) the first house and then buy again vs buy directly after {purchase_year_first_house_scenario_two} years"



#compare_purchase_years(house_purchase_year_input = 1, investment_horizon = 45, sell_year_first_house = 5, keep_proceeding_first_sale = 'yes') - compare_purchase_years(house_purchase_year_input = 5, investment_horizon = 45, sell_year_first_house = 45, keep_proceeding_first_sale = 'no')


st.write('Static evaluation: benefit over rent of a single purchase', df_results['net_benefit_over_rent'].sum())

st.write(scenario_one_analysis_recap, scenario_1['net_benefit_over_rent(000s)'][-1:])
st.write(scenario_two_analysis_recap, scenario_1['benefit_buy&sell_vs_wait_buy'][-1:])

fig, ax1 = plt.subplots(figsize=(12, 7))

color = 'tab:blue'
ax1.set_xlabel('Investment Horizon')
ax1.set_ylabel('Benefit Buy & Sell vs Always renting(000s)', color=color)
line1, = ax1.plot(scenario_1['investment_horizon'], scenario_1['net_benefit_over_rent(000s)'], marker='o', color=color)
ax1.tick_params(axis='y', labelcolor=color)

ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis
color = 'tab:red'
ax2.set_ylabel('Benefit Buy & Sell vs Waiting to buy (000s)', color=color)
line2, = ax2.plot(scenario_1['investment_horizon'], scenario_1['benefit_buy&sell_vs_wait_buy'], marker='o', color=color)
ax2.tick_params(axis='y', labelcolor=color)

# Place legend at the upper left without cutting into the chart
lines = [line1, line2]
labels = [l.get_label() for l in lines]
ax1.legend(lines, labels, loc='upper left')

fig.suptitle('Investment Horizon Benefits Analysis', x=0.5, y=1.02)

# Display the plot in Streamlit
st.pyplot(fig)


























