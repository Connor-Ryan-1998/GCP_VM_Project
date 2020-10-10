# Module Imports
from flask import Flask, session, copy_current_request_context, request, Flask, jsonify, make_response, redirect
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
import dash_html_components as html
import dash_core_components as dcc
import flask_sqlalchemy
import plotly.express as px
import dash
import flask
import os
import sys
import yfinance as yf
from pandas_datareader import data as pdr

external_stylesheets = [dbc.themes.BOOTSTRAP]

server = flask.Flask(__name__)
server.config['SECRET_KEY'] = os.urandom(24)
yf.pdr_override()



app = dash.Dash(
    server=server, external_stylesheets=external_stylesheets, url_base_pathname='/')

engine = create_engine('postgresql+psycopg2://postgres:password@localhost/postgres')

data = ""
with engine.connect() as con:
    result = con.execute("SELECT * FROM information_schema.tables")
    for row in result:
        data = data +row 
df = pdr.get_data_yahoo("SPY", start="2017-01-01", end="2017-04-30")
fig = px.scatter(df, x=df.index, y='Close')
app.layout = html.Div(children=[
    html.H4(children='SPY Close values for 2017'),
    html.Div(
        dcc.Graph(figure=fig),
        html.Div(str(data))),
])
