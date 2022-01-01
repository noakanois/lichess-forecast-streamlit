import streamlit as st
import pandas as pd
import berserk
import numpy as np
import matplotlib.pyplot as plt
import datetime as dt
import api_key
import plotly.express as px

token1 = api_key.token
session = berserk.TokenSession(token1)
client = berserk.Client(session=session)


game_modes = ("Bullet", "Blitz", "Rapid", "Classical")
selected_game_mode = st.selectbox("Choose a game mode", game_modes)

game_mode_dict = {"Bullet":0, "Blitz":1, "Rapid":2, "Classical":3}

@st.cache
def load_data(mode):
    
    stats = client.users.get_rating_history("noakanoi")[game_mode_dict.get(mode)]["points"]
    rating = [x[3] for x in stats]
    date = [dt.date(x[0],x[1]+1,x[2]) for x in stats]
    return pd.DataFrame(rating, date)


data = load_data(selected_game_mode)


def plot_data():
    fig = px.line(data, title=f"{selected_game_mode} Rating")
    fig.layout.update(title_text=f"{selected_game_mode} Rating", xaxis_rangeslider_visible=True)
    st.plotly_chart(fig)
    
plot_data()
    

#x = st.slider('Select the year range',bullet_date[0], bullet_date[-1], (bullet_date[0], bullet_date[-1]))
#st.line_chart(bullet_data)
