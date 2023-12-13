import requests
import psycopg2
#from . import render_password as rpw
#import render_password as rpw
import socket
import os

myip = socket.gethostbyname(socket.gethostname())

if '172.17.0.2' <= myip <= '172.17.255.255':
    print(f'本機{myip}')
    from . import render_password as rpw
    DATABASE=rpw.DATABASE
    USER=rpw.USER
    PASSWORD=rpw.PASSWORD
    HOST=rpw.HOST


else:
    print(f'server{myip}')
    DATABASE=os.environ['DATABASE']
    USER=os.environ['USER']
    PASSWORD=os.environ['PASSWORD'] 
    HOST=os.environ['HOST']

#從資料庫中呼叫最新的資料
def lastest_datetime_data()->list[tuple]: 
    conn = psycopg2.connect(database=DATABASE, 
                                user=USER, 
                                password=PASSWORD, 
                                host=HOST, 
                                port="5432")   
    cursor = conn.cursor() 
    #匯入SQL語法：抓出1322個站點最新資料（待更新）
    sql = '''
    select a.站點名稱, a.更新時間, a.行政區, a.地址, a.總車輛數, a.可借, a.可還 from 台北市youbike as a 
    join (select distinct 站點名稱,max(更新時間) 更新時間 from 台北市youbike group by 站點名稱) as b
    on a.更新時間=b.更新時間 and a.站點名稱=b.站點名稱
    '''
    cursor.execute(sql) #執行SQL
    rows = cursor.fetchall()
    cursor.close()
    conn.close()

    return rows

#查詢第一個關鍵字
#SQL內的要查詢的資訊先寫問號
def search_sitename(word:str) ->list[tuple]:
    conn = psycopg2.connect(database=DATABASE,
                            user=USER, 
                            password=PASSWORD, 
                            host=HOST, 
                            port="5432")    
    cursor = conn.cursor() 
    sql = '''
    select 站點名稱, 更新時間, 行政區, 地址, 總車輛數, 可借, 可還
    from  台北市youbike
    where (更新時間, 站點名稱) in(
	select max(更新時間), 站點名稱
	from 台北市youbike
	group by 站點名稱
	) and 站點名稱 like %s
    '''
    cursor.execute(sql,[f'%{word}%'])
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    return rows