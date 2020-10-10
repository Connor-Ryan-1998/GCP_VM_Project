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

class Config(object):
    """Base Configuration"""
    try:
        user = os.environ["POSTGRES_USER"]
        password = os.environ["POSTGRES_PASSWORD"]
        hostname = os.environ["POSTGRES_HOSTNAME"]
        database = os.environ["APPLICATION_DB"]
        SQLALCHEMY_DATABASE_URI = (
            f"postgresql+psycopg2://{user}:{password}@{hostname}:5432{database}"
        )
        SQLALCHEMY_TRACK_MODIFICATIONS = False
    except Exception as e:
        print('Database config error: '+str(e))

app = dash.Dash(
    server=server, external_stylesheets=external_stylesheets, url_base_pathname='/')

df = pdr.get_data_yahoo("SPY", start="2017-01-01", end="2017-04-30")
fig = px.scatter(df, x=df.index, y='Close')
app.layout = html.Div(children=[
    html.H4(children='SPY Close values for 2017'),
    html.Div(
        dcc.Graph(figure=fig)),
])
