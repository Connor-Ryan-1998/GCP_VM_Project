from flask import Flask, session, copy_current_request_context, request, Flask, jsonify, make_response, redirect
from datetime import date,datetime,timedelta
import dash_html_components as html
from dash.dependencies import Input, Output, State
from pandas_datareader import data as pdr
import pandas as pd
import dash_table
import plotly.express as px
import dash_core_components as dcc
import dash_core_components as dcc
import flask_sqlalchemy
import psycopg2
from callbacks import *
import base64
import sys
import dash_bootstrap_components as dbc
import flask
import os
import yfinance as yf
import dash

external_stylesheets = [dbc.themes.BOOTSTRAP]

server = flask.Flask(__name__)
server.config['SECRET_KEY'] = os.urandom(24)
yf.pdr_override()

app = dash.Dash(
    server=server, external_stylesheets=external_stylesheets, url_base_pathname='/')