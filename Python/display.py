import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, Event
import plotly
from plotly import tools
from Database import Database
from Controller import Controller
import myutils

database = Database("mongodb://192.168.1.144:27017")
controller = Controller()
sample_rate = 100
N = 1

app = dash.Dash()

app.layout = html.Div(children=[
    html.H1(children='Hello WatchOut!'),



    html.Div(children='''
        WatchOut: A wireless intrusion detection system for your house.
    '''),

    html.Div([
        html.H2(id='Status'),
        dcc.Interval(
            id='interval-div',
            interval=1*4000,  # in milliseconds
            n_intervals=0
        )
    ]),

    # html.Div([
    dcc.Graph(id='live-graph', animate=False),
    dcc.Interval(
        id='interval-component',
        interval=1*3000,  # in milliseconds
        n_intervals=0
    )
    # ]),



    # dcc.Interval(id='graph-update', interval=1*3000),
])

@app.callback(
    Output(component_id='Status', component_property='children'),
    [Input('interval-div', 'n_intervals')]
)
def update_output_div(n):
    flag, angle, energy, avg_cos_sim = controller.predict(database, N)
    # print("flag", flag)
    if flag:
        # return 'Dangerous!'
        return 'Dangerous!' + '  ' + str(angle) + '  ' + str(energy) + '  ' + str(avg_cos_sim)
        # return 'Dangerous!' + '   '+'Angle: ' + str(angle) + '   '+'Energy: ' + str(energy) + '   '+'Sim: ' + str(avg_cos_sim)
        # return 'Dangerous!' + '\n' + 'Angle: ' + str(angle) + '\n' + 'Energy: ' + str(energy) + '\n' + 'Sim: ' + str(avg_cos_sim)
    else:
        # return 'Safe.'
        return 'Safe.' + '  ' + str(angle) + '  ' + str(energy) + '  ' + str(avg_cos_sim)
        # return 'Safe.' + '   '+ 'Angle: ' + str(angle) + '   '+'Energy: ' + str(energy) + '   '+'Sim: ' + str(avg_cos_sim)
        # return 'Safe.' + '\n' + 'Angle: ' + str(angle) + '\n' + 'Energy: ' + str(energy) + '\n' + 'Sim: ' + str(avg_cos_sim)


@app.callback(Output('live-graph', 'figure'),
              events=[Event('interval-component', 'interval')])
# @app.callback(Output('live-graph', 'figure'),
#               [Input('interval-component', 'n_intervals')])
def update_graph_scatter():

    signals = myutils.preprocess_byte2(database.read_records(N), sample_rate)
    if signals.shape[0] == 0:
        return []
    print('plot:', signals.max())
    # print('plot', signals.shape)
    X = range(signals.shape[1] + 1)
    print("min", min(X))
    print("max", max(X))

    data1 = plotly.graph_objs.Scatter(
        x=list(X),
        y=list(signals[0]),
        name='Channel 1',
        mode='lines',
    )
    data2 = plotly.graph_objs.Scatter(
        x=list(X),
        y=list(signals[1]),
        name='Channel 2',
        mode='lines'
    )
    data3 = plotly.graph_objs.Scatter(
        x=list(X),
        y=list(signals[2]),
        name='Channel 3',
        mode='lines'
    )
    data4 = plotly.graph_objs.Scatter(
        x=list(X),
        y=list(signals[3]),
        name='Channel 4',
        mode='lines'
    )
    data5 = plotly.graph_objs.Scatter(
        x=list(X),
        y=list(signals[4]),
        name='Channel 5',
        mode='lines'
    )
    data6 = plotly.graph_objs.Scatter(
        x=list(X),
        y=list(signals[5]),
        name='Channel 6',
        mode='lines'
    )
    data7 = plotly.graph_objs.Scatter(
        x=list(X),
        y=list(signals[6]),
        name='Channel 7',
        mode='lines'
    )
    data8 = plotly.graph_objs.Scatter(
        x=list(X),
        y=list(signals[7]),
        name='Channel 8',
        mode='lines'
    )
    # data = [data1, data2, data3, data4, data5, data6, data7, data8]

    fig = tools.make_subplots(rows=4, cols=2)
    fig.append_trace(data1, 1, 1)
    fig.append_trace(data2, 1, 2)
    fig.append_trace(data3, 2, 1)
    fig.append_trace(data4, 2, 2)
    fig.append_trace(data5, 3, 1)
    fig.append_trace(data6, 3, 2)
    fig.append_trace(data7, 4, 1)
    fig.append_trace(data8, 4, 2)

    fig['layout']['xaxis1'].update(range=[min(X), max(X)])
    fig['layout']['yaxis1'].update(range=[-1, 1])
    fig['layout']['xaxis2'].update(range=[min(X), max(X)])
    fig['layout']['yaxis2'].update(range=[-1, 1])
    fig['layout']['xaxis3'].update(range=[min(X), max(X)])
    fig['layout']['yaxis3'].update(range=[-1, 1])
    fig['layout']['xaxis4'].update(range=[min(X), max(X)])
    fig['layout']['yaxis4'].update(range=[-1, 1])
    fig['layout']['xaxis5'].update(range=[min(X), max(X)])
    fig['layout']['yaxis5'].update(range=[-1, 1])
    fig['layout']['xaxis6'].update(range=[min(X), max(X)])
    fig['layout']['yaxis6'].update(range=[-1, 1])
    fig['layout']['xaxis7'].update(range=[min(X), max(X)])
    fig['layout']['yaxis7'].update(range=[-1, 1])
    fig['layout']['xaxis8'].update(range=[min(X), max(X)])
    fig['layout']['yaxis8'].update(range=[-1, 1])


    fig['layout'].update(title='Acoustic Data')
    # fig['layout'].update(height=600, width=600, title='Multiple Channels')

    return fig



if __name__ == '__main__':
    app.run_server(debug=False)