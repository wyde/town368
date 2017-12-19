#!/home/wyde/.virtualenvs/town368-3hr/bin/python
# -*- coding:utf-8 -*-
# Author: wyde
# Contact: wyde@csie.ntu.edu.tw

# import project-based 的 config
import sys
sys.path.append("/home/wyde/daan/config")
from default import *

# 跟抓資料有關的 import 區
import requests
from bs4 import BeautifulSoup
import re
import datetime
import copy
import re
import pandas as pd


# 抓取資料丟到 dataframe (Lab2)
def spider_station(infile):
    xl = pd.ExcelFile(infile)
    dfp = xl.parse('主計總處與內政部對照表')
    header = dfp.iloc[2]
    dfc = dfp[3:].copy().copy()
    dfc = dfc.rename(columns = header)
    dfd = dfc[['縣市名稱', '區鄉鎮名稱', '區里代碼']].drop_duplicates()
    dfd['區里代碼'] = dfd['區里代碼'].apply(lambda x: int(re.findall('\d+', str(x))[0]))
    ## dfc 裡有些區里代碼有亂碼，透過 regular expression 清乾淨再轉回 int
    dfd = dfd.reset_index(drop=True)
    df = dfd.copy().copy()
    cols = df.columns.tolist()
    cols = cols[-1:] + cols[:-1] # 等價 cols[2:] + cols[:2]
    df = df[cols]
    df.columns = ['sid', 'city', 'district']
    return df

def spider_report(d_code):
    url = 'http://www.cwb.gov.tw/V7/forecast/town368/3Hr/'  + str(d_code) + '.htm'
    print("spider is crawling %s..." % url)

    try:
        req = requests.get(url)
    except:
        print('WARNING: url fetching error, please try again and check district code...')
        return None
    
    rscode = req.status_code
    if not (rscode < 300 and rscode > 199):
        print('WARNING: http status code returns %d...' % rscode)
        return None

    req.encoding = 'utf-8' # 不指定會發生編碼錯誤
    soup = BeautifulSoup(req.text, 'html.parser')
    trs = soup.find_all('tr')
    #print("    fetching data from completed, parsing...")
    
    columns = ['record_t', # 0
               'weekday', # 1
               'wx', # 2
               't', # 3 
               'at', # 4
               'beaufort', # 5
               'wind_dir', # 6
               'rh', # 7
               'pop', #8 
               'ci'] # 9
    df = pd.DataFrame(columns=columns)
    #print("    building empty dataframe, there're %d columns in dataframe" % len(columns))

    year_s = []
    year_s.append("%d" % datetime.datetime.now().year)
    year_s.append("%d" % (datetime.datetime.now() + datetime.timedelta(days=1)).year) # in case tmrr is next year
    year_s.append("%d" % (datetime.datetime.now() + datetime.timedelta(days=2)).year) # in case it's next year in 2 days
    colspans = []
    dates = []
    days = []
    k = 0
    for idx, td in enumerate(trs[0].findAll('td')): # trs[0] 是時間相關的列
        if idx > 0:
            if td.has_attr('colspan'):
                colspans.append(td.attrs['colspan'])
            else:
                colspans.append("1")
            days.append(re.findall('[一|二|三|四|五|六|日]', td.text)[0]) # 用正規表示式把星期"幾"選出來
            month_n_date = re.findall('\d+', td.text)
            dates.append(year_s[k] + '-' + month_n_date[0] + '-' + month_n_date[1])
            k+=1
    #print("    cleaned up time information...")
    
    # insert data into dataframe
    record_ts = []
    weekdays = []
    hours = trs[1].findAll('span')
    k = 0
    for i in range(0, len(colspans)):
        for j in range(0, int(colspans[i])):
            record_ts.append(dates[i] + 'T' + hours[k].text)
            k+=1
            weekdays.append(days[i])
    df['record_t'] = record_ts #第 0 行
    df['weekday'] = weekdays #第 1 行
    
    wxs = []
    for img in trs[2].findAll('img'):
        wxs.append(img.attrs['alt'])
    df['wx'] = wxs #第 2 行
    #print("    %d:%d columns data inserted..." % (0,2))
    
    vals = []
    for i in range(3, 10): # 第 3 行到第 9 行除了第 8 行
        if i is not 8: # 降雨機率可能要展開 colspan == 2
            tds = trs[i].findAll('td')
            for idx, td in enumerate(tds):
                if idx > 0:
                    vals.append(td.text)
            df.iloc[:,i] = vals
            vals = []
    #print("    %d:%d columns data inserted...except %d" % (3, 9, 8))
    
    pops = [] # probability of precipitation
    rep = 0
    for idx, td in enumerate(trs[8].findAll('td')): # 第 8 行
        if idx > 0:
            if td.has_attr('colspan'):
                rep = int(td.attrs['colspan'])
            else:
                rep = 1
            for i in range(0, rep):
                pops.append(td.text)
    df['pop'] = pops
    #print("    inserted the %dth column" % 8)
    df.insert(0, 'station_sid', d_code)
    #print("    inserted the district code: %d at the beginning column" % d_code)
    print("crawling completed, return dataframe")
    return df

# SQLAlchemy 和 MySQL 參數 import 區
from sqlalchemy import DateTime, TIMESTAMP, text, Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship, sessionmaker

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
Base = declarative_base()


