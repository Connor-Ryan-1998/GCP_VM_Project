# Module Imports
from flask import Flask, session, copy_current_request_context, request, Flask, jsonify, make_response, redirect
from dash.dependencies import Input, Output, State
from datetime import date
import dash_bootstrap_components as dbc
import dash_html_components as html
import dash_core_components as dcc
import flask_sqlalchemy
import plotly.express as px
import psycopg2
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
#Favourites
dropdown = dbc.DropdownMenu(
    label="Favourites",
    children=[
        dbc.DropdownMenuItem("ASX.AEF"),
        dbc.DropdownMenuItem("ASX.CBA"),
    ],
)

register_email = dbc.FormGroup(
    [
        dbc.Label("Email", html_for="example-email"),
        dbc.Input(type="email", id="example-email", placeholder="Enter email"),
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
        dbc.NavItem(dbc.NavLink("Not Logged in", href="#")),
        dropdown,
        html.Div([
        dbc.Button("Register", id="Register"),
            dbc.Modal(
            [
                dbc.ModalHeader("Register"),
                form1,
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

#Data sets
df = pdr.get_data_yahoo("MSFT", start="2017-01-01", end="2018-04-30")
fig = px.scatter(df, x=df.index, y='Close')


#App layout
app.layout = html.Div(children=[navbar,
    html.H4(children='SPY Close values for 2017'),
    html.Div([dbc.Input(placeholder="Enter stock...", type="text",id="stock_ticker",style={"width" : "15%"}),
    dcc.DatePickerRange(
        id='dateTimePicker',
        min_date_allowed=date(1995, 8, 5),
        initial_visible_month=date(2017, 8, 5),
        end_date=date(2017, 8, 25)
    )]),
    html.Br(),
    dbc.Button("Generate Chart", id="Generate"),
    dbc.Button("Add To Favourites", id="addToFavourites"),
    html.Div(children=[dcc.Graph(figure=fig)],id='chartmain')
])


#Callbacks
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
    Output("Register_modal", "is_open"),
    [Input("Register", "n_clicks"), Input("close_register", "n_clicks")],
    [State("Register_modal", "is_open")],
)
def toggle_register_modal(n1, n2, is_open):
    if n1 or n2:
        return not is_open
    return is_open

@app.callback(
    Output("chartmain", "children"),
    [Input("stock_ticker", "value"),
    dash.dependencies.Input('dateTimePicker', 'start_date'),
    dash.dependencies.Input('dateTimePicker', 'end_date'),
    Input("Generate", "n_clicks")])
def generate_chart(value, start_date, end_date, n_clicks: int):
    if (n_clicks > 0):
        conn = psycopg2.connect(
        host="postgres",
        database="production",
        user="postgres",
        password="postgres")
        cur = conn.cursor()
        cur.execute("SELECT * FROM information_schema.columns WHERE table_name like '%user%'")
        db_version = cur.fetchone()
        df = pdr.get_data_yahoo(value, start=start_date, end=end_date)
        fig = px.line(df, x=df.index, y='Close',title=db_version)
        return dcc.Graph(figure=fig)
