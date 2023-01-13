from random import random
from tkinter import messagebox as messagebox
import pymysql
import time
import uuid

global cursor
global g_table
global sql_execute_list


def run():
    for x in sql_execute_list:
        print(x)
        cursor.execute(x)
    messagebox.showinfo("成功", "执行完成")


def try_connect(host, port, user, password, data_base, table):
    print(f"连接数据库...")
    try:
        conn = pymysql.connect(
            host=host,
            port=port,
            user=user,
            password=password,
            database=data_base,
            charset='utf8',
            autocommit=True  # 自动提交
        )
        global g_table
        g_table = table
        global cursor
        cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
    except pymysql.err.OperationalError as e:
        # 连接失败，报提示
        print(e)
    print(f"连接数据库成功，执行sql..")
    sql = "desc " + table
    try:
        cursor.execute(sql)
        return cursor.fetchall()
    except:
        messagebox.showerror("执行失败", f"数据库:{data_base} \n不存在表:{table}")
        return None


def generate_sql(count, filed_list):
    global sql_execute_list
    sql_execute_list = []

    id_value = int(random() * 10000)

    # 循环写入行数据
    for row in range(count):

        number_value = int(random() * 500)
        tinyint_value = int(random() * 2)
        str_value = uuid.uuid4().__str__()
        time_value = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        values_tuple = []
        global g_table
        str_sql = "INSERT INTO " + g_table + " VALUES"

        # 循环写入字段数据
        for field in filed_list:
            type = field["Type"]
            if type == "bigint" and field["Field"] == "id":
                values_tuple.append(id_value.__str__())
            elif type == "bigint" or type.startswith("int"):
                values_tuple.append(number_value.__str__())
            elif type.startswith("varchar") or type.startswith("text"):
                values_tuple.append("\"" + str_value + "\"")
            elif type.startswith("tinyint"):
                values_tuple.append(tinyint_value.__str__())
            elif type == "datetime":
                values_tuple.append("\"" + time_value + "\"")
            else:
                raise Exception(f"未支持的类型{type},请联系开发者完善")
            id_value += 1

        str_sql_value = ",".join(values_tuple)
        str_sql += "(" + str_sql_value + ")"

        sql_execute_list.append(str_sql)
    string_text = ""
    for x in sql_execute_list:
        string_text += x.__str__() + ";\n"
    return string_text
