from dash import Dash, html, dash_table, callback, Input, Output, dcc, State
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import dash_bootstrap_components as dbc
from . import cpbl_datasource
import dash
import base64
import os

index = Dash(requests_pathname_prefix="/dash/index/", external_stylesheets=[dbc.themes.BOOTSTRAP])

#連結外部css檔
external_stylesheets=['assets/header.css']

index.title='中華職棒查詢'

#layout
index.layout = html.Div([
    dbc.Container([
            html.Div([
                html.Div([
                    html.H1("測試頁面")
                ],className="col text-center")
]),])])