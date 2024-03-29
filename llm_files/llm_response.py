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
       
    # Add user input to conversation history
    
    #conversation.add_user_input(user_prompt)  # Context + user input

    # Generate output based on the current input and conversation context
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


        #Example Functions to be used
        
        #conversation.add_system_response(f"ROE Calculation: {roe_result}")
        
        return answer
    
    else:
        standard_answer = query_llm(user_prompt, model = model_general)
        return standard_answer


















# def generate_response(user_prompt):
#     global conversation_history

#     # Add the new user prompt to the conversation history
#     conversation_history.append({"role": "user", "content": user_prompt})
    

#     if needs_specialized_tool(user_prompt):
#         # Extract transactions and parameters
#         transactions, updated_parameters = extract_transactions_and_parameters(user_prompt)
#         transactions_json = json.dumps(transactions)
#         updated_parameters_json = json.dumps(updated_parameters)
#         conversation_history.append({"role": "system", "content": f"Calculated transactions: {transactions_json}, parameters: {updated_parameters_json}"})

#         tools = [llm_function_for_roe_calculation, llm_function_for_cash_flow_benefit]

#         # Initial response from the LLM
#         response = client.chat.completions.create(
#             model="ft:gpt-3.5-turbo-1106:de-martinos::8kBM9N6T",
#             messages=conversation_history,
#             tools=tools,
#             tool_choice="auto",
#         )

#         response_message = response.choices[0].message
    
#         tool_calls = response_message.tool_calls
        
#         # Step 2: check if the model wanted to call a function
#         if tool_calls:
#             # Step 3: call the function
#             # Note: the JSON response may not always be valid; be sure to handle errors
#             available_functions = {
#                 "calculate_roe_example": calculate_roe,
#                 "calculate_cashflow_benefit" : calculate_cashflow_benefit
#             }  # only one function in this example, but you can have multiple
#             conversation_history.append({"role": "assistant", "content": response_message.content})  # Assuming 'response_message' has a 'content' attribute
#   # extend conversation with assistant's reply
#             # Step 4: send the info for each function call and function response to the model
#             for tool_call in tool_calls:
#                 function_name = tool_call.function.name
#                 function_to_call = available_functions[function_name]
#                 function_args = json.loads(tool_call.function.arguments)
#                 function_response = function_to_call(
#                     transactions=function_args.get("transactions"),
#                     updated_parameters=function_args.get("updated_parameters"),
#                 )
#                 conversation_history.append(
#                     {
#                         "tool_call_id": tool_call.id,
#                         "role": "tool",
#                         "name": function_name,
#                         "content": function_response,
#                     }   
#                 )


#         # Process tool calls and append responses to conversation history
#         # ... (rest of the tool processing logic) ...

#         # Generate the second response based on the tool's output
#         second_response = client.chat.completions.create(
#             model="ft:gpt-3.5-turbo-1106:de-martinos::8kBM9N6T",
#             messages=conversation_history,
#         )

#         # Capture the final response content
#         final_response_content = second_response.choices[0].message.content
#         conversation_history.append({"role": "system", "content": final_response_content})
#         #print(conversation_history)
#         return final_response_content
#     else:
#         # Handle general LLM response for non-tool-related prompts
#         response = client.chat.completions.create(
#             model="gpt-3.5-turbo-1106",
#             messages=conversation_history,
#         )
#         general_response_content = response.choices[0].message.content
#         conversation_history.append({"role": "system", "content": general_response_content})
#         return general_response_content

# # Example usage
# response = generate_response("Calculate the roe if I buy a house in 1 year.")
# print(response)




# def generate_response(user_prompt):
    
#     transactions = extract_transactions(user_prompt)

#     # Convert transactions to JSON string for the OpenAI API
#     transactions_json = json.dumps(transactions)

#     # Step 1: send the conversation and available functions to the model
#     messages = [{"role": "user", "content": user_prompt},
#                 {"role": "system", "content": f"Calculated transactions: {transactions_json}"}
#     ]
#     print(user_prompt)
#     tools = [
#     {
#         "type": "function",
#         "function": {
#             "name": "calculate_roe_example",
#             "description": "Calculate the annualized ROE of the given transactions.",
#             "parameters": {
#                 "type": "object",
#                 "properties": {
#                     "transactions": {
#                         "type": "array",
#                         "description": "Array of transaction dictionaries.",
#                         "items": {
#                             "type": "object",
#                             "properties": {
#                                 "action": {"type": "string"},
#                                 "year": {"type": "number"}
#                             },
#                             "required": ["action", "year"]
#                         }
#                     },
#                     "horizon_year": {
#                         "type": "number",
#                         "description": "Investment horizon for the ROE calculation",
#                         "default": 10  # Default value if not specified
#                     }
#                 },
#                 "required": ["transactions"]
#             }
#         }
#     }
#     ]
#     response = client.chat.completions.create(
#         model="gpt-3.5-turbo-1106",
#         messages=messages,
#         tools=tools,
#         tool_choice="auto",  # auto is default, but we'll be explicit
#     )
    
#     response_message = response.choices[0].message
    
#     tool_calls = response_message.tool_calls
    
#     # Step 2: check if the model wanted to call a function
#     if tool_calls:
#         # Step 3: call the function
#         # Note: the JSON response may not always be valid; be sure to handle errors
#         available_functions = {
#             "calculate_roe_example": calculate_roe,
#             "calculate_cashflow_benefit" : calculate_cashflow_benefit
#         }  # only one function in this example, but you can have multiple
#         messages.append(response_message)  # extend conversation with assistant's reply
#         # Step 4: send the info for each function call and function response to the model
#         for tool_call in tool_calls:
#             function_name = tool_call.function.name
#             function_to_call = available_functions[function_name]
#             function_args = json.loads(tool_call.function.arguments)
#             function_response = function_to_call(
#                 transactions=function_args.get("transactions"),
#                 horizon_year=function_args.get("horizon_year"),
#             )
#             messages.append(
#                 {
#                     "tool_call_id": tool_call.id,
#                     "role": "tool",
#                     "name": function_name,
#                     "content": function_response,
#                 }   
#             )  # extend conversation with function response
#         second_response = client.chat.completions.create(
#             model="gpt-3.5-turbo-1106",
#             messages=messages,
#         )  # get a new response from the model where it can see the function response
#         return second_response.choices[0].message.content

