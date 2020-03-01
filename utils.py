import time
import pymysql
def get_time():
    time_str=time.strftime("%Y{}%m{}%d{} %X")
    return time_str.format("年","月","日")

def get_conn():
    conn=pymysql.connect(host="localhost",user="root",password="CHENG345@qian",db="2019ncov",charset="utf8")
    cursor=conn.cursor()
    return conn,cursor

def close_conn(conn,cursor):
    if cursor:
        cursor.close()
    if conn:
        conn.close()

def query(sql,*args):
    conn,cursor=get_conn()
    cursor.execute(sql,args)
    res=cursor.fetchall()
    close_conn(conn,cursor)
    return res

def get_c1_data():
    sql="select sum(confirm),(select suspect from history order by ds desc limit 1),sum(heal),sum(dead) from details where update_time=(select update_time from details order by update_time desc limit 1)"
    res=query(sql)
    return res[0]

if __name__ == '__main__':
    print(get_c1_data())