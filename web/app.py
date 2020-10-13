# Module Imports
# from flask import Flask, session, copy_current_request_context, request, Flask, jsonify, make_response, redirect
# ##from dash.dependencies import Input, Output, State
# from datetime import date,datetime,timedelta
# #from pandas_datareader import data as pdr
# ##import dash_bootstrap_components as dbc
# import dash_html_components as html
# import dash_core_components as dcc
# import flask_sqlalchemy
# #import plotly.express as px
# import psycopg2
# from callbacks import *
# ##import dash
# ##import flask
# ##import os
# import base64
# import sys

from callbacks import * 

# external_stylesheets = [dbc.themes.BOOTSTRAP]

# server = flask.Flask(__name__)
# server.config['SECRET_KEY'] = os.urandom(24)
# yf.pdr_override()

# app = dash.Dash(
#     server=server, external_stylesheets=external_stylesheets, url_base_pathname='/')
#Favourites
dropdown = dcc.Dropdown(
    placeholder="Favourites",
    id='favouritesDropdown',
    value='SPY',
    options=[
            {'label':'SPY', 'value' : 'SPY'}
            ],
    style = {"margin-right":"30px"}
)

register_email = dbc.FormGroup(
    [
        dbc.Label("Email", html_for="example-email"),
        dbc.Input(type="email", id="registerEmail", placeholder="Enter email"),
    ]
)


register_pw = dbc.FormGroup(
    [
        dbc.Label("Password", html_for="register_pw"),
        dbc.Input(
            type="password",
            id="register_pw",
            placeholder="Enter password",
        ),
    ]
)

login_email = dbc.FormGroup(
    [
        dbc.Label("Email", html_for="login_email"),
        dbc.Input(type="email", id="login_email", placeholder="Enter email"),
    ]
)

login_pw = dbc.FormGroup(
    [
        dbc.Label("Password", html_for="login_pw"),
        dbc.Input(
            type="password",
            id="login_pw",
            placeholder="Enter password",
        ),
    ]
)

form1 = dbc.Form([register_email, register_pw],style={"padding" : "2%"})
form2 = dbc.Form([login_email, login_pw],style={"padding" : "2%"})

#Navbar
navbar = dbc.NavbarSimple(
    children=[
        dbc.NavItem(dbc.NavLink("Not Logged in", href="#", id='loggedInStatus')),
        dropdown,
        html.Div([
        dbc.Button("Register", id="Register",style = {"margin-right":"30px"}),
            dbc.Modal(
            [
                dbc.ModalHeader("Register"),
                form1,
                html.Div(children=[],id='registeredStatus'),
                dbc.ModalFooter(children=[
                    dbc.Button("Register", color="primary",id="registerButton"),
                    dbc.Button("Close", id="close_register", className="ml-auto")]
                ),
            ],
            id="Register_modal",
        )]),    
        html.Div([
        dbc.Button("Login", id="Login",style = {"margin-right":"30px"}),
            dbc.Modal(
            [
                dbc.ModalHeader("Login"),
                form2,
                html.Div(children=[],id='loggedInStatusSuccess'),
                dbc.ModalFooter(children=[
                    dbc.Button("Login", color="primary", id="loginButton"),
                    dbc.Button("Close", id="close", className="ml-auto")]
                ),
            ],
            id="Login_modal",
        )]),
    ],
    brand="Stock Tracker",
    brand_href="#",
    color="primary",
    dark=True,
)

#App layout
app.layout = html.Div(children=[navbar,
    html.Div(children = [
        html.H4(children=['Stock Monitor + Fundamentals'],id='headerTitle'),
        html.Div([dbc.Input(placeholder="Enter stock...", type="text",id="stock_ticker",style={"margin" : "2px","width" : "15%","padding" : "2%"}),
        dcc.DatePickerRange(
            id='dateTimePicker',
            min_date_allowed=date(1995, 8, 5),
            initial_visible_month=date.today(),
            start_date=date.today()-timedelta(days=7),
            end_date=date.today(),
        )]),
        html.Br(),
        html.Div(children=[],id='favouritesOutPut'),
        dbc.Button("Generate Chart", id="Generate",style={"margin" : "2px"}),
        dbc.Button("Add To Favourites", id="addToFavourites")],
        style={"padding-left" : "40%","padding-top" : "2%"}),
        html.Div(children=[
                        html.Div(children=[],id='chartmainF'),
                        html.Div(children=[],id='fundamentalsF')
                        ],
                id = 'favouritesDiv'),
        html.Div(children=[
                        html.Div(children=[],id='chartmain'),
                        html.Div(children=[],id='fundamentals')
                ],
        id = 'mainDiv')
])