from dash import Dash, html, dash_table, callback, Input, Output, dcc, State
import pandas as pd
import dash_bootstrap_components as dbc
from . import cpbl_datasource

dash3 = Dash(requests_pathname_prefix="/dash/app3/", external_stylesheets=[dbc.themes.BOOTSTRAP])
dash3.title='中華職棒查詢dash3'

current_data = cpbl_datasource.lastest_datetime_data()

current_df = pd.DataFrame(current_data,
                          columns=['年份', '所屬球隊', '球員編號', '球員姓名', '出場數', '先發次數', '中繼次數', '勝場數', '敗場數', '救援成功', '中繼成功', '有效局數', '面對打者數', '被安打數', '被全壘打數', '保送數', '三振數', '自責分', '投打習慣', '背號', '身高體重', '生日', '照片網址', '奪三振率', '防禦率'])


#layout
dash3.layout = html.Div(
    [
        dbc.Container([
            html.Div([
                html.Div([
                    html.H1("中華職棒查詢dash3")
                ],className="col text-center")
            ],
            className="row",
            style={"paddingTop":'2rem'}),
            #搜尋功能
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
                        data=current_df.to_dict('records'),
                        columns=[{'id': column, 'name': column} for column in current_df.columns],
                        page_size=20,
                        style_table={'height': '300px', 'overflowY': 'auto'},
                        fixed_rows={'headers': True},
                        style_cell_conditional=[
                                {   'if': {'column_id': '年份'},
                                 'width': '25%'},
                                {   'if': {'column_id': '所屬球隊'},
                                 'width': '5%'},
                                {   'if': {'column_id': '球員編號'},
                                 'width': '5%'},
                                {   'if': {'column_id': '球員姓名'},
                                 'width': '5%'},
                                {   'if': {'column_id': '出場數'},
                                 'width': '5%'},
                                {   'if': {'column_id': '先發次數'},
                                 'width': '5%'},
                                {   'if': {'column_id': '中繼次數'},
                                 'width': '5%'},
                                {   'if': {'column_id': '勝場數'},
                                 'width': '5%'},
                                {   'if': {'column_id': '敗場數'},
                                 'width': '5%'},
                                {   'if': {'column_id': '救援成功'},
                                 'width': '5%'},
                                {   'if': {'column_id': '中繼成功'},
                                 'width': '5%'},
                                {   'if': {'column_id': '有效局數'},
                                 'width': '5%'},
                                {   'if': {'column_id': '面對打者數'},
                                 'width': '5%'},
                                {   'if': {'column_id': '被安打數'},
                                 'width': '5%'},
                                {   'if': {'column_id': '球員姓名'},
                                 'width': '5%'},
                                {   'if': {'column_id': '被全壘打數'},
                                 'width': '5%'},
                                {   'if': {'column_id': '保送數'},
                                 'width': '5%'},
                                {   'if': {'column_id': '三振數'},
                                 'width': '5%'},
                                {   'if': {'column_id': '自責分'},
                                 'width': '5%'},
                                {   'if': {'column_id': '投打習慣'},
                                 'width': '5%'},
                                {   'if': {'column_id': '背號'},
                                 'width': '5%'},
                                {   'if': {'column_id': '身高'},
                                 'width': '5%'},
                                {   'if': {'column_id': '體重'},
                                 'width': '5%'},
                                {   'if': {'column_id': '生日'},
                                 'width': '5%'},
                                {   'if': {'column_id': '照片網址'},
                                 'width': '5%'},
                                {   'if': {'column_id': '奪三振率'},
                                 'width': '5%'},
                                {   'if': {'column_id': '防禦率'},
                                 'width': '5%'},
                        ],
                        row_selectable="single", 
                        selected_rows=[] 
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
    [Output('main_table','data'),Output('main_table', 'column')],
    [Input('submit-val','n_clicks')],
    [State('input_value','value')]
)
def clickBtn(n_clicks:None | int, inputValue:str):
    global current_df
    if n_clicks is not None:
        print('clickbtn判斷')
        #呼叫datasource的搜尋方法，傳出list[tuple]
        searchData:list[tuple] = cpbl_datasource.search_sitename(inputValue)
        current_df = pd.DataFrame(searchData,columns=['年份', '所屬球隊', '球員編號', '球員姓名', '出場數', '先發次數', '中繼次數', '勝場數', '敗場數', '救援成功', '中繼成功', '有效局數', '面對打者數', '被安打數', '被全壘打數', '保送數', '三振數', '自責分', '投打習慣', '背號', '身高體重', '生日', '照片網址', '奪三振率', '防禦率'])
        print(searchData)
        #current_df = current_df.reset_index()
        #'] = current_df['站點名稱'].map(lambda name:name[11:])
        print('按確定')
        return current_df.to_dict('records'),[{'id':column,'name':column} for column in current_df]
    
    
    #當clickBtn is None -> 「確定」按鈕沒被按下，網頁剛啟動時
    
    print('第一次啟動')
    current_data = cpbl_datasource.lastest_datetime_data()
    current_df = pd.DataFrame(current_data,columns=['年份', '所屬球隊', '球員編號', '球員姓名', '出場數', '先發次數', '中繼次數', '勝場數', '敗場數', '救援成功', '中繼成功', '有效局數', '面對打者數', '被安打數', '被全壘打數', '保送數', '三振數', '自責分', '投打習慣', '背號', '身高體重', '生日', '照片網址', '奪三振率', '防禦率'])

    return current_df.to_dict('records'), [{'id': column, 'name': column} for column in current_df.columns]


@callback(
    Output('showMessage','children'),
    Input('main_table','selected_rows')
)

#抓出選擇的欄位內容
def selectedRow(selected_rows:list[int]): #傳入list[裡面放int]
        global current_df
        #取得一個站點，series
        #def可以取得py檔的文件變數
        if len(selected_rows) != 0:
              #宣告變數後面加上資料型別(type hint)
              oneSite:pd.DataFrame = current_df.iloc[[selected_rows[0]]]
              oneTable:dash_table.DataTable = dash_table.DataTable(oneSite.to_dict('records'), [{'id': column, 'name': column} for column in current_df.columns])

              return oneTable
        
        return None