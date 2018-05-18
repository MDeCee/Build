# -*- coding: utf-8 -*-
import plotly.graph_objs as go
import pandas as pd
import time
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_table_experiments as dt
import plotly
import dash_auth

df = pd.read_csv('Dataframes/Countries.csv', error_bad_lines=False)
#df2 = pd.read_csv('Dataframes/Languages.csv')[:50]
#df4 = pd.read_csv('Dataframes/SuicideByCountry.csv')[:50]
df5 = pd.read_csv('Dataframes/SuicideByDate.csv')[:50]
start_time = time.time()
df6 = pd.read_csv('Dataframes/People2.csv', error_bad_lines=False)

Users_Passwords = [
    ['Admin', '7797']
]
app = dash.Dash('auth')
server = app.server
auth = dash_auth.BasicAuth(
    app,
    Users_Passwords
)
app.scripts.config.serve_locally=True
app.config.suppress_callback_exceptions = True

def make_layout():
   return html.Div([
    html.Div(dt.DataTable(rows=[{}]), style={'display': 'none'}),
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content'),
])

@app.callback(dash.dependencies.Output('page-content', 'children'),
              [dash.dependencies.Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/page-1':
        return page_1_layout
    else:
        return index_page
app.css.append_css({
    'external_url': 'https://codepen.io/chriddyp/pen/bWLwgP.css'
})


app.layout = make_layout


index_page = html.Div([
    dcc.Markdown('''
Twitter Suicidal and Depressive Behavior Visualizer
===================================== 

**Made for educational purposes.**           
This web page is made to spread awareness about depression and suicidal behavior, and how one would need to act if they 
know people who behave in a similar manner.   

**Viewer discretion advised.** 

This page is made using [Dash](https://plot.ly/products/dash/).
Use the dropdown above to select location of interest to display the number of entries from that location. 
*Terms of Service in Development.*
    '''),
    dcc.Dropdown(
        id='xaxis-column',
        options=[{'label': i, 'value': i} for i in df['country_location']],
        multi=True
    ),
    dcc.Graph(
        id='bar'
    ),
    dcc.Link('I accept the Terms of Service', href='/page-1')
])


page_1_layout = html.Div([
    html.H1('Records'),
    html.Div([
        dcc.Tabs(
            tabs=[
                {'label': 'Correlation Details', 'value': 1},
                {'label': 'User Details', 'value': 2},
                {'label': 'Tweet Details', 'value': 3},
            ],
            value=1,
            id='tabs2',
            vertical=False,
            style={'height': '46', 'width': '100%', 'float': 'right'}),
        dcc.Tabs(
            tabs=[
                {'label': 'Low Risk', 'value': 1},
                {'label': 'Risk', 'value': 2},
                {'label': 'High Risk', 'value': 3},
            ],
            value=1,
            id='tabs',
            vertical=True,
            style={'height': '1000', 'width': '20%', 'float': 'left'}),
        html.Div(id='tab-output', style={'height': '400', 'width': '80%', 'float': 'left'})
    ], id='content', style={'height': '1000'}),
    dcc.Graph(
        id='histogram',
        figure={
            'data': [
                go.Scatter(
                    y=df5['NrTweets'], x=df5['Date'], # Data
                    mode='lines'
                   )
            ],
            'layout': {
                'title': '"Suicide" usage on Twitter'
            }
        }
    ),
 #   html.Div(id='page-1-content'),
    html.Div([
    html.H1('Countries'),
    html.Div(id='selected-indexes'),
    dcc.Graph(
            id='graph'
    ),
	dt.DataTable(
                rows=df.to_dict('records'),
                row_selectable=True,
                selected_row_indices=[],
                filterable=True,
                sortable=True,
                min_height=350,
                editable=False,
                id='datatable'
            )
#    ],className='container', style={'maxWidth': '90%'}),
], style={'marginLeft': 40, 'marginRight': 40}),
	html.Br(),
    dcc.Link('Go back to home', href='/'),

], style={'marginLeft': 40, 'marginRight': 40})
#, className="container"
@app.callback(dash.dependencies.Output('tab-output', 'children'),
              [dash.dependencies.Input('tabs', 'value'),
               dash.dependencies.Input('tabs2', 'value')])
def display_tab(value, value2):
    if value2 == 1:
        if value == 1:
            df3 = pd.read_csv('Dataframes/People.csv')[:100000]
            return (
                html.Div(dt.DataTable(
                    rows=df3.to_dict('records'),
                    filterable=True,
                    sortable=True,
                    editable=False,
                    min_height= 1000,
                    column_widths=80
                ))
            )
        if value == 2:
            df3 = pd.read_csv('Dataframes/PeopleRisk.csv')[:100000]
            return (
                html.Div(dt.DataTable(
                    rows=df3.to_dict('records'),
                    filterable=True,
                    sortable=True,
                    editable=False,
                    min_height= 1000,
                    column_widths=80
                ))
            )
        if value == 3:
            df6 = pd.read_csv('Dataframes/PeopleHighRisk.csv')[:100000]
            return (
                html.Div(dt.DataTable(
                    rows=df6.to_dict('records'),
                    filterable=True,
                    sortable=True,
                    editable=False,
                    min_height= 1000,
                    column_widths=80
                ))
            )

    if value2 == 2:
        if value == 1:
            df6 = pd.read_csv('Dataframes/People2.csv')[:100000]
            return (html.Div(dt.DataTable(
                rows=df6.to_dict('records'),
                filterable=True,
                sortable=True,
                editable=False,
                min_height=1000
            )))
        if value == 2:
            df6 = pd.read_csv('Dataframes/People2Risk.csv')[:100000]
            return (
                html.Div(dt.DataTable(
                    rows=df6.to_dict('records'),
                    filterable=True,
                    sortable=True,
                    editable=False,
                    min_height= 1000,
                    column_widths=80
                ))
            )
        if value == 3:
            df6 = pd.read_csv('Dataframes/People2HighRisk.csv')[:100000]
            return (
                html.Div(dt.DataTable(
                    rows=df6.to_dict('records'),
                    filterable=True,
                    sortable=True,
                    editable=False,
                    min_height= 1000,
                    column_widths=80
                ))
            )

    if value2 == 3:
        if value == 1:
            df7 = pd.read_csv('Dataframes/People3.csv', error_bad_lines=False)
            return (html.Div(dt.DataTable(
                rows=df7.to_dict('records'),
                filterable=True,
                sortable=True,
                editable=False,
                min_height=1000
            )))
        if value == 2:
            df7 = pd.read_csv('Dataframes/People3Risk.csv', error_bad_lines=False)
            return (html.Div(dt.DataTable(
                rows=df7.to_dict('records'),
                filterable=True,
                sortable=True,
                editable=False,
                min_height=1000
            )))
        if value == 3:
            df7 = pd.read_csv('Dataframes/People3HighRisk.csv', error_bad_lines=False)
            return (html.Div(dt.DataTable(
                rows=df7.to_dict('records'),
                filterable=True,
                sortable=True,
                editable=False,
                min_height=1000
            )))
@app.callback(dash.dependencies.Output('datatable', 'selected_row_indices'),
            [dash.dependencies.Input('graph', 'clickData')],
            [dash.dependencies.State('datatable', 'selected_row_indices')])
def update_selected_row_indices(clickData, selected_row_indices):
    if clickData:
        for point in clickData['points']:
            if point['pointNumber'] in selected_row_indices:
                selected_row_indices.remove(point['pointNumber'])
            else:
                selected_row_indices.append(point['pointNumber'])
    return selected_row_indices

@app.callback(
    dash.dependencies.Output('graph', 'figure'),
    [dash.dependencies.Input('datatable', 'rows'),
     dash.dependencies.Input('datatable', 'selected_row_indices')])
def update_figure2(rows, selected_row_indices):
    dff = pd.DataFrame(rows)
    fig = plotly.tools.make_subplots(
        rows=3, cols=1,
        subplot_titles=('Total Tweets', 'Total Tweets with Suicide', 'Total Tweets with Low Sentiment'),
        shared_xaxes=True,
        print_grid = False)

    marker = {'color': ['#0074D9']*len(dff)}
    for i in (selected_row_indices or []):
        marker['color'][i] = '#FF351B'
    fig.append_trace({
        'x': dff['country_location'],
        'y': dff['Tweets'],
        'type': 'bar',
        'marker': marker
    }, 1, 1)
    fig.append_trace({
        'x': dff['country_location'],
        'y': dff['TweetsSuicide'],
        'type': 'bar',
        'marker': marker
    }, 2, 1)
    fig.append_trace({
        'x': dff['country_location'],
        'y': dff['TweetsLowSentiment'],
        'type': 'bar',
        'marker': marker
    }, 3, 1)

    fig['layout']['showlegend'] = False

    fig['layout']['height'] = 1200

    fig['layout']['margin'] = {'l': 30,'r': 10,'t': 50,'b': 180}

    return fig


@app.callback(
    dash.dependencies.Output('bar', 'figure'),
    [dash.dependencies.Input('xaxis-column', 'value')])

def update_figure(country1):
    traces = []
    if country1 is not None:
        for i in country1:
            df_by_continent = df[df['country_location'] == i]
            traces.append(go.Bar(
                    x=df_by_continent['country_location'],  # assign x as the dataframe column 'x'
                    y=df_by_continent['Tweets']
                    )
            )

    return {
        'data': traces,
        'layout': {
                'title': 'Dash Data Visualization'
            }
    }
if __name__ == '__main__':

    app.run_server(debug=True)

