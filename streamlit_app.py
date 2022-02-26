import streamlit as st
import pandas as pd
import berserk
import numpy as np
import matplotlib.pyplot as plt
import datetime as dt
import plotly.express as px
from fbprophet import Prophet
from fbprophet.plot import plot_plotly
from plotly import graph_objs as go
import sys

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
        st.write(fig2)
