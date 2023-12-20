from dash import Dash, html, dash_table, callback, Input, Output, dcc, State
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import dash_bootstrap_components as dbc
from . import cpbl_datasource
import os
import base64
import matplotlib as plt


dash2 = Dash(requests_pathname_prefix="/dash/app2/", external_stylesheets=[dbc.themes.BOOTSTRAP])
dash2.title='中華職棒查詢'
current_data = cpbl_datasource.lastest_datetime_data()
#print(f'怪怪的{current_data}')

current_df = pd.DataFrame(current_data,
                          columns=['年份','所屬球隊', '球員編號', '球員姓名', '先發次數', '中繼次數', '勝場數', '敗場數', '三振數', '自責分'])

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
                        style_table={'height': '500px','width':'1200px', 'overflowY': 'auto','textOverflow': 'ellipsis', 'margin':'0'},
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
                html.Div([
                    html.Div([
                        html.Img(id='photo',className="",style={'width':'200px', 'height':'270px','margin': '0', 'padding':'0'}),
                        ],className="col"),
                    html.Div(
                        className="col",id='showMessage'),
                    html.Div(
                        html.Div(id='game',className="col")
                        ,style={'width':'200px', 'height':'270px','margin': '0', 'padding':'0','background-color':'blue'}),
                ],className="row",style={'margin': '20px', 'text-align':'center','background-color':'yellow'})],
            className="container text-center",style={'width':'1200px','margin-left': '0', 'text-align':'center',}),
            
            html.Div([
                dcc.Graph(id='info')],
                     className='in',
                    style={'color':'red'}),
                
            html.Div([
                dcc.Graph(id='game_pie'),
        
            ],
            className='in',
            style={'color':'red'}),
            

        ])
    ],
    className="container-lg"
    )

#按下查詢按鈕，啟動查詢＆回傳資料  
@callback(
    [Output('main_table','data'), Output('main_table', 'columns'), Output('main_table', 'selected_rows')],
    [Input('btn','n_clicks')],
    [State('input_value','value')],
)
def clickBtn(n_clicks:None | int, inputValue:str):
    global current_df
    if n_clicks is not None:
        print('clickbtn判斷')
        #print(inputValue)
        #呼叫datasource的搜尋方法，傳出list[tuple]
        searchData:list[tuple] = cpbl_datasource.search_sitename(inputValue)
        current_df = pd.DataFrame(searchData,columns=['年份', '所屬球隊', '球員編號', '球員姓名', '先發次數', '中繼次數', '勝場數', '敗場數', '三振數', '自責分'])
        #print(searchData)
        print('按確定')
        return current_df.to_dict('records'),[{'id':column,'name':column} for column in current_df],[]
    
    
    #當clickBtn is None -> 「確定」按鈕沒被按下，網頁剛啟動時
    else:
        print('第一次啟動')
        current_data = cpbl_datasource.lastest_datetime_data()
        current_df = pd.DataFrame(current_data,columns=['年份', '所屬球隊', '球員編號', '球員姓名',  '先發次數', '中繼次數', '勝場數', '敗場數', '三振數', '自責分'])
        #current_df = current_df.reset_index()

        return current_df.to_dict('records'), [{'id':column,'name':column} for column in current_df.columns],[]   


#============下方顯示球員資料欄位=================
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

            df_transposed = oneSite_df.transpose()
            df_display = pd.DataFrame({
            '球員資料': df_transposed.index,
            '內容': df_transposed.iloc[:, 0].values})

            oneTable:dash_table.DataTable = dash_table.DataTable(columns=[{'name': '球員資料', 'id': '球員資料'},
            {'name': '內容', 'id': '內容'}],
            data=df_display.to_dict('records'),
            style_table={'margin': 0,'height':'100%'},style_header={'fontWeight': 'bold'},
            style_cell_conditional=[
            {'if': {'column_id': '球員資料'}, 'width': '3%','height':'100%', 'text-align': 'center', 'font-weight': 'bold'},
            {'if': {'column_id': '內容'}, 'width': '3%','height':'100%', 'text-align': 'center'},])
            
            return oneTable
        
        return None

#===================點擊球員資料後顯示圓餅圖======================
@callback(
    Output('game_pie','figure'),
    Input('main_table','selected_rows')
)

