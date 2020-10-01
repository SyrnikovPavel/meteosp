import pandas as pd
import datetime
from openpyxl import load_workbook
import statsmodels.api as sm
import plotly.graph_objects as go
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output


def load_data():

    # TODO Сделать обновление из базы

    data = [[
        x.date,
        x.temp,
        x.hum,
        x.pres,
        x.lux
    ] for x in Climat.select()]

    df = pd.DataFrame(data, columns=['date', 'temp', 'hum', 'pres', 'lux'])
    df.index = df['date']
    del df['date']

    l30_date = (datetime.datetime.today().replace(hour=1, minute=0, second=0, microsecond=0) - datetime.timedelta(30))
    l30_df = df[df.index >= l30_date]
    mean_by_day_df = l30_df.groupby(by=[l30_df.index.to_period('D')]).mean()
    mean_by_hour_df = l30_df.groupby(by=[l30_df.index.hour]).mean()
    return df, mean_by_day_df, mean_by_hour_df


def get_trend_trace(x, y, name_line_trend):
    return go.Scatter(x=x, y=sm.nonparametric.lowess(y, x)[:, 1].round(2),
                      mode='lines',
                      name=name_line_trend,
                      yaxis='y1'
                      )


def get_scatter_trace(x, y, name_line):
    return go.Scatter(x=x, y=y.round(2),
                      mode='lines',
                      name=name_line,
                      yaxis='y1',
                      )


def get_bar_trace(x, y, name_line):
    return go.Bar(x=x, y=y.round(2), name=name_line, yaxis='y1')


def get_graphs(df, mean_by_day_df, mean_by_hour_df, variable_name='temp'):

    russian_names = {
        'temp': 'Температура',
        'hum': 'Влажность',
        'pres': 'Давление',
        'lux': 'Освещенность'
    }

    names_y_axis = {
        'temp': 't, C',
        'hum': 'h, %',
        'pres': 'p, мм.рт.ст.',
        'lux': 'l, люкс'
    }

    names_plot = {
        'temp': 'Среднесуточная температура',
        'hum': 'Среднесуточная влажность',
        'pres': 'Среднесуточное давление',
        'lux': 'Среднесуточная освещенность'
    }

    x = df.index
    y = df[variable_name].values
    name_line = variable_name
    name_plot = russian_names.get(variable_name)
    name_y_axis = names_y_axis.get(variable_name)
    name_line_trend = name_line + '_trend'

    trace1 = get_scatter_trace(x, y, name_line)
    trace2 = get_trend_trace(x, y, name_line_trend)

    data_fig = [trace1, trace2]
    layout = go.Layout(title=name_plot,
                       yaxis=dict(title=name_y_axis),
                       )

    all_data = go.Figure(data=data_fig, layout=layout)

    x = mean_by_day_df.index.to_timestamp()
    y = mean_by_day_df[variable_name].values
    name_plot = names_plot.get(variable_name) + ' за последние 30 дней'

    trace1 = get_bar_trace(x, y, name_line)
    trace2 = get_trend_trace(x, y, name_line_trend)

    data_fig = [trace1, trace2]
    layout = go.Layout(title=name_plot,
                       yaxis=dict(title=name_y_axis),
                       )

    mean_by_day = go.Figure(data=data_fig, layout=layout)

    x = mean_by_hour_df.index
    y = mean_by_hour_df[variable_name].values
    name_plot = names_plot.get(variable_name) + ' по часам за последние 30 дней'

    trace1 = get_bar_trace(x, y, name_line)
    trace2 = get_trend_trace(x, y, name_line_trend)

    data_fig = [trace1, trace2]
    layout = go.Layout(title=name_plot,
                       yaxis=dict(title=name_y_axis),
                       )

    mean_by_hour = go.Figure(data=data_fig, layout=layout)

    return all_data, mean_by_day, mean_by_hour


def serve_layout():
    df, mean_by_day_df, mean_by_hour_df = load_data()
    all_data, mean_by_day, mean_by_hour = get_graphs(df, mean_by_day_df, mean_by_hour_df, variable_name='temp')

    return html.Div(children=[
        html.H1(children='Климат контроль v. 0.0.1'),

        dcc.Dropdown(
            id='main_var',
            options=[
                {'label': 'Температура', 'value': 'temp'},
                {'label': 'Влажность', 'value': 'hum'},
                {'label': 'Давление', 'value': 'pres'},
                {'label': 'Освещенность', 'value': 'lux'}
            ],
            value='temp'
        ),
        dcc.Graph(
            id='all_data',
            figure=all_data
        ),
        html.Span(children=[
            dcc.Graph(
                id='mean_by_day',
                figure=mean_by_day
            ),
            dcc.Graph(
                id='mean_by_hour',
                figure=mean_by_hour
            ),
        ])
    ])


def init_dashboard(server):
    dash_app = dash.Dash(
        server=server,
        routes_pathname_prefix='/dashapp/',
    )
    dash_app.layout = serve_layout
    init_callbacks(dash_app)
    return dash_app.server


def init_callbacks(dash_app):
    @dash_app.callback(
        [Output('all_data', 'figure'),
         Output('mean_by_day', 'figure'),
         Output('mean_by_hour', 'figure')],
        [Input('main_var', 'value')])
    def update_figure(variable_name):
        df, mean_by_day_df, mean_by_hour_df = load_data()
        all_data, mean_by_day, mean_by_hour = get_graphs(
            df,
            mean_by_day_df,
            mean_by_hour_df,
            variable_name=variable_name
        )

        return all_data, mean_by_day, mean_by_hour
