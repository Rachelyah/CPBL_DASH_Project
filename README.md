## 中華職棒投手資料查詢網頁

### 一、專題組員：葉俐彤 Rachel Yeh

### 二、專案目的：

     - 提供關注中華職棒的使用者，透過網頁快速查詢各投手數據
     - 透過Dash將數據資料圖表視覺畫呈現，讓投手成績更一目了然

### 三、程式集：
    - 程式集：
        1.  main.py（Dash網址的註冊及設定）
        2.  cpbl_datasource.py (postgre資料庫連線及查詢、圖片顯示編碼轉換method)
        3.  cpbl_treeview.py (樹狀選單及進階數據圖表製作)
    
    - 使用軟體及套件關鍵字：Python、SQLite、TKinter、seaborn、matplotlib、pandas、Pillow


### 四、專案網址：
專案網址：[https://github.com/Rachelyah/CPBL_data_tkinter](https://github.com/Rachelyah/CPBL_data_tkinter)



### 五、使用說明：
    - 初始畫面：樹狀選單可快速瀏覽所有投手的名單及數據

![Alt text](README_img/1.start.png)

    - 點擊樹狀選單的選手，「球員資料」欄位顯示該球員相關數據

![Alt text](README_img/2.TreeView.png)

![Alt text](README_img/2-1.ALL_info.png)

![Alt text](README_img/3.player_info.png)

        1. 球員照片：可以看出球員加入球隊時是否開心

![Alt text](README_img/4.player_info_pic.png)

        2. 球員資料：所屬球隊、球員姓名、背號、投打習慣、身高體重、生日

![Alt text](README_img/5.player_data.png)

        3. 進階數據：有效局數、救援、中繼成功次數、被安打、全壘打數、保送數

![Alt text](README_img/6.player_data_IP.png)

        4. 奪三振率(K9)與防禦率(ERA)圖表：該投手當年度這兩項數據與聯盟總平均比較之圖表，藉此可看出當年度該投手這兩項重要指標是否優於聯盟大部分投手

![Alt text](README_img/7.player_K9_ERA.png)

    - 使用者亦可透過「選擇球隊」按鈕，選取指定球隊更新下方樹狀選單，找到指定球隊的球員


![Alt text](README_img/8.click_team.png)

![Alt text](README_img/9.TreeView_team_update.png)

### 六、資料來源：

- [cpbl-opendata-Idkrsi](https://github.com/ldkrsi/cpbl-opendata)：引用網友分享的過往統計數據csv檔(pitchings.csv)

- [中華職棒大聯盟全球資訊網 The Official Site of CPBL](https://www.cpbl.com.tw/)：透過爬蟲抓取球員的基本資料(投打習慣、身高體重、生日、背號、照片等資料)