# SQLAlchemy 的 Class 們
class Station(Base):
    __tablename__ = 'station'
    sid = Column(Integer, primary_key=True, autoincrement=False)
    city = Column(String(8))
    district = Column(String(8))
    
    def __repr__(self):
        return 'sid: %d, city: %s, district: %s' % (self.sid, self.city, self.district)

class Report(Base):
    __tablename__ = 'report'
    rid = Column(Integer, primary_key=True)
    #station_sid = Column(Integer, ForeignKey('station.sid'))
    station_sid = Column(Integer)
    update_t = Column(TIMESTAMP, server_default=text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'))
    record_t = Column(TIMESTAMP)
    weekday = Column(String(3))
    wx = Column(String(32))
    t = Column(Integer)
    at = Column(Integer)
    beaufort = Column(String(16))
    wind_dir = Column(String(3))
    rh = Column(String(4))
    pop = Column(String(4))
    ci = Column(String(8))

    def __repr__(self):
        return """rid: %d, \nstation_sid: %d, \nupdate_t: %s, \nrecord_t: %s, \nweekday: %s, \nwx: %s, \
                \nt: %d, \nat: %d, \nbeaufort: %s, \nwind_dir: %s, \nrh: %s, \npop: %s, \nci: %s""" \
                % (self.rid, self.station_sid, str(self.update_t), str(self.record_t), self.weekday, \
                self.wx, self.t, self.at, self.beaufort, self.wind_dir, self.rh, self.pop, self.ci)


# function 們

def recreate_table(engine, table):
    if engine.dialect.has_table(engine, table):
        Base.metadata.tables[table].drop(engine)
        print('table ' + table +  ' has been droped')
    Base.metadata.tables[table].create(engine)
    print('table ' + table +  ' has been created...')
    
#def insert_df_into_mysql(df):
#    Session = sessionmaker(bind=engine)
#    session = Session()
#    df.to_sql(name='report', con=engine, if_exists='append', index=False)
#    session.close()

def autosave_df_to_csv(df):
    outfile_csv = datetime.datetime.now().strftime("./csv/%Y%m%d%H%m%S_dataframe.csv")
    df.to_csv(outfile_csv, sep=',', encoding='utf-8', index=False)
    print('csv file %s saved\n' % outfile_csv)
    
def update_mysql_data(row, ta):
    ta.wx = row['wx']
    ta.t = row['t']
    ta.at = row['at']
    ta.beaufort = row['beaufort']
    ta.wind_dir = row['wind_dir']
    ta.rh = row['rh']
    ta.pop = row['pop']
    ta.ci = row['ci']

def add_mysql_data(row):
    ta = Report()
    ta.station_sid = row['station_sid']
    ta.record_t = row['record_t']
    ta.weekday = row['weekday']
    ta.wx = row['wx']
    ta.t = row['t']
    ta.at = row['at']
    ta.beaufort = row['beaufort']
    ta.wind_dir = row['wind_dir']
    ta.rh = row['rh']
    ta.pop = row['pop']
    ta.ci = row['ci']
    return ta

if __name__ == '__main__':
    engine_para = ('mysql+mysqldb://' + 
                MYSQL_CONFIG['user'] + ':' +
                MYSQL_CONFIG['passwd'] + '@' +
                MYSQL_CONFIG['host'] + ':3306/' +
                MYSQL_CONFIG['db'] + '?charset=' +
                MYSQL_CONFIG['charset'])
    engine = create_engine(engine_para, max_overflow=5)

    # 第一次用先建立全部 table
#    Base.metadata.create_all(engine) # create all tables
#    print('all tables created')

    # 測試用的 function，重建 table
    # 注意!!!!!!資料會消失
    #recreate_table(engine, 'station')
    #recreate_table(engine, 'report')

    # 開啟 mysql 連線
    Session = sessionmaker(bind=engine)
    session = Session()
    
    # 先抓 station，station 的 excel 表事先已下載
    # csv、xlsx 先用 wget 載好再處理
#    print("dealing with station data")
#    df = spider_station('./xlsx/comparison_table.xlsx')
#    try:
#        df.to_sql(name='station', con=engine, if_exists = 'append', index=False)
#    except:
#        print('WARNING: table station might already exist')

    # insert or update data in mysql schema each row a time
#    print("\nupdating mysql...only in 台北市")
#    stations = session.query(Station).filter_by(city='台北市').all()

    print("\nupdating mysql...throughout Taiwan")
    stations = session.query(Station).all()
    for station in stations:
        print('\nScanning: ' + station.city + station.district + ' current time: ' +  datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S"))
        df = spider_report(station.sid)
        if df is not None:
            for idx, row in df.iterrows():
                record_t = row['record_t']
                station_sid = row['station_sid'] #台北市大安區碼 6300300
                kwargs = {'record_t':record_t, 'station_sid':station_sid}
                try:
                    record = session.query(Report).filter_by(**kwargs).all()[0]
                    update_mysql_data(row, record)
                    session.commit()
                    print("    %s has been found in mysql report table" % record_t)
                except:
                    record = add_mysql_data(row)
                    session.add(record)
                    session.commit()
                    print("    %s not found, new record has been created" % record_t)
    print("updated, closing session\n")

    # 關掉 mysql 連線
    session.close()

    # 生成測資，自動依日期時間存檔
    # autosave_df_to_csv(df)
