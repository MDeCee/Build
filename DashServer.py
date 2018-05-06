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

df = pd.read_csv('Dataframes/Countries.csv', error_bad_lines=False)[:50]
#df2 = pd.read_csv('Dataframes/Languages.csv')[:50]
df3 = pd.read_csv('Dataframes/People.csv')[:100000]
df6 = pd.read_csv('Dataframes/People2.csv', error_bad_lines=False)
df7 = pd.read_csv('Dataframes/People3.csv', error_bad_lines=False)
#df4 = pd.read_csv('Dataframes/SuicideByCountry.csv')[:50]
#df5 = pd.read_csv('Dataframes/SuicideByDate.csv')[:50]
plotly.tools.set_credentials_file(username='MDeCee', api_key='XekXmMpB1MgONf6C5rLS')
start_time = time.time()
APP_NAME = 'Dash Authentication Twitter'
APP_URL = 'https://mdc-dash-win.herokuapp.com'
#APP_URL = '127.0.0.1:8050'
app = dash.Dash(__name__)
server = app.server
auth = dash_auth.PlotlyAuth(
    app,
    APP_NAME,
    'private',
    APP_URL
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
    dcc.Dropdown(
        id='xaxis-column',
        options=[{'label': i, 'value': i} for i in df['country_location']],
        multi=True
    ),
    dcc.Graph(
        id='bar'
    ),
    dcc.Link('Go to Page 1', href='/page-1')
])


page_1_layout = html.Div([
    html.H1('Records'),
    dt.DataTable(
                rows=df3.to_dict('records'),
                filterable=True,
                sortable=True,
                editable=False,
                min_height= 500,
                column_widths=80
            ),
    html.Div([
    dt.DataTable(
                rows=df6.to_dict('records'),
                filterable=True,
                sortable=True,
                editable=False,
                min_height=500
            )], style={'width': '49%', 'display': 'inline-block', 'vertical-align': 'left'}),
    html.Div([], style={'width': '1%', 'display': 'inline-block', 'vertical-align': 'middle'}),
    html.Div([
    dt.DataTable(
        rows=df7.to_dict('records'),
        filterable=True,
        sortable=True,
        editable=False,
        min_height=500
    )], style={'width': '49%', 'display': 'inline-block', 'vertical-align': 'right'}),
 #   html.Div(id='page-1-content'),
    html.Div([
    html.H1('Countries'),
	dt.DataTable(
                rows=df.to_dict('records'),
                row_selectable=True,
                selected_row_indices=[],
                filterable=True,
                sortable=True,
                min_height=500,
                editable=False,
                id='datatable'
            ),
    html.Div(id='selected-indexes'),
    dcc.Graph(
        id='graph'
    ),
#    ],className='container', style={'maxWidth': '90%'}),
], style={'marginLeft': 100, 'marginRight': 100}),
	html.Br(),
    dcc.Link('Go back to home', href='/'),

])
#, className="container"

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

