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


#Callbacks
# ##Login callbacks
# @app.callback(
#     Output("Login_modal", "is_open"),
#     [Input("Login", "n_clicks"), Input("close", "n_clicks")],
#     [State("Login_modal", "is_open")],
# )
# def toggle_login_modal(n1, n2, is_open):
#     if n1 or n2:
#         return not is_open
#     return is_open

# @app.callback(
#     Output("loggedInStatusSuccess", "children"),
#     Output("loggedInStatus", "children"),
#     Output("favouritesDropdown","options"),
#     [Input("loginButton", "n_clicks")],
#     [dash.dependencies.State("login_email", "value"),
#     dash.dependencies.State("login_pw", "value")],
# )
# def loginAccount(n_clicks,email,password):
#     favourites = []
#     try:
#         if (n_clicks):
#             conn = psycopg2.connect(
#             host="postgres",
#             database="production",
#             user="postgres",
#             password="postgres")
#             cur = conn.cursor()
#             #encrypt LOGIN password
#             encryptedLoginPassword = base64.b64encode(password.encode("utf-8")).decode("utf-8")
#             cur.execute("SELECT password from users WHERE username = '{}';".format(email))
#             result=cur.fetchone()
#             if result = encryptedLoginPassword:
#                 session['username'] = email
#                 cur.execute("SELECT ticker from userFavourites uF inner join users u on u.userId = uF.userId \
#                              WHERE u.username = '{}';".format(session['username']))
#                 result = cur.fetchall()
#                 for ticker in result:
#                     favourites.append(str(ticker))
#                 return 'Login successful ' + str(result) + 'g, you may exit the modal', 'Logged in as ' + str(email),[{'key': i, 'value': i} for i in favourites]
#             else:
#                 return 'Authentication failed: Please check username/password'
#     except Exception as e:
#         return 'Error: ' + str(e)

# ##Register Callbacks
# @app.callback(
#     Output("Register_modal", "is_open"),
#     [Input("Register", "n_clicks"), Input("close_register", "n_clicks")],
#     [State("Register_modal", "is_open")],
# )
# def toggle_register_modal(n1, n2, is_open):
#     if n1 or n2:
#         return not is_open
#     return is_open

# @app.callback(
#     Output("registeredStatus", "children"),
#     [Input("registerButton", "n_clicks")],
#     [dash.dependencies.State("registerEmail", "value"),
#     dash.dependencies.State("register_pw", "value")],
# )
# def registerAccount(n_clicks,email,password):
#     try:
#         if (n_clicks):
#             conn = psycopg2.connect(
#             host="postgres",
#             database="production",
#             user="postgres",
#             password="postgres")
#             cur = conn.cursor()
#             #encrypt password
#             encryptedPassword = base64.b64encode(password.encode("utf-8")).decode("utf-8")
#             currentDateTime = datetime.now()
#             cur.execute("INSERT INTO users(username,password,dateCreated) VALUES('{}','{}','{}');".format(email,encryptedPassword,str(currentDateTime)))
#             cur.execute("SELECT username FROM users WHERE username = '{}' ;".format(email))
#             result = cur.fetchone()
#             return 'Registered: ' + str(result)
#     except Exception as e:
#         return 'Error: '+ str(e)

# #Add to favourites
# # [Input("Generate", "n_clicks")],
# #     [dash.dependencies.State('dateTimePicker', 'start_date'),
# #     dash.dependencies.State('dateTimePicker', 'end_date'),
# #     dash.dependencies.State("stock_ticker", "value")])
# # @app.callback(
# #Favourites Callback
# @app.callback(
#     Output("chartmainF", "children"),
#     Output("fundamentalsF", "children"),
#     Output("mainDiv","style"),
#     [Input("favouritesDropdown", "value")],
#     [dash.dependencies.State('dateTimePicker', 'start_date'),
#     dash.dependencies.State('dateTimePicker', 'end_date')])
# def generate_chartFromFavourites(value,start_date,end_date):
#     try:
#         if not value:
#             return 'Invalid Favourite', 'Invalid Favourite Fundamental', {'display': 'none'}
#         else:
#             df = pdr.get_data_yahoo(value, start=start_date, end=end_date)
#             fig = px.line(df, x=df.index, y='Close')
#             return dcc.Graph(figure=fig), 'Fundamentals of stonk', {'display': 'none'}
#     except Exception as e:
#         return 'Error: '+ str(e), 'Invalid Favourite Fundamental', {'display': 'none'}

# ###Main chart generation
# @app.callback(
#     Output("chartmain", "children"),
#     Output("fundamentals", "children"),
#     Output("favouritesDiv","style"),
#     [Input("Generate", "n_clicks")],
#     [dash.dependencies.State('dateTimePicker', 'start_date'),
#     dash.dependencies.State('dateTimePicker', 'end_date'),
#     dash.dependencies.State("stock_ticker", "value")])
# def generate_chart(n_clicks, start_date, end_date, value):
#     if (n_clicks):
#         try:
#             df = pdr.get_data_yahoo(value, start=start_date, end=end_date)
#             fig = px.line(df, x=df.index, y='Close')
#             return dcc.Graph(figure=fig), 'Fundamentals of stonk', {'display': 'none'}
#         except Exception as e:
#             return 'Error: '+ str(e), 'No Fundamentals',  {'display': 'none'}
