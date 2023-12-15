from dash import Dash, html, dash_table, callback, Input, Output, dcc, State
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import dash_bootstrap_components as dbc
from . import cpbl_datasource
import os


dash2 = Dash(requests_pathname_prefix="/dash/app2/", external_stylesheets=[dbc.themes.BOOTSTRAP])
dash2.title='中華職棒查詢'
current_data = cpbl_datasource.lastest_datetime_data()

current_df = pd.DataFrame(current_data,
                          columns=['年份', '所屬球隊', '球員編號', '球員姓名', '出場數', '先發次數', '中繼次數', '勝場數', '敗場數', '三振數', '自責分'])

#layout
dash2.layout = html.Div(
    [
        dbc.Container([
            html.Div([
                html.Div([
                    html.H1("中華職棒查詢")
                ],className="col text-center")
            ],
            className="row",
            style={"paddingTop":'2rem'}),
            #搜尋功能
            html.Div([
                html.Div([
                    html.Div([
                                dbc.Label("球員查詢"),
                                dbc.Input(
                                placeholder="請輸入球員姓名", 
                                type="text",
                                id='input_value'),                                
                    ])
        
                ],className="col"),
                html.Div([
                    html.Button(children='查詢', 
                                id='btn',
                                className="btn btn-primary",)
                        ],className="col"),
            ],
            className="row row-cols-auto align-items-end",
            style={"paddingTop":'2rem'}),
            html.Div([
                html.Div([
                    dash_table.DataTable(
                        id='main_table',
                        page_size=10,
                        style_table={'height': '500px','width':'1200px', 'overflowY': 'auto','textOverflow': 'ellipsis'},
                        fixed_rows={'headers': True},
                        row_selectable='single',
                        selected_rows=[],
                        style_cell_conditional=[
                                {   'if': {'column': 'selected_rows'}, 'width': '1px'},
                                {   'if': {'column_id': '年份'},'width': '15%'},
                                {   'if': {'column_id': '所屬球隊'},'width': '15%'},
                                {   'if': {'column_id': '球員編號'},'width': '15%'},
                                {   'if': {'column_id': '球員姓名'},'width': '15%'},
                                {   'if': {'column_id': '出場數'},'width': '5%'},
                                {   'if': {'column_id': '先發次數'},'width': '5%'},
                                {   'if': {'column_id': '中繼次數'},'width': '5%'},
                                {   'if': {'column_id': '勝場數'},'width': '5%'},
                                {   'if': {'column_id': '敗場數'},'width': '5%'},
                                {   'if': {'column_id': '三振數'},'width': '5%'},
                                {   'if': {'column_id': '自責分'},'width': '5%'},

                        ],

                    ),
                ],className="col text-center")
            ],
            className="row",
            style={"paddingTop":'0.5rem'}),
            html.Div([
                html.Div(className="col",id='showMessage'),
            ],
            className="row",
            style={"paddingTop":'2rem'}),
            html.Div([
                dcc.Graph(id='info'),
            html.Div([
                html.H1("照片"),
            ])
            
            ],
            className='in',
            style={'color':'red'}
                     )
            

        ])
    ],
    className="container-lg"
    )

#回傳查詢的確定按鈕被按了幾次   
@callback(
    [Output('main_table','data'), Output('main_table', 'columns'), Output('main_table', 'selected_rows')],
    [Input('btn','n_clicks')],
    [State('input_value','value')],
)
def clickBtn(n_clicks:None | int, inputValue:str):
    global current_df
    print('clickbtn判斷')
    if n_clicks is not None:
        print('clickbtn判斷')
        #print(inputValue)
        #呼叫datasource的搜尋方法，傳出list[tuple]
        searchData:list[tuple] = cpbl_datasource.search_sitename(inputValue)
        current_df = pd.DataFrame(searchData,columns=['年份', '所屬球隊', '球員編號', '球員姓名', '出場數', '先發次數', '中繼次數', '勝場數', '敗場數', '三振數', '自責分'])
        #print(searchData)
        print('按確定')
        return current_df.to_dict('records'),[{'id':column,'name':column} for column in current_df],[]
    
    
    #當clickBtn is None -> 「確定」按鈕沒被按下，網頁剛啟動時
    else:
        print('第一次啟動')
        current_data = cpbl_datasource.lastest_datetime_data()
        current_df = pd.DataFrame(current_data,columns=['年份', '所屬球隊', '球員編號', '球員姓名', '出場數', '先發次數', '中繼次數', '勝場數', '敗場數', '三振數', '自責分'])
        #current_df = current_df.reset_index()

        return current_df.to_dict('records'), [{'id':column,'name':column} for column in current_df.columns],[]   


#==========下方顯示球員資料欄位=================
@callback(
    Output('showMessage','children'),
    Input('main_table','selected_rows')
)

#抓出選擇的欄位內容
def selectedRow(selected_rows:list[int]): #傳入list[裡面放int]
        global current_df
        #def可以取得py檔的文件變數
        if len(selected_rows) != 0:
              #宣告變數後面加上資料型別(type hint)
            idSite:pd.DataFrame = current_df.iloc[[selected_rows[0]]]
            player_id = int(idSite['球員編號'].iloc[0])
            rows = cpbl_datasource.search_player_by_id(player_id)
            print(f'回來了{rows}')
              
            oneSite_df:pd.DataFrame = pd.DataFrame(rows,columns=['所屬球隊', '球員姓名', '背號', '投打習慣', '身高體重', '生日', '奪三振率', '防禦率'])
              
            oneTable:dash_table.DataTable = dash_table.DataTable(oneSite_df.to_dict('records'), [{'id': column, 'name': column} for column in oneSite_df.columns])
            #print(oneSite_df)
            #print(oneTable)
            

            return oneTable
        
        return None


#更新圖表
@callback(
    Output('info', 'figure'),
    Input('main_table','selected_rows')
)

def update_bar(selected_rows:list[int]): #傳入list[裡面放int]
        global current_df
        #def可以取得py檔的文件變數
        if len(selected_rows) != 0:
              #宣告變數後面加上資料型別(type hint)
            idSite:pd.DataFrame = current_df.iloc[[selected_rows[0]]]
            player_id = int(idSite['球員編號'].iloc[0])
            print(f"Player ID: {player_id}")
            
            rows = cpbl_datasource.search_player_by_id(player_id)
            oneSite_df:pd.DataFrame = pd.DataFrame(rows,columns=['所屬球隊', '球員姓名', '背號', '投打習慣', '身高體重', '生日', '奪三振率', '防禦率'])
              
            fig = px.bar(
            idSite,
            x='球員姓名',
            y=['奪三振率', '防禦率'],
            barmode='group',
            title='奪三振率和防禦率')
            
            if fig is not None:
                return fig
        
        return px.bar()