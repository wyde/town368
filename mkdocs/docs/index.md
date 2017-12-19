# town368 開放環境 API

這是一個練手的 side project ，爬取了全台灣 368 鄉鎮市區級的**未來 72 小時內逐 3 小時**的氣象預報，還在開發中，歡迎指點或 PR
<br><br>
未來預計新增一些鄉鎮市區級的開放資料與圖資，建立微型氣候的預測模型，以作為台灣民眾戶外活動的參考

- [從架構到文件的原始碼 on Github](https://github.com/wyde/town368)
- [開發筆記](https://wyde.github.io/2017/09/18/Crawler-RESTful-API-Data-Visualization/)
- 前端應用小 demo 
    - [台大戶外球場可以打球嗎？](http://dadacho.com)
    - (有作品想放在這可以 mail 我)

## Overview

在 v1.0 版的 API ，我們將會爬取全台灣 368 鄉鎮與[資料來源(如下圖)](http://www.cwb.gov.tw/V7/forecast/town368/towns/6300300.htm)雷同的氣象預報，輸入 db ，建立可以 json format 存取的 RESTful API
![](https://i.imgur.com/NVrKo2G.png)

政府開放資料有類似的資料，不過沒有歷史資料及 RESTful API 可供使用

- [鄉鎮天氣預報-台灣未來2天天氣預報](https://data.gov.tw/dataset/9307)
- [鄉鎮天氣預報-全臺灣各鄉鎮市區預報資料](https://data.gov.tw/dataset/9309)

town368 API 目前提供兩則 API 及不同查詢參數供使用

- Reports 提供自 2017.9.4. 起的逐三小時鄉鎮市區級的氣象預報
- Stations 提供行政區劃與主計處舊制的村里代碼之間的對應

## API Schema 

### Root Endpoint

    https://town368.csie.ntu.edu.tw

### Reports

- URL

    `/v1.0/reports/[rid]` - 抓取第 [record id] 條紀錄 

- Method
    
    `GET`

- Success Response

    - Code: 200 <br>
    - Content: <br> `{"rid":1000,"station_sid":1000507,"update_t":"2017-09-04T00:30:23Z","record_t":"2017-09-04T03:00:00Z","weekday":"一","wx":"多雲","t":25,"at":28,"beaufort":"<=1","wind_dir":"東南風","rh":"86%","pop":"10%","ci":"舒適"}`
    
- Sample Call:

```
    $.ajax({
        type: 'GET',
        url: 'https://town368.csie.ntu.edu.tw/v1.0/reports/1000',
        dataType: 'json',
        success: function(json) {
            console.log(json)
        }
    });
```

---
 
- URL

    `/v1.0/reports`

- Method
    
    `GET`

- URL Params

    `?limit=500&offset=[500*n]` - n 為正整數，每 500 條紀錄換頁

- Success Response

    - Code: 200 <br>
    - Content:<br> `{"count":57974,"next":"http://town368.csie.ntu.edu.tw/v1.0/reports?limit=1500&offset=1500","previous":null,"results":[{"rid":1,"station_sid":6300100,"update_t":"2017-08-31T02:37:16Z","record_t":"2017-08-31T03:00:00Z","weekday":"四","wx":"短暫陣雨","t":28,"at":31,"beaufort":"2","wind_dir":"偏東風","rh":"93%","pop":"30%","ci":"悶熱"},...],}`

---
 
- URL

    `/v1.0/reports`

- Method
    
    `GET`

- URL Params

    - `?station_sid=6300300` - 可查詢大安區的氣象資料<br>
    - `?record_t=2017-09-21T09:00:00Z` - 可查詢 2017.9.21 的氣象資料，採用 ISO 8601 時間格式，每三小時紀錄一次 (00, 03, 06...)
    - `?station_sid=6300300&record_t=2017-09-21T09:00:00Z` - 結合上述 params ，此 api 可查詢 2017.9.21. 早上 9-12 間的氣象資料

- Success Response

    - Code: 200 <br>
    - Content:<br> `{"count":1,"next":null,"previous":null,"results":[{"rid":51375,"station_sid":6300300,"update_t":"2017-09-21T05:36:51Z","record_t":"2017-09-21T09:00:00Z","weekday":"四","wx":"晴天","t":31,"at":34,"beaufort":"2","wind_dir":"西北風","rh":"60%","pop":"0%","ci":"悶熱"}]}`

- Note

    - 查詢時間如果超過現在時間，且在未來 72 小時內，則為預測資料
    - 查詢時間若是現在或過去時間，且在 2017.9.4. 之後，則為歷史資料

---

### Stations

- URL

    `/v1.0/stations`

- Method

    `GET`

- URL Params

    - `?city=台北市` - city 為台灣各直轄市、縣轄市
    - `?city=台北市&district=大安區` - 可進一步指定所屬鄉鎮市區級行政區 

- Success Response

    - Code: 200<br>
    - Content:<br> `{"count":12,"next":null,"previous":null,"results":[{"sid":6300100,"city":"台北市","district":"松山區"},{"sid":6300200,"city":"台北市","district":"信義區"},{"sid":6300300,"city":"台北市","district":"大安區"},{"sid":6300400,"city":"台北市","district":"中山區"},{"sid":6300500,"city":"台北市","district":"中正區"},{"sid":6300600,"city":"台北市","district":"大同區"},{"sid":6300700,"city":"台北市","district":"萬華區"},{"sid":6300800,"city":"台北市","district":"文山區"},{"sid":6300900,"city":"台北市","district":"南港區"},{"sid":6301000,"city":"台北市","district":"內湖區"},{"sid":6301100,"city":"台北市","district":"士林區"},{"sid":6301200,"city":"台北市","district":"北投區"}]}`


