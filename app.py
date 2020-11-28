import os

import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State

import pandas as pd
import elasticsearch as es


combos_df = pd.DataFrame.from_records(
    data = (
        ('4.6 nightly', 'aws'),
        ('4.6 nightly', 'aws future'),
        ('4.6 nightly', 'aws next'),
        ('4.6 nightly', 'aws ovn next'),
        ('4.6 nightly', 'azure'),
        ('4.6 nightly', 'gcp'),
        ('4.6 ovn nightly', 'aws'),
        ('4.6 ovn nightly', 'aws future'),
        ('4.6 ovn nightly', 'aws next'),
        ('4.6 ovn nightly', 'aws ovn next'),
        ('4.6 ovn nightly', 'azure'),
        ('4.6 ovn nightly', 'gcp'),
        ('4.7 nightly', 'aws'),
        ('4.7 nightly', 'aws future'),
        ('4.7 nightly', 'aws next'),
        ('4.7 nightly', 'aws ovn next'),
        ('4.7 nightly', 'azure'),
        ('4.7 nightly', 'gcp'),
        ('4.7 ovn nightly', 'aws'),
        ('4.7 ovn nightly', 'aws future'),
        ('4.7 ovn nightly', 'aws next'),
        ('4.7 ovn nightly', 'aws ovn next'),
        ('4.7 ovn nightly', 'azure'),
        ('4.7 ovn nightly', 'gcp'),
        ('4.8 nightly', 'aws'),
        ('4.8 nightly', 'aws future'),
        ('4.8 nightly', 'aws next'),
        ('4.8 nightly', 'aws ovn next'),
        ('4.8 nightly', 'azure'),
        ('4.8 nightly', 'gcp')
    ),
    columns = ['ocp version', 'cloud pipeline']
)


ocp_versions = [
    '4.6 nightly',
    '4.6 ovn nightly',
    '4.7 nightly',
    '4.7 ovn nightly',
    '4.8 nightly'
]

cloud_pipelines = [
    'aws',
    'aws future',
    'aws next',
    'aws ovn next',
    'azure',
    'gcp'
]


combos = combos_df.to_dict()


uperf_res = pd.DataFrame.from_records(
        data = (
            (1024, 1, 4943.97),
            (1024, 2, 4913.15),
            (1024, 4, 2500.6)
        ),
        columns=['message size', 'pairs', 'tcp throughput']
    )



app = dash.Dash(__name__, 
    external_stylesheets=[dbc.themes.BOOTSTRAP])


status = {
    'uperf':'success',
    'fio': 'danger',
    'pgbench':'warning',
    'vegeta':'success',
    'kube-burner':'danger',
}




def make_card(header, status, df):
    return dbc.Card([
        dbc.CardHeader(header),
        dbc.Card(
            [dbc.Table.from_dataframe(df, striped=True, bordered=True, hover=True)],
            color = status
        )
    ])


build_card = make_card('build', 'warning', uperf_res)
install_card = make_card('install', 'success', uperf_res)
uperf_card = make_card('uperf', 'success', uperf_res)
http_card = make_card('http test', 'danger', uperf_res)
kubelet_card = make_card('kubelet density', 'success', uperf_res)
objdens_card = make_card('object density', 'success', uperf_res)
upgrade_card = make_card('upgrade', 'success', uperf_res)


aws_card = dbc.Card(
    dbc.CardBody(
        [html.H4('aws', className='card-title')]
    )
)


aws_row = html.Div([
    dbc.Row(
        [aws_card, build_card, install_card, uperf_card,
        http_card,kubelet_card, objdens_card, upgrade_card
        ] 
    )
])





app.layout = html.Div(children=[
    html.H1(children='Performance and Scale'),
    html.Div(children='''
        Dash: A web application framework for PSE
    '''),
    dbc.ListGroup([dbc.ListGroupItem(item) for item in ocp_versions], horizontal=True, className="mb-2"),
    dbc.ListGroup([
        dbc.Card([
            dbc.CardHeader(ocp_versions[0]),
            dbc.ListGroupItem(aws_row)]),
        dbc.Card([
            dbc.CardHeader(ocp_versions[1]),
            dbc.ListGroupItem(aws_row)]),
    ]),
    # aws_row
])


if __name__ == '__main__':
    app.run_server(debug=True)
