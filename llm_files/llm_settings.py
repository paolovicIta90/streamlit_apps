import datetime
from datetime import date
import numpy as np
import pandas as pd
import re
import os
import json
from openai import OpenAI
import ast

os.environ["OPENAI_API_KEY"] = "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"
conversation_history=[]

client = OpenAI()

def query_llm(prompt, model):
    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        temperature=0,
        max_tokens=150,  # Adjust as necessary
        top_p=0,
        frequency_penalty=0,
        presence_penalty=0
    )
    return response.choices[0].message.content

def assess_if_tool_is_needed(user_prompt, model):

    adjusted_user_promt = f"""Given the user's request: '{user_prompt}', does it imply real estate transactions or discuss relevant parameters or tools related to real estate investment analysis? Answer with 'True' or 'False' only.
                            If in the user's request there is a reference to assuming the same transactions as before, answer with 'True'"""
    llm_answer = query_llm(adjusted_user_promt, model = model)
    llm_answer_bolean = ast.literal_eval(llm_answer)
    return llm_answer_bolean

def extract_transactions_and_parameters(user_prompt, model):

    adjusted_prompt = f"""Please convert the following user request: {user_prompt} 
    into a structured format of transactions (list of dictionary), a dictionary with parameters and a dictionary with the functions to be used. 
    The dictionaries making up the list transactions should have the following structure 'action':action, 'year':year. 
    Every action should be one word, use _ to combine rent and out. 
    The parameters dictionary should have the following structure: parameter:value
    The function dictionary the following structure: function:function, output_text:output_text
    """
    
    llm_output = query_llm(adjusted_prompt, model)    
    llm_output_parts = llm_output.split('\n') 
    print(llm_output_parts)
    transactions_str = llm_output_parts[0].split(':', 1)[1].strip()
    transactions = ast.literal_eval(transactions_str)
    if transactions[-1]['action'] in ('buy', 'rent_out'):
        transactions.append({'action':'sell', 'year':45})

    return transactions

def create_updated_parameters_dict(updated_parameters, initial_parameters_dict):

    initial_parameters_dict = initial_parameters_dict.copy()
    if updated_parameters == {}:
        return initial_parameters_dict
    else:
        for parameter_name, new_parameters_value in updated_parameters.items():
            if parameter_name in initial_parameters_dict:
                initial_parameters_dict[parameter_name] = new_parameters_value
            else:
                # Handle unknown parameter or log a warning
                print(f"Warning: Unknown parameter '{parameter_name}'")
    
        updated_parameters_dict=initial_parameters_dict

    
        return updated_parameters_dict


    

    
