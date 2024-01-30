from dash import Dash, html, dcc, callback, Output, Input
import dash_bootstrap_components as dbc

import plotly.express as px
import plotly.graph_objects as go

import pandas as pd
import numpy as np
import json

# df = pd.read_csv("HIST_PAINEL_COVIDBR_2023_Parte1_08dez2023.csv",sep=";")
# df_states = df[(~df["estado"].isna()) & (df["codmun"].isna())]
# df_brasil = df[df["regiao"] == "Brasil"]
# df_states.to_csv("df_states.csv")
# df_brasil.to_csv("df_brasil.csv")

df_states = pd.read_csv("df_states.csv")
df_brasil = pd.read_csv("df_brasil.csv")
df_states_ = df_states [df_states ["data"] == "2023-01-01"] 

brazil_states = json.load(open("Dashboard COVID-19/geojson/brazil_geo.json","r"))
df_data = df_states[df_states["estado"]=="PE"]
selection_columns = {"casosAcumulado": "Casos acumulados",
                     "casosNovos": "Casos Novos",
                     "obitosAcumulado":"Obitos Totais",
                     "obitosNovos":"Obitos Por dia "
                     }


app = Dash(__name__, external_stylesheets=[dbc.themes.VAPOR])

fig= px.choropleth_mapbox(df_states_, locations="estado", color="casosNovos",
                          center={"lat":-11.60,"lon":-47.19}, zoom=4,
                          geojson=brazil_states, color_continuous_scale="Reds", opacity=0.5,
                          hover_data={"casosNovos":True, "obitosNovos":True, "estado":True})

fig.update_layout(
    paper_bgcolor="#9370DB",
    autosize=True,
    margin=go.layout.Margin(l=0, r=0, b=0, t=0),
    showlegend=False,
    mapbox_style="carto-positron"
)

fig2= go.Figure(layout={"template":"plotly_dark"})
fig2.add_trace(go.Scatter(x=df_data["data"],y=df_data["casosAcumulado"]))
fig2.update_layout(
    paper_bgcolor="#9370DB",
    plot_bgcolor= "#9370DB",
    autosize= True,
    margin=dict(l=10,r=10,t=10, b=10)

)

app.layout= dbc.Container(
    dbc.Row([
       dbc.Col([ 
            html.Div([
                html.H2("Dashboard Covid"),
                dbc.Button("BRASIL", color="primary",id="location-button", size="lg")
            ],style={}),
            html.P("imforme a data na qual deseja obter informações:",style={"margin-top": "40px"}),
            html.Div(id="div-test", children=[
                dcc.DatePickerSingle(
                    id="date-picker",
                    min_date_allowed = df_brasil["data"].min(),
                    max_date_allowed = df_brasil["data"].max(),
                    initial_visible_month=df_brasil["data"].min(),
                    date=df_brasil["data"].max(),
                    display_format="MMMM D, YYYY",
                    style={
                        "width":"100%",
                        "border":"0px solid black",
                        "padding":"3px"
                    }
                )
            ]),
            dbc.Row([
             dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.Span("Casos recuperados"),
                        html.H3(style={"color":"#F704F7"},id="casos-recuperados=text"),
                        html.Span("Recuperados data"),
                        html.H5(style={"color":"#5C04F7"},id="casos-recuperados-data=text")

                    ])
                ], color="light", outline=True, style={
                                                "box-shadow":"2 6px 6px 0 rgba(0, 0, 0, 0.15), 0 4px 20px 0 rgba(0, 0, 0, 0.19)",
                                                "color":"#140254"})
                ], md=6),
             dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.Span("Obitos confirmados "),
                        html.H3(style={"color":"#F704F7"},id="obitos-confirmados=text"),
                        html.Span("obitos data"),
                        html.H3(style={"color":"#5C04F7"},id="obitos-confirmando-data=text")

                    ])
                ], color="danger", outline=True, style={"box-shadow":"2 6px 6px 0 rgba(0, 0, 0, 0.15), 0 4px 20px 0 rgba(0, 0, 0, 0.19)",
                                                         "color":"#140254"})
                ], md=6)
        ]),html.Div([
            html.P("selecione o tipo de dado:",style={"margin-top": "40px"}),
            dcc.Dropdown(id = "location-dropdown",
                         options= [{"label": j, "value": i} for i, j in selection_columns.items()],
                         value= "casosNovos",
                         style= {"margin-top":"10px"}
                         ),
            dcc.Graph(id='line-map',figure=fig2)
            
             ]),
        ],md=5, style={"padding":"20px", "blackground-color":"#9400D3"}),
        
        dbc.Col([
            dcc.Graph(id='choropleth-map',figure=fig)
        ],md=7)
    ]
    
    )
,fluid=True)

if __name__ == "__main__":
    app.run_server(debug=True)