import os

import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State

import pandas as pd
import elasticsearch as es


uperf_res = pd.DataFrame.from_records(
        data = (
            (1024, 1, 4943.97),
            (1024, 2, 4913.15),
            (1024, 4, 2500.6)
        ),
        columns=['message size', 'pairs', 'tcp throughput']
    )


def dummy_data():
    return pd.DataFrame.from_records(
        data=(
            ('aws', 'danger'),
            ('aws future', 'success'),
            ('aws next', 'warning'),
            ('aws ovn next', 'success'),
            ('azure', 'danger'),
            ('gcp', 'danger')
        ),
        columns=['pipeline', 'status']
    )


def generate_table(df, max_rows=10):
    return html.Table([
        html.Thead(
            html.Tr([html.Th(col) for col in df.columns])
        ),
        html.Tbody([
            html.Tr([
                html.Td(df.iloc[i][col]) for col in df.columns
            ]) for i in range(min(len(df), max_rows))
        ])
    ])





app = dash.Dash(__name__, 
    external_stylesheets=[dbc.themes.BOOTSTRAP])


# clouds = [
#     'aws',
#     'aws future',
#     'aws next',
#     'aws ovn next',
#     'azure',
#     'gcp'
# ]



def make_item(i, label, color):
    # we use this function to make the example items to avoid code duplication
    return dbc.Card(
        [
            dbc.CardHeader(
                html.H2(
                    dbc.Button(
                        label,
                        color=color,
                        id=f"group-{i}",
                    )
                )
            ),
            dbc.CardBody(
                generate_table(uperf_res),
                id=f"card-{i}",
            ),
        ]
    )


status = {
    'uperf':'success',
    'fio': 'danger',
    'pgbench':'warning',
    'vegeta':'success',
    'kube-burner':'danger',
}


aws_card = dbc.Card(
    dbc.CardBody(
        [html.H4('aws', className='card-title')]
    )
)


uperf_card = dbc.Card([
        dbc.CardHeader('uperf'),
    dbc.CardBody(
        [
            html.H4('uperf', className='card-title'),
            generate_table(uperf_res)
        ]
    )
],
color = 'success'
)

fio_card = dbc.Card([
        dbc.CardHeader('fio'),
    dbc.CardBody(
        [
            html.H4('uperf', className='card-title'),
            generate_table(uperf_res)
        ]
    )
],
color = 'danger'
)

vegeta_card = dbc.Card([
    dbc.CardHeader('vegeta'),
    dbc.CardBody(
        [
            html.H4('vegeta', className='card-title'),
            generate_table(uperf_res)
        ]
    ),
],
color = 'warning'
)




# clouds = html.Div([
#     dbc.Row(
#         [make_item(i+1,item[0],item[1]) for i,item in enumerate(status.items())] 
#     )
# ])


table = dbc.Table.from_dataframe(uperf_res, striped=True, bordered=True, hover=True)


aws_row = html.Div([
    dbc.Row(
        [aws_card, uperf_card, fio_card, vegeta_card] 
    )
])



app.layout = html.Div(children=[
    html.H1(children='Performance and Scale'),
    html.Div(children='''
        Dash: A web application framework for PSE
    '''),
    aws_row
])




if __name__ == '__main__':
    app.run_server(debug=True)