#更新先發中繼圓餅圖
def game_pie(selected_rows:list[int]):
    global current_df
    if len(selected_rows) != 0:
        idSite:pd.DataFrame = current_df.iloc[[selected_rows[0]]]
        player_id = int(idSite['球員編號'].iloc[0])
        rows = cpbl_datasource.search_player_game_pie(player_id)
        
        games_df:pd.DataFrame = pd.DataFrame(rows,columns=['球員編號','所屬球隊','球員姓名', '出場數','先發次數','中繼次數','勝場數','敗場數','救援成功','中繼成功','有效局數','面對打者數','被安打數','被全壘打數','保送數','三振數','自責分','奪三振率','防禦率'])
        
        # 創建一個空的 DataFrame
        new_df = pd.DataFrame(columns=['出場類型', '出場數'])

        # 添加二維資料
        data = {'先發': [games_df['先發次數'].iloc[0]], '中繼': [games_df['中繼次數'].iloc[0]]}


        # 將二維資料轉換成 DataFrame 並添加到新的 DataFrame
        for category, values in data.items():
            category_df = pd.DataFrame({'出場類型': [category], '出場數': values})
            new_df = pd.concat([new_df, category_df], ignore_index=True)
        
        game_pie = px.pie(new_df, values='出場數', names='出場類型', title='先發&中繼佔比',hover_data=['出場數'])
       
        return game_pie
        



#更新圖表
@callback(
    Output('info', 'figure'),
    Input('main_table','selected_rows')
)

def update_bar(selected_rows:list[int]): #傳入list[裡面放int]
    fig = None
    global current_df
    #def可以取得py檔的文件變數
    if len(selected_rows) != 0:
        #宣告變數後面加上資料型別(type hint)
        idSite:pd.DataFrame = current_df.iloc[[selected_rows[0]]]
        player_id = int(idSite['球員編號'].iloc[0])
        print(f"Player ID: {player_id}")
            
        rows = cpbl_datasource.search_player_by_id(player_id)
        oneSite_df:pd.DataFrame = pd.DataFrame(rows,columns=['所屬球隊', '球員姓名', '背號', '投打習慣', '身高體重', '生日', '奪三振率', '防禦率'])
        

        #畫圖
        # 計算平均值
        k9_rea = cpbl_datasource.avg_k9_rea()
        k9_rea_df = pd.DataFrame(k9_rea,columns=['所屬球隊', '球員姓名', '背號', '投打習慣','身高體重', '生日','奪三振率','防禦率'])

        average_k9 = k9_rea_df['奪三振率'].mean()
        average_era = k9_rea_df['防禦率'].mean()

        # 建立長條圖
        fig = px.bar(oneSite_df,x='球員姓名',y=['奪三振率','防禦率'], barmode='group')

        # 加入第一條虛線表示平均值
        fig.add_shape(
            type='line',
            x0=-0.5,
            x1=len(oneSite_df) - 0.5,
            y0=average_k9,
            y1=average_k9,
            line=dict(color='red', dash='dash')
            )

            # 加入第二條虛線表示平均值
        fig.add_shape(
            type='line',
            x0=-0.5,
            x1=len(oneSite_df) - 0.5,
            y0=average_era,  # 設定第二條虛線的高度
            y1=average_era,  # 設定第二條虛線的高度
            line=dict(color='blue', dash='dash')
            )

            # 設定圖表佈局
        fig.update_layout(
            legend=dict(
            title='',  # 如果需要標題的話
            orientation='h',  # 水平方向的圖例
            yanchor='bottom',
            y=1.02,  # 調整圖例的垂直位置
            xanchor='right',
            x=1  # 調整圖例的水平位置
            ),
            title='奪三振率與防禦率',
            bargap=0.2,
            yaxis_range=[0,10])
                      
        print('fig已完成')
        return fig
        
    return fig

#顯示照片
@callback(
    Output('photo', 'src'),
    Input('main_table','selected_rows')
)

def update_photo(selected_rows:list[int]):
    global current_df
        #def可以取得py檔的文件變數
    if len(selected_rows) != 0:
              #宣告變數後面加上資料型別(type hint)
            print('update photo開始')
            idSite:pd.DataFrame = current_df.iloc[[selected_rows[0]]]
            player_id = int(idSite['球員編號'].iloc[0])
            #print(f"Player ID: {player_id}")
            
            rows = cpbl_datasource.search_player_by_id(player_id)
            print(f'順風:{rows}')
            print(f'資料型別:{type(rows)}')
            names = rows[0][1]
            print(f'姓名叫出{names}')
            # 設定圖片檔案的路徑
            imgfile = (f'/workspaces/CPBL_DASH_Project-1/dash_file/assets/img/{names}.jpg')

            # 讀取圖片檔案，轉換成 base64 編碼
            with open(imgfile, "rb") as image_file:
                img_data = base64.b64encode(image_file.read())
                img_data = img_data.decode()
                img_data = "{}{}".format("data:image/jpg;base64, ", img_data)

            print('照片好了')
        
            return img_data