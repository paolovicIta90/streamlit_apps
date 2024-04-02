import os
import sys

# Get the directory of the current file
current_dir = os.path.dirname(os.path.abspath(__file__))

# Go one level up from the current directory
parent_dir = os.path.dirname(current_dir)

# Append the parent directory to sys.path
sys.path.append(parent_dir)

from llm_files.llm_settings import *
from llm_files.tools_for_llm import *
from investment_analysis import *

state = {
    "transactions": [],
    }

def generate_response(user_prompt, model_finetuned, model_general, updated_parameters_dict):
       
    tool_to_be_used = assess_if_tool_is_needed(user_prompt=user_prompt, model = model_general)

    print(tool_to_be_used)
    if tool_to_be_used:
        # Process output to extract transactions and parameters
        transactions = extract_transactions_and_parameters(user_prompt, model = model_finetuned)        
        
        # Check if transactions are empty and use the last state if so
        if not transactions:
            transactions = [state['transactions'][-1]] if state['transactions'] else []

        # Update state with new transactions and parameters, if provided
        if transactions:
            state["transactions"] = transactions

        total_housing_cost = calculate_annual_housing_cost(state['transactions'], updated_parameters_dict)
        equity_accumulation_value = calculate_equity_accumulation_update(state['transactions'], updated_parameters_dict)
        real_cost_owing_house = total_housing_cost - equity_accumulation_value
 
        answer = f"""The ROE of the real estate investment is {calculate_roe(state['transactions'], updated_parameters_dict)} 
                   The Cashflow Benefit is {calculate_cashflow_benefit(state['transactions'], updated_parameters_dict)}
                   The total cash outflow is {calculate_total_cashoutflow(state['transactions'], updated_parameters_dict)}
                   The average total cost of owing a house during the first purchase is {calculate_annual_housing_cost(state['transactions'], updated_parameters_dict)}
                   The average net mortgage payment is {calculate_mortgage_payments_updated(state['transactions'], updated_parameters_dict)}
                   The average real cost (money wasted like rent) of owning a house is {real_cost_owing_house}
                   The average equity accumulation throughout the investment horizon {calculate_equity_accumulation_update(state['transactions'], updated_parameters_dict)}
                   """   
        return answer
        
    else:
        standard_answer = query_llm(user_prompt, model = model_general)
        return standard_answer
