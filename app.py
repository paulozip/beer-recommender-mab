import json

import plotly.graph_objects as go
import requests
import streamlit as st

import helpers.SessionState as SessionState
from helpers.experiment_chart import (cumulative_exploration_plot,
                                      cumulative_reward_plot, show_best_arm)

BANDIT_ENDPOINT = 'http://0.0.0.0:8000/{}'

st.markdown("<h1 style='text-align: center'>🍺 Beer recommender 🍺</h1>", unsafe_allow_html=True)
st.markdown("<h4 style='text-align: center'>Can we find THE BEST BEER to recommend to people WE DON'T KNOW?</h4>", unsafe_allow_html=True)
st.markdown('\n\n')

arm = requests.request('POST', BANDIT_ENDPOINT.format('pull')).json()

st.markdown("<img style='display: block; margin-left: auto; margin-right: auto; width: 50%;' src=\"{}\" width=200px>".format(arm['brand_image'][str(arm['arm'])]), unsafe_allow_html=True)
st.markdown("<h4 style='text-align: center;'>{}</h4>".format(arm['brand']), unsafe_allow_html=True)

container = st.beta_container()
container.markdown("<h3 style='text-align: center'>Did you like this recommendation?</h3>", unsafe_allow_html=True)
#st.markdown(arm)

session_state = SessionState.get(arm=arm['arm']) 

col1, col2, col3, col4, col5 = container.beta_columns(5)

# If the user click on the like button
with col3:
    bt_thumbs_up = st.button('👍')
    if bt_thumbs_up:
        reward_payload = { 'arm': session_state.arm, 'reward': 1.0 }
        reward_response = requests.request('POST', BANDIT_ENDPOINT.format('reward'), data=json.dumps(reward_payload))
        session_state.arm = arm['arm']

# If the user click on the dislike button
with col4:
    bt_thumbs_down = st.button('👎')
    if bt_thumbs_down:
        reward_payload = { 'arm': session_state.arm, 'reward': -1.0 }
        reward_response = requests.request('POST', BANDIT_ENDPOINT.format('reward'), data=json.dumps(reward_payload))
        session_state.arm = arm['arm']

# Plotly Expander
expander = st.beta_expander('Click here for some nice charts')
with expander:
    arms_rewards = requests.request('GET', BANDIT_ENDPOINT.format('all_rewards')).json()
    
    # Showing optimal arm
    st.markdown("<h3 style='text-align: center'>The optimal beer is: " + show_best_arm(arms_rewards) + "</h3>", unsafe_allow_html=True)

    # Show cumulative exploration arm
    st.plotly_chart(cumulative_exploration_plot(arms_rewards))
    st.plotly_chart(cumulative_reward_plot(arms_rewards))

st.markdown("<h5 style='text-align: center;'>Made by <a href=\"https://www.paulovasconcellos.com.br\">Paulo Vasconcellos</a> with ❤️</h5>", unsafe_allow_html=True)
