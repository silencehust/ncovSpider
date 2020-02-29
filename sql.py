import requests
import json
import pymysql
import traceback
import time
from selenium.webdriver import Firefox,FirefoxOptions

def get_tencent_data(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:74.0) Gecko/20100101 Firefox/74.0"
    }
    r = requests.get(url=url, headers=headers)
    res = json.loads(r.text)
    data_all = json.loads(res["data"])
    return data_all

def get_conn():
    conn=pymysql.connect(host="localhost",user="root",password="CHENG345@qian",db="2019ncov",charset="utf8")
    cursor=conn.cursor()
    return conn,cursor

def close_conn(conn,cursor):
    if cursor:
        cursor.close()
    if conn:
        conn.close()

def get_history():
    historyUrl = "https://view.inews.qq.com/g2/getOnsInfo?name=disease_other"
    data_all=get_tencent_data(historyUrl)
    history={}
    for i in data_all['chinaDayList']:
        ds="2020."+i["date"]
        tup=time.strptime(ds,"%Y.%m.%d")
        ds=time.strftime("%Y-%m-%d",tup)
        confirm=i["confirm"]
        suspect=i["suspect"]
        heal=i["heal"]
        dead=i["dead"]
        history[ds]={"confirm":confirm,"suspect":suspect,"heal":heal,"dead":dead}

    for i in data_all['chinaDayList']:
        ds="2020."+i["date"]
        tup=time.strptime(ds,"%Y.%m.%d")
        ds=time.strftime("%Y-%m-%d",tup)
        confirm=i["confirm"]
        suspect=i["suspect"]
        heal=i["heal"]
        dead=i["dead"]
        history[ds].update({"confirm_add":confirm,"suspect_add":suspect,"heal_add":heal,"dead_add":dead})
    return history

def get_details():
    url = "https://view.inews.qq.com/g2/getOnsInfo?name=disease_h5"
    details=[]
    data_all=get_tencent_data(url)
    print(data_all)
    print(data_all.keys())
    print(data_all["areaTree"][0].keys())
    # print(data_all["areaTree"][0]["children"].keys())

def get_baidu_hot():
    option = FirefoxOptions()
    option.add_argument("--headless")
    option.add_argument("--no-sandbox")
    url="https://voice.baidu.com/act/virussearch/virussearch?from=osari_map&tab=0&infomore=1"
    web = Firefox(options=option)
    web.get(url)
    moreButton = web.find_element_by_xpath('/html/body/div[2]/div/div/div/section/div[2]/div[1]/div/div[2]/section/div')
    moreButton.click()
    time.sleep(1)
    s = web.find_elements_by_xpath(
        '/html/body/div[2]/div/div/div/section/div[2]/div[1]/div/div[2]/section/a/div/span[2]')
    context=[i.text for i in s]
    print(context)
    web.close()
    return context

def update_hotsearch():
    cursor=None
    conn=None
    try:
        context=get_baidu_hot()
        print(f"{time.asctime()}开始更新热搜数据")
        conn,cursor=get_conn()
        sql="insert into hotsearch(dt,content) values(%s,%s)"
        ts=time.strftime("%Y-%m-%d %X")
        for i in context:
            cursor.execute(sql,(ts,i))
        conn.commit()
        print(f"{time.asctime()}数据更新完毕")
    except:
        traceback.print_exc()
    finally:
        close_conn(conn,cursor)

if __name__ == '__main__':
   update_hotsearch()