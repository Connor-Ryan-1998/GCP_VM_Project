#Module Import
from config import *


try:
    conn = psycopg2.connect(
                        host="postgres",
                        database="production",
                        user="postgres1",
                        password="secret123")
    cur = conn.cursor()
except Exception as e:
    print('Not Connected: ' +str(e))
    pass
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
    Output("stock_ticker", "value"),
    [Input("favouritesDropdown", "value")])
def generate_chartFromFavourites(value):
    try:
        if not value:
            return ''
        else:
            return value
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
    if n_clicks == None:
        n_clicks = 0
    elif (n_clicks > -1):
        try:
            df = pdr.get_data_yahoo(value, start=start_date, end=end_date)
            fig = px.line(df, x=df.index, y='Close')
            df = pd.DataFrame.from_dict([yf.Ticker(value).info])
            del df['longBusinessSummary']
            data = df.to_dict('rows')
            columns =  [{"name": i, "id": i,} for i in (df.columns)]
            return dcc.Graph(figure=fig), [dash_table.DataTable(id='fundamentalsTable',
                                                                data=data, columns=columns,
                                                                editable=False,
                                                                sort_action="native",
                                                                sort_mode="multi",
                                                                row_selectable="multi",
                                                                style_table={
                                                                    'maxHeight': '50ex',
                                                                    'overflowY': 'scroll',
                                                                    'width': '100%',
                                                                    'minWidth': '100%',
                                                                },
                                                                # style cell
                                                                style_cell={
                                                                    'fontFamily': 'Open Sans',
                                                                    'textAlign': 'center',
                                                                    'height': '60px',
                                                                    'padding': '2px 22px',
                                                                    'whiteSpace': 'inherit',
                                                                    'overflow': 'hidden',
                                                                    'textOverflow': 'ellipsis',
                                                                },
                                                                style_cell_conditional=[
                                                                    {
                                                                        'if': {'column_id': 'State'},
                                                                        'textAlign': 'left'
                                                                    },
                                                                ],
                                                                style_header={
                                                                    'fontWeight': 'bold',
                                                                    'backgroundColor': 'white',
                                                                },
                                                                style_data_conditional=[
                                                                    {
                                                                        # stripped rows
                                                                        'if': {'row_index': 'odd'},
                                                                        'backgroundColor': 'rgb(248, 248, 248)'
                                                                    },
                                                                    {
                                                                        # highlight one row
                                                                        'if': {'row_index': 4},
                                                                        "backgroundColor": "#3D9970",
                                                                        'color': 'white'
                                                                    }
                                                                ]
                )
            ]
        except Exception as e:
            return 'Error: '+ str(e), 'No Fundamentals'

