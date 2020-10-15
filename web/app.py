#Module Import
from callbacks import * 



dropdown = dcc.Dropdown(
    placeholder="Favourites",
    id='favouritesDropdown',
    value='',
    options=[{'label':'SPY', 'value' : 'SPY'}],
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
                    dbc.Button("Register", color="primary",id="registerButton", n_clicks = 0),
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
                    dbc.Button("Login", color="primary", id="loginButton", n_clicks = 0),
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
        html.Div(
        [dbc.Input(placeholder="Enter stock ticker...", type="text",id="stock_ticker",style={"margin" : "2px","width" : "25%"}),
        dcc.Dropdown(id="dropdownIntervals",
            placeholder = "Select interval",
            options = [
                    {'label' : '2 Minute', 'value' : '2m'},
                    {'label' : '30 Minutes', 'value' : '30m'},
                    {'label' : 'Daily', 'value' : '1d'},
                    {'label' : 'Weekly', 'value' : '1wk'},
                    {'label' : 'Monthly', 'value' : '1mo'}                            
            ],style={"width" : "50%","margin" : "1px"}), 
        dcc.DatePickerRange(
            id='dateTimePicker',
            min_date_allowed=date(1995, 8, 5),
            initial_visible_month=date.today(),
            start_date=date.today()-timedelta(days=7),
            end_date=date.today(),
            style={"margin" : "4px"}
        )]),
        html.Br(),
        html.Div(children=[],id='favouritesOutPut'),
        html.Div(children=[],id='dataExportOutput'),
        dbc.Button("Generate Chart", id="Generate",style={"margin" : "2px"}, n_clicks = 0),                   
        dbc.Button("Add To Favourites", id="addToFavourites")],
        style={"padding-left" : "40%","padding-top" : "2%"}),
        html.Div(
                [dcc.Loading(
                        id="loadingMain",
                        children=[
                        html.Div(children=[],id='chartmain'),
                        html.Div(children=[],id='fundamentals')],
                        type="circle",
                        style={"padding-top" : "20%"})],
        id = 'mainDiv')
])