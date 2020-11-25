import os

import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State

import pandas as pd
import elasticsearch as es
import pandasticsearch as pdsh



def es_data():
    url = os.getenv('ELASTICSEARCH_URL')
    index = 'mb'
    db = es.Elasticsearch(
        url
    )   
    table = db.search(index='mb')
    return table


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

def uperf_df():
    # status_dict = dict(
    #     failure='danger',
    #     success='success',
    #     unstable='warning',
    #     primary='primary',
    #     default='default'
    # )
    # df0 = dummy_data()
    # data = df0.to_dict()

    uperf_res = pd.DataFrame.from_records(
        data = (
            (1024, 1, 4943.97),
            (1024, 2, 4913.15),
            (1024, 4, 2500.6)
        ),
        columns=['message size', 'pairs', 'tcp throughput']
    )
    return uperf_res


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


# collapse0 = html.Div(
#     [
#         dbc.Button(
#             "Open collapse",
#             id="collapse-button",
#             className="mb-3",
#             color="primary",
#         ),
#         dbc.Collapse(
#             dbc.Card(dbc.CardBody("This content is hidden in the collapse")),
#             id="collapse",
#         ),
#     ]
# )

# @app.callback(
#     Output("collapse", "is_open"),
#     [Input("collapse-button", "n_clicks")],
#     [State("collapse", "is_open")],
# )
# def toggle_collapse(n, is_open):
#     if n:
#         return not is_open
#     return is_open


# def make_toggle(label, color):
#     return dbc.Card([
#         dbc.Button(label, id=f"collapse-{label}", className="mb-3", color=color), 
#         dbc.Collapse(generate_table(uperf_df()), id=f"collapse-{toggle}")
#     ])


def make_item(i, label, color):
    # we use this function to make the example items to avoid code duplication
    return dbc.Card(
        [
            dbc.CardHeader(
                html.H2(
                    dbc.Button(
                        label,
                        color=color,
                        id=f"group-{i}-toggle",
                    )
                )
            ),
            dbc.Collapse(
                dbc.CardBody(generate_table(uperf_df())),
                id=f"collapse-{i}",
            ),
        ]
    )


status = {
    'aws':'danger',
    'aws future': 'success',
    'aws next':'warning',
    'aws ovn next':'success',
    'azure':'danger',
    'gcp':'danger'
}


accordion = html.Div(
    [make_item(i+1,item[0],item[1]) for i,item in enumerate(status.items())], className="accordion"
)




@app.callback(
    [Output(f"collapse-{i}", "is_open") for i in range(1, len(status.values())+1)],
    [Input(f"group-{i}-toggle", "n_clicks") for i in range(1, len(status.values())+1)],
    [State(f"collapse-{i}", "is_open") for i in range(1, len(status.values())+1)],
)
def toggle_accordion(n1, n2, n3, n4,n5, n6, 
    is_open1, is_open2, is_open3, is_open4, is_open5, is_open6):
    ctx = dash.callback_context

    if not ctx.triggered:
        return False, False, False, False, False, False
    else:
        print(ctx.triggered[0]["prop_id"])
        button_id = ctx.triggered[0]["prop_id"].split(".")[0]

    if button_id == "group-1-toggle" and n1:
        return not is_open1, False, False, False, False, False
    elif button_id == "group-2-toggle" and n2:
        return False, not is_open2, False, False, False, False
    elif button_id == "group-3-toggle" and n3:
        return False, False, not is_open3, False, False, False
    elif button_id == "group-4-toggle" and n4:
        return False, False, False, not is_open4, False, False
    elif button_id == "group-5-toggle" and n5:
        return False, False, False, False, not is_open5, False
    elif button_id == "group-6-toggle" and n6:
        return False, False, False, False, False, not is_open6
    return False, False, False, False, False, False











app.layout = html.Div(children=[
    html.H1(children='Hello Performance Pipelines'),
    html.Div(children='''
        Dash: A web application framework for PSE
    '''),
    # collapse0,
    accordion,
    # clouds,
    # generate_table(uperf_df())
])




if __name__ == '__main__':
    app.run_server(debug=True)
