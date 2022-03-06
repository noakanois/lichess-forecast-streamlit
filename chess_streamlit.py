""""import streamlit as st
import pandas as pd
import berserk
import numpy as np
import matplotlib.pyplot as plt
import datetime as dt
import api_key
import plotly.express as px
from fbprophet import Prophet
from fbprophet.plot import plot_plotly
from plotly import graph_objs as go
import sys

token1 = api_key.token
session = berserk.TokenSession(token1)
client = berserk.Client(session=session)

st.title("Lichess Ratings and Forecaster")

username = st.text_input("Put in a username", "noakanoi")

st.header(f"{username} Lichess Ratings")
game_modes = ("Bullet", "Blitz", "Rapid", "Classical")
selected_game_mode = st.selectbox("Choose a game mode", game_modes)
game_mode_dict = {"Bullet":0, "Blitz":1, "Rapid":2, "Classical":3}

@st.cache
def load_data(mode):   
    stats = client.users.get_rating_history(username)[game_mode_dict.get(mode)]["points"]
    rating = [x[3] for x in stats]
    date = [dt.date(x[0],x[1]+1,x[2]) for x in stats]
    data = {"ds": date, "y": rating, "date": date}
    data= pd.DataFrame(data)
    data = data.set_index("date")
    return data

data = load_data(selected_game_mode)
   
if data.empty:
    st.write(f"There doesn't seem to be any data for {username} for the gamemode {selected_game_mode}")
    st.write("Please try a different username or gamemode")
    
if not data.empty:
    fig = px.line(data["y"], labels={"value": "Rating","date": "Date", "variable":"Blitz"},title=f"{selected_game_mode} Rating")
    fig.layout.update(title_text=f"{selected_game_mode} Rating", xaxis_rangeslider_visible=True)
    st.plotly_chart(fig)    


if not data.empty:
    m = Prophet()
    m.fit(data)

    

    
if not data.empty:
    range = (50, 100, 365, 1000)
    selected_range = st.selectbox("Choose a timeframe for the forecast", range, 2)

    future = m.make_future_dataframe(periods=selected_range)
    forecast = m.predict(future)

    st.subheader(f'Rating {username} with forecast for {selected_range} days')
    fig1 = plot_plotly(m, forecast)
    st.plotly_chart(fig1)
    
    trend = st.button("Show extra information about the forecast")
    if trend:
        st.subheader("Forecast components")
        fig2 = m.plot_components(forecast)
        st.write(fig2)"""
        
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px
import sqlite3 as sql

game_mode = ["li_bullet", "li_blitz", "li_rapid", "ch_bullet", "ch_blitz", "ch_rapid"]

dict_game = {x:pd.read_csv(f"{x}_predict.csv") for x in game_mode}

st.title("Elo Converter / Chesscom <-> Lichess")

x = st.text_input("Put in the rating you want to convert", 1500)

head = ["ch_bullet", "ch_blitz", "ch_rapid", "li_bullet", "li_blitz", "li_rapid"]
dict = {"ch_bullet":"Chesscom Bullet", "ch_blitz":"Chesscom Blitz", "ch_rapid":"Chesscom Rapid", "li_bullet":"Lichess Bullet", "li_blitz":"Lichess Blitz", "li_rapid":"Lichess Rapid"}

inv = {v: k for k, v in dict.items()}

selected_game_mode1 = st.selectbox("Choose the rating you want to convert from", dict.values(), 1)
selected_game_mode2 = st.selectbox("Choose the rating you want to convert to", dict.values(), 4)

selected_game_mode_1 = inv[selected_game_mode1]
selected_game_mode_2 = inv[selected_game_mode2]

df = dict_game[selected_game_mode_1][[selected_game_mode_1, f"predicted_{selected_game_mode_2}"]]
data = df.at[int(x)-700, f"predicted_{selected_game_mode_2}"]


st.header(f"{dict[selected_game_mode_1]}: {x}")
st.header(f"{dict[selected_game_mode_2]}: {int(data)} predicted")

x = df[selected_game_mode_1][::30]
y = df[f"predicted_{selected_game_mode_2}"][::30]

fig = px.scatter(x = x, y = y, title= "Rating")
fig.update_xaxes(range=[750, 2700])
fig.update_yaxes(range=[750, 2700])
fig.layout.update(title_text="Rating")
st.plotly_chart(fig) 