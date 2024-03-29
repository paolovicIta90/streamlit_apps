import os
import sys

# Get the directory of the current file
current_dir = os.path.dirname(os.path.abspath(__file__))

# Go one level up from the current directory
parent_dir = os.path.dirname(current_dir)

# Append the parent directory to sys.path
sys.path.append(parent_dir)

import streamlit as st
import importlib

from llm_files.llm_response import generate_response, initial_parameters



st.title("Real Estate assistant")


model_finetuned = 'ft:gpt-3.5-turbo-1106:de-martinos::8pGlpE1P'
model_general='gpt-4-turbo-preview'
updated_parameters_dict = initial_parameters



with st.sidebar.form("Inputs"):
        
    horizon_year = st.number_input('Horizon Year', value=7, format="%d")
    house_value_t0 = st.number_input('House Value at T0', value=500000, format="%d")
    house_value_increase = st.number_input('House Value Increase', value=0.025, format="%f")
    equity_contribution = st.number_input('Equity Contribution', value=0, format="%d")
    manteinance_cost = st.number_input('Maintenance Cost', value=1500, format="%d")
    mortgage_rate = st.number_input('Mortgage Rate', value=0.04, format="%f")
    service_cost =  st.number_input('Service Cost', value=180, format="%d")
    ground_lease = st.number_input('Ground Lease', value=0, format="%d")
    ground_lease_expiry = st.number_input('Ground Lease Expiry', value=1, format="%d")
    
    submit_form = st.form_submit_button(label='Update Parameters')

if submit_form:
    updated_parameters_dict['horizon_year'] = horizon_year
    updated_parameters_dict['house_value_t0'] = house_value_t0
    updated_parameters_dict['house_value_increase'] = house_value_increase
    updated_parameters_dict['equity_contribution'] = equity_contribution
    updated_parameters_dict['manteinance_cost'] = manteinance_cost
    updated_parameters_dict['mortgage_rate'] = mortgage_rate
    updated_parameters_dict['service_cost'] = service_cost
    updated_parameters_dict['ground_lease'] = ground_lease
    updated_parameters_dict['ground_lease_expiry'] = ground_lease_expiry
    

st.write(initial_parameters)
if st.button('Reload My Module'):
    importlib.reload(llm_response)

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if submit_form:
    assistant_answer = 'Parameters have been updated'
    st.session_state.messages.append({"role": "assistant", "content": assistant_answer})
    st.markdown(assistant_answer)

if prompt := st.chat_input("What is up?"):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        assistant_answer = generate_response(user_prompt = prompt, model_finetuned = model_finetuned, 
                                            model_general = model_general, updated_parameters_dict = updated_parameters_dict
                                            )       
        st.session_state.messages.append({"role": "assistant", "content": assistant_answer})
      
        st.markdown(assistant_answer)