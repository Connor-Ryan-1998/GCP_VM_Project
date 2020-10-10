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

navbar = dbc.NavbarSimple(
    children=[
        dbc.NavItem(dbc.NavLink("", href="#")),
        dbc.DropdownMenu(
            children=[
                dbc.DropdownMenuItem("More pages", header=True),
                dbc.DropdownMenuItem("Page 2", href="#"),
                dbc.DropdownMenuItem("Page 3", href="#"),
            ],
            nav=True,
            in_navbar=True,
            label="More",
        ),    
    html.Div([
        dbc.Button("Login", id="Login"),
            dbc.Modal(
            [
                dbc.ModalHeader("Header"),
                dbc.ModalBody("This is the content of the modal"),
                dbc.ModalFooter(
                    dbc.Button("Close", id="close", className="ml-auto")
                ),
            ],
            id="modal",
        )]),
    ],
    brand="NavbarSimple",
    brand_href="#",
    color="primary",
    dark=True,
)
df = pdr.get_data_yahoo("SPY", start="2017-01-01", end="2017-04-30")
fig = px.scatter(df, x=df.index, y='Close')
app.layout = html.Div(children=[navbar,
    html.H4(children='SPY Close values for 2017'),
    html.Div(
        dcc.Graph(figure=fig))
])

@app.callback(
    Output("modal", "is_open"),
    [Input("Login", "n_clicks"), Input("close", "n_clicks")],
    [State("modal", "is_open")],
)
def toggle_modal(n1, n2, is_open):
    if n1 or n2:
        return not is_open
    return is_open
