# Module Imports
from flask import Flask, session, copy_current_request_context, request, Flask, jsonify, make_response, redirect
from dash.dependencies import Input, Output, State
from datetime import date,datetime
import dash_bootstrap_components as dbc
import dash_html_components as html
import dash_core_components as dcc
import flask_sqlalchemy
import plotly.express as px
import psycopg2
import dash
import flask
import os
import base64
import sys
import yfinance as yf
from pandas_datareader import data as pdr

external_stylesheets = [dbc.themes.BOOTSTRAP]

server = flask.Flask(__name__)
server.config['SECRET_KEY'] = os.urandom(24)
yf.pdr_override()

app = dash.Dash(
    server=server, external_stylesheets=external_stylesheets, url_base_pathname='/')
#Favourites
dropdown = dbc.DropdownMenu(
    label="Favourites",
    children=[],
    id='favouritesDropdown'
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

form1 = dbc.Form([register_email, register_pw])
form2 = dbc.Form([login_email, login_pw])

#Navbar
navbar = dbc.NavbarSimple(
    children=[
        dbc.NavItem(dbc.NavLink("Not Logged in", href="#", id='loggedInStatus')),
        dropdown,
        html.Div([
        dbc.Button("Register", id="Register"),
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
        dbc.Button("Login", id="Login"),
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

# #Data sets
df = pdr.get_data_yahoo("MSFT", start="2017-01-01", end="2018-04-30")
fig = px.scatter(df, x=df.index, y='Close')


#App layout
app.layout = html.Div(children=[navbar,
    html.H4(children=['SPY Close values for 2017'],id='headerTitle'),
    html.Div([dbc.Input(placeholder="Enter stock...", type="text",id="stock_ticker",style={"width" : "15%"}),
    dcc.DatePickerRange(
        id='dateTimePicker',
        min_date_allowed=date(1995, 8, 5),
        initial_visible_month=date(2017, 8, 5),
        start_date=date(2017, 1, 1),
        end_date=date(2017, 8, 25)
    )]),
    html.Br(),
    dbc.Button("Generate Chart", id="Generate"),
    dbc.Button("Add To Favourites", id="addToFavourites"),
    html.Div(children=[dcc.Graph(figure=fig)],id='chartmain')
])


#Callbacks
##Login callbacks
@app.callback(
    Output("Login_modal", "is_open"),
    [Input("Login", "n_clicks"), Input("close", "n_clicks")],
    [State("Login_modal", "is_open")],
)
def toggle_login_modal(n1, n2, is_open):
    if n1 or n2:
        return not is_open
    return is_open

@app.callback(
    Output("loggedInStatusSuccess"), "children"),
    Output("loggedInStatus", "children"),
    Output("favouritesDropdown","children"),
    [Input("loginButton", "n_clicks")],
    [dash.dependencies.State("login_email", "value"),
    dash.dependencies.State("login_pw", "value")],
)
def loginAccount(n_clicks,email,password):
    favourites = []
    if (n_clicks):
        conn = psycopg2.connect(
        host="postgres",
        database="production",
        user="postgres",
        password="postgres")
        cur = conn.cursor()
        #encrypt LOGIN password
        encryptedLoginPassword = base64.b64encode(password.encode("utf-8")).decode("utf-8")
        try:
            cur.execute("SELECT password from users WHERE username = '{}'".format(email)))
            result=cur.fetchone()
            print(result[0])
            for ticker in ['MSFT','AAPL']:
                favourites.append(dbc.DropdownMenuItem(str(ticker)))
            return 'Login successful, you may exit the modal'. 'Logged in as ' + str(email),favourites
        except Exception as e:
            return 'Error: ' + str(e)

##Register Callbacks
@app.callback(
    Output("Register_modal", "is_open"),
    [Input("Register", "n_clicks"), Input("close_register", "n_clicks")],
    [State("Register_modal", "is_open")],
)
def toggle_register_modal(n1, n2, is_open):
    if n1 or n2:
        return not is_open
    return is_open

@app.callback(
    Output("registeredStatus", "children"),
    [Input("registerButton", "n_clicks")],
    [dash.dependencies.State("registerEmail", "value"),
    dash.dependencies.State("register_pw", "value")],
)
def registerAccount(n_clicks,email,password):
    if (n_clicks):
        conn = psycopg2.connect(
        host="postgres",
        database="production",
        user="postgres",
        password="postgres")
        cur = conn.cursor()
        #encrypt password
        encryptedPassword = base64.b64encode(password.encode("utf-8")).decode("utf-8")
        currentDateTime = datetime.now()
        try:
            cur.execute("INSERT INTO users(username,password,dateCreated) VALUES('{}','{}','{}')".format(email,encryptedPassword,currentDateTime))
            return 'Registered'
        except Exception as e:
            return 'Error: '+ str(e)




###Main chart generation
@app.callback(
    Output("chartmain", "children"),
    [Input("Generate", "n_clicks")],
    [dash.dependencies.State('dateTimePicker', 'start_date'),
    dash.dependencies.State('dateTimePicker', 'end_date'),
    dash.dependencies.State("stock_ticker", "value")])
def generate_chart(n_clicks, start_date, end_date, value):
    if (n_clicks):
        df = pdr.get_data_yahoo(value, start=start_date, end=end_date)
        fig = px.line(df, x=df.index, y='Close')
        return dcc.Graph(figure=fig)
