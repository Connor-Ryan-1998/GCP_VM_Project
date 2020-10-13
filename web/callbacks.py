from config import *
# from dash.dependencies import Input, Output, State
# from pandas_datareader import data as pdr
# import plotly.express as px
# import dash_core_components as dcc

try:
    conn = psycopg2.connect(
                        host="postgres",
                        database="production",
                        user="postgres1",
                        password="secret123")
    cur = conn.cursor()
except Exception as e:
    print('Not Connected: ' +str(e))
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
    Output("loggedInStatusSuccess", "children"),
    Output("loggedInStatus", "children"),
    Output("favouritesDropdown","options"),
    [Input("loginButton", "n_clicks")],
    [dash.dependencies.State("login_email", "value"),
    dash.dependencies.State("login_pw", "value")],
)
def loginAccount(n_clicks,email,password):
    try:
        if (n_clicks):
            cur = conn.cursor()
            #encrypt LOGIN password
            encryptedLoginPassword = base64.b64encode(password.encode("utf-8")).decode("utf-8")
            cur.execute("SELECT password from public.users WHERE username = '{}';".format(email))
            result=cur.fetchone()
            if str(result[0]) == str(encryptedLoginPassword):
                favourites = []
                session['username'] = email
                cur.execute("SELECT ticker from public.userFavourites uF inner join users u on u.userId = uF.userId WHERE u.username = '{}';".format(session['username']))
                result = cur.fetchall()
                for ticker in result:
                    favourites.append(str(ticker[0]))
                if favourites == None:
                    favourites =  ['SPY']
                return 'Login successful ' + str(session['username']) + ', you may exit the modal', 'Logged in as ' + str(email),[{'label': str(i), 'value': str(i)} for i in favourites]
            else:
                cur.execute("rollback;")
                return 'Authentication failed: Please check username/password','Login failed (please try again)', [{'label': 'SPY', 'value': 'SPY'}]
    except Exception as e:
        cur.execute("rollback;")
        return 'Error: ' + str(e),'Login failed (please try again)', [{'key': 'SPY', 'value': 'SPY'}]

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
    try:
        if (n_clicks):
            #encrypt password
            encryptedPassword = base64.b64encode(password.encode("utf-8")).decode("utf-8")
            currentDateTime = datetime.now()
            cur.execute("INSERT INTO public.users(username,password,dateCreated) VALUES('{}','{}','{}');".format(email,encryptedPassword,str(currentDateTime)))
            cur.execute("SELECT username FROM public.users WHERE username = '{}' ;".format(email))
            result = cur.fetchone()
            return 'Registered: ' + str(result)
    except Exception as e:
        cur.execute("rollback;")
        return 'Error: '+ str(e)

#Add to favourites
@app.callback(
     Output("favouritesOutPut", "children"),
     [Input("addToFavourites", "n_clicks")],
     [dash.dependencies.State("stock_ticker", "value")])
def addChartToFavourites(n_clicks, value):
    if (n_clicks):
        try:
            if session.get('username') is not None:
                try:
                    cur.execute("SELECT userId FROM public.users WHERE username = '{}' ;".format(session['username']))
                    result = cur.fetchone()
                    cur.execute("INSERT INTO public.userFavourites(userId,ticker) VALUES({},'{}');".format(result[0],str(value)))
                    return 'Added {} to your favourites'.format(value)
                except Exception as e:
                    return 'Error: '+ str(e)
            elif session.get('username') is None:
                return 'User not logged in'
        except Exception as e:
            return 'Error: '+ str(e)
    
#Favourites Callback
@app.callback(
    Output("chartmainF", "children"),
    Output("fundamentalsF", "children"),
    [Input("favouritesDropdown", "value")],
    [dash.dependencies.State('dateTimePicker', 'start_date'),
    dash.dependencies.State('dateTimePicker', 'end_date')])
def generate_chartFromFavourites(value,start_date,end_date):
    try:
        if not value:
            return 'Invalid Favourite', 'Invalid Favourite Fundamental'
        else:
            df = pdr.get_data_yahoo(value, start=start_date, end=end_date)
            fig = px.line(df, x=df.index, y='Close')
            return dcc.Graph(figure=fig), 'Fundamentals of stonk'
    except Exception as e:
        return 'Error: '+ str(e), 'Invalid Favourite Fundamental'

###Main chart generation
@app.callback(
    Output("chartmain", "children"),
    Output("fundamentals", "children"),
    [Input("Generate", "n_clicks")],
    [dash.dependencies.State('dateTimePicker', 'start_date'),
    dash.dependencies.State('dateTimePicker', 'end_date'),
    dash.dependencies.State("stock_ticker", "value")])
def generate_chart(n_clicks, start_date, end_date, value):
    if (n_clicks):
        try:
            df = pdr.get_data_yahoo(value, start=start_date, end=end_date)
            fig = px.line(df, x=df.index, y='Close')
            return dcc.Graph(figure=fig), 'Fundamentals of stonk'
        except Exception as e:
            return 'Error: '+ str(e), 'No Fundamentals'

