
import streamlit as st
st.title("Session state basics")
"st.session_state_object:", st.session_state
number = st.slider("A Number", 1, 10, key = 'slider')

st.write(st.session_state)

col1, buff, col2 = st.beta_columns([1,0.5,3])
option_names = ['a', 'b', 'c']

next=st.button('Next option')

if next:
    if st.session_state['radio_option'] == 'a':
        st.session_state['radio_option'] = 'b'
    elif st.session_state['radio_option'] == 'b':
        st.session_state['radio_option'] = 'c'
    else:
        st.session_state['radio_option'] = 'a'



