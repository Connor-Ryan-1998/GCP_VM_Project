# Module Imports
from flask import Flask, session, copy_current_request_context, request, Flask, jsonify, make_response, redirect
from dash.dependencies import Input, Output, State
import mariadb
import pandas as pd
import dash_bootstrap_components as dbc
import dash_html_components as html
import dash_core_components as dcc
import dash
import flask
import os
import sys
import yfinance as yf
external_stylesheets = [dbc.themes.BOOTSTRAP]

server = flask.Flask(__name__)
server.config['SECRET_KEY'] = os.urandom(24)

app = dash.Dash(
    server=server, external_stylesheets=external_stylesheets, url_base_pathname='/')

host = ""
try:
    conn = mariadb.connect(
        user="admin",
        password="password",
        host=host,
        port=3306,
        database="users"
    )
    cur = conn.cursor()
except mariadb.Error as e:
    print(f"Error connecting to MariaDB Platform: {e}")
    # sys.exit(1)

# app.layout = HTML HERE

msft = yf.Ticker("AEF.AX")
print(msft.info)
