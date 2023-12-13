from dash import Dash, html, dash_table, callback, Input, Output, dcc, State
import pandas as pd
import dash_bootstrap_components as dbc
from . import datasource

current_data = datasource.lastest_datetime_data()
current_df = pd.DataFrame(current_data,columns=['站點名稱','更新時間','行政區','地址','總數','可借','可還'])
current__df = current_df.reset_index()
current__df['站點名稱'] = current__df['站點名稱'].map(lambda name:name[11:])

#建立一個Dash的實體，加入網址、style設定
dash2 = Dash(requests_pathname_prefix="/dash/app2/", external_stylesheets=[dbc.themes.BOOTSTRAP])
dash2.title='台北市'


#dash.html的layout，不適合複雜的html結構
dash2.layout = html.Div(
    [
        dbc.Container([
            html.Div([
                html.Div([
                    html.H1("台北市youbike及時資料")
                ],className="col text-center")
            ],
            className="row",
            style={"paddingTop":'2rem'}),
            html.Div([
                html.Div([
                    html.Div([
                                dbc.Label("站點名稱"),
                                dbc.Input(
                                placeholder="請輸入站點名稱", 
                                type="text",
                                id='input_value'),                                
                    ])
        
                ],className="col"),
                html.Div([
                    html.Button('確定', 
                                id='submit-val',
                                className="btn btn-primary",)
                        ],className="col"),
            ],
            className="row row-cols-auto align-items-end",
            style={"paddingTop":'2rem'}),
            html.Div([
                html.Div([
                    dash_table.DataTable(
                        id='main_table',
                        #data=lastest_df1.to_dict('records'),
                        #columns=[{'id':column,'name':column} for column in lastest_df1.columns],
                        page_size=20,
                        style_table={'height': '300px', 'overflowY': 'auto'},
                        fixed_rows={'headers': True},
                        style_cell_conditional=[
                                {   'if': {'column_id': 'index'},
                                 'width': '5%'
                                },
                                {   'if': {'column_id': '站點名稱'},
                                 'width': '25%'},
                                {   'if': {'column_id': '總數'},
                                 'width': '5%'},
                                {   'if': {'column_id': '可借'},
                                 'width': '5%'},
                                {   'if': {'column_id': '可還'},
                                 'width': '5%'},
                        ],
                        row_selectable="single", #新增可點選的欄位，推定一次點一個欄位
                        selected_rows=[]         #預設一開始不要點選，要的話可以在[]中新增預設索引值
                    ),
                ],className="col text-center")
            ],
            className="row",
            style={"paddingTop":'0.5rem'}),
            html.Div([
                html.Div(children="",className="col",id='showMessage')
            ],
            className="row",
            style={"paddingTop":'2rem'})

        ])
    ],
    className="container-lg"
    )

#回傳查詢的確定按鈕被按了幾次
@callback(
    [Output('main_table','data'), Output('main_table', 'column'), Output('main_table', 'selected_rows')],
    [Input('submit-val','n_clicks')],
    [State('input_value','value')]
)
def clickBtn(n_clicks:None | int, inputValue:str):
    global current__df
    if n_clicks is not None:
        #呼叫datasource的搜尋方法，傳出list[tuple]
        searchData:list[tuple] = datasource.search_sitename(inputValue)
        current__df = pd.DataFrame(searchData,columns=['站點名稱','更新時間','行政區','地址','總數','可借','可還'])
        print(searchData)
        current__df = current__df.reset_index()
        current__df['站點名稱'] = current__df['站點名稱'].map(lambda name:name[11:])
        print('按確定')
        return current__df.to_dict('records'),[{'id':column,'name':column} for column in current__df],[]
    
    
    #當clickBtn is None -> 「確定」按鈕沒被按下，網頁剛啟動時
    print('第一次啟動')
    current_data = datasource.lastest_datetime_data()
    current_df = pd.DataFrame(current_data,columns=['站點名稱','更新時間','行政區','地址','總數','可借','可還'])
    current__df = current_df.reset_index()
    current__df['站點名稱'] = current__df['站點名稱'].map(lambda name:name[11:])

    return current__df.to_dict('records'), [{'id':column,'name':column} for column in current__df.columns],[]   


@callback(
    Output('showMessage','children'),
    Input('main_table','selected_rows')
)

#抓出選擇的欄位內容
def selectedRow(selected_rows:list[int]): #傳入list[裡面放int]
        #取得一個站點，series
        #def可以取得py檔的文件變數
        if len(selected_rows) != 0:
              #宣告變數後面加上資料型別(type hint)
              oneSite:pd.DataFrame = current__df.iloc[[selected_rows[0]]]
              oneTable:dash_table.DataTable = dash_table.DataTable(oneSite.to_dict('records'), [{"name": i, "id": i} for i in oneSite.columns])

              return oneTable
        
        return None