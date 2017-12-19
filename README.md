# town368 REST API 
本 API 蒐集 2017.9.4. 以後臺灣 368 個鄉鎮天氣預報歷史資料
- [API root endpoint](https://town368.csie.ntu.edu.tw)
- [document](https://wyde.github.io/town368)

## 技術棧
- interactive shell：jupyter notebook
- 爬蟲：requests
- 資料清理：pandas
- 資料管線：SQLAlchemy + MySQL
- API：Django REST Framework + MySQL
- 佈署：Nginx + Gunicorn

## 環境
- 開發：Cloud9 (Ubuntu14.04 Container)
- 生產：CentOS 7

## 開發方向
- db 換成 PostgresSQL
- 測試把 Django 的 ORM 換成 SQLAlchemy 的好處
- 優化爬蟲的寫法
- 用 container 開發、佈署
- 寫 test case

## 未來我們會試圖符合以下規範：
- 民104.7 國發會 [共通性資料存取應用程式介面(API)規範](http://file.data.gov.tw/opendatafile/%E5%85%B1%E9%80%9A%E6%80%A7%E8%B3%87%E6%96%99%E5%AD%98%E5%8F%96%E6%87%89%E7%94%A8%E7%A8%8B%E5%BC%8F%E4%BB%8B%E9%9D%A2API%E8%A6%8F%E7%AF%84.pdf)
- 民104.7 國發會 [資料集詮釋資料標準規範](http://file.data.gov.tw/opendatafile/%E8%B3%87%E6%96%99%E9%9B%86%E8%A9%AE%E9%87%8B%E8%B3%87%E6%96%99%E6%A8%99%E6%BA%96%E8%A6%8F%E7%AF%84.pdf)

## 安裝
- 設定 virtualenv ， pip install 開發 / 佈署對應的 requirements/env.txt
- sudo apt-get or yum install 開發 / 佈署對應的 pkglist
- 安裝 MySQL 5.7
- 寫專案根目錄下的 ./config/default.py 範例 ./config/default.py.example

## Changelog
- 1.1.20171219
