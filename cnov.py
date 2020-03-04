import requests
import json
import pymysql
import traceback
import time
from selenium.webdriver import Firefox,FirefoxOptions
import sys

def get_tencent_data(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:74.0) Gecko/20100101 Firefox/74.0"
    }
    r = requests.get(url=url, headers=headers)
    res = json.loads(r.text)
    data_all = json.loads(res["data"])
    return data_all
def get_history():
    historyUrl = "https://view.inews.qq.com/g2/getOnsInfo?name=disease_other"
    data_all=get_tencent_data(historyUrl)
    history={}
    for i in data_all['chinaDayList']:
        ds = "2020." + i["date"]
        tup = time.strptime(ds, "%Y.%m.%d")
        ds = time.strftime("%Y-%m-%d", tup)
        confirm = i["confirm"]
        suspect = i["suspect"]
        heal = i["heal"]
        dead = i["dead"]
        history[ds] = {"confirm": confirm, "suspect": suspect, "heal": heal, "dead": dead}

    for i in data_all['chinaDayAddList']:
        ds = "2020." + i["date"]
        tup = time.strptime(ds, "%Y.%m.%d")
        ds = time.strftime("%Y-%m-%d", tup)
        confirm = i["confirm"]
        suspect = i["suspect"]
        heal = i["heal"]
        dead = i["dead"]
        history[ds].update({"confirm_add": confirm, "suspect_add": suspect, "heal_add": heal, "dead_add": dead})

    return history

def get_details():
    url = "https://view.inews.qq.com/g2/getOnsInfo?name=disease_h5"
    details=[]
    data_all=get_tencent_data(url)
    update_time=data_all["lastUpdateTime"]
    data_country=data_all["areaTree"]
    data_province=data_country[0]["children"]
    for province_info in data_province:
        province=province_info["name"]
        for city_info in province_info["children"]:
            city=city_info["name"]
            confirm=city_info["total"]["confirm"]
            confirm_add=city_info["today"]["confirm"]
            heal=city_info["total"]["heal"]
            dead=city_info["total"]["dead"]
            details.append([update_time,province,city,confirm,confirm_add,heal,dead])

    return details

def get_conn():
    conn=pymysql.connect(host="116.62.52.185",user="root",password="CHENG345@qian",db="2019ncov",charset="utf8")
    cursor=conn.cursor()
    return conn,cursor

def close_conn(conn,cursor):
    if cursor:
        cursor.close()
    if conn:
        conn.close()

def update_details():
    cursor=None
    conn=None
    try:
        li=get_details()
        conn,cursor=get_conn()
        sql="insert into details(update_time,province,city,confirm,confirm_add,heal,dead) value(%s,%s,%s,%s,%s,%s,%s)"
        sql_query="select %s=(select update_time from details order by id desc limit 1)"
        cursor.execute(sql_query,li[0][0])
        if not cursor.fetchone()[0]:
            print(f"{time.asctime()}开始更新最新数据")
            for item in li:
                cursor.execute(sql,item)
            conn.commit()
            print(f"{time.asctime()}更新最新数据完毕")
        else:
            print(f"{time.asctime()}已是最新数据!")
    except:
        traceback.print_exc()
    finally:
        close_conn(conn,cursor)

def insert_history():
    cursor=None
    conn=None
    try:
        dic=get_history()
        print(f"{time.asctime()}开始插入历史数据")
        conn,cursor=get_conn()
        sql="insert into history values(%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        for k,v in dic.items():
            cursor.execute(sql,[k,v.get("confirm"),v.get("confirm_add"),v.get("suspect"),v.get("suspect_add"),
                                v.get("heal"),v.get("heal_add"),v.get("dead"),v.get("dead_add")])
        conn.commit()
        print(f"{time.asctime()}插入历史数据完毕")
    except:
        traceback.print_exc()
    finally:
        close_conn(conn,cursor)

def update_history():
    cursor = None
    conn = None
    try:
        dic = get_history()
        print(f"{time.asctime()}开始更新历史数据")
        conn, cursor = get_conn()
        sql = "insert into history values(%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        sql_query="select confirm from history where ds=%s"
        for k, v in dic.items():
            if not cursor.execute(sql_query,k):
                cursor.execute(sql, [k, v.get("confirm"), v.get("confirm_add"), v.get("suspect"), v.get("suspect_add"),
                                 v.get("heal"), v.get("heal_add"), v.get("dead"), v.get("dead_add")])
        conn.commit()
        print(f"{time.asctime()}历史数据更新完毕")
    except:
        traceback.print_exc()
    finally:
        close_conn(conn, cursor)

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
    l=len(sys.argv)
    if l==1:
        s="""
        参数说明：
        1：更新历史数据
        2：更新详情数据
        3：更新每日热搜数据
        """
        print(s)
    else:
        order=sys.argv[1]
        if order=="1":
            update_history()
        elif order=="2":
            update_details()
        elif order=="3":
            update_hotsearch()
        else:
            print("参数错误")
