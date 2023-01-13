import os
import sys
import sqlutil
import tkinter as tk


def get_resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)


def do_execute():
    list_filed = sqlutil.try_connect(host.get(), port.get(), user.get(), password.get(), data_base.get(), table.get())
    sqlutil.generate_sql(count.get(), list_filed)
    sqlutil.run()


def pop_win_command():
    list_filed = sqlutil.try_connect(host.get(), port.get(), user.get(), password.get(), data_base.get(), table.get())
    if list_filed is None:
        return
    string_text = sqlutil.generate_sql(count.get(), list_filed)

    pop_win = tk.Toplevel()
    pop_win.title("SQL预览")
    pop_win.geometry("1150x850+450+50")  # 定义弹窗大小及位置，前两个是大小，用字母“x”连接，后面是位置。
    entry_1 = tk.Text(pop_win, width=150, height=60)

    entry_1.grid(row=0, column=0, columnspan=2, padx=10, pady=10)

    entry_1.insert(tk.END, str(string_text))
    entry_1.focus_set()  # 把焦点设置到输入框上，就是弹窗一出，光标在输入框里了。

    def chuli_enter(ev=None):
        sqlutil.run()
        pop_win.destroy()

    entry_1.bind("<Return>", chuli_enter)  # 绑定在entry_1输入完内容后回车提交

    def tuichu(ev=None):
        pop_win.destroy()  # 关闭弹窗

    pop_win.bind("<Escape>", tuichu)  # 当焦点在整个弹窗上时，绑定ESC退出

    b1 = tk.Button(pop_win, width=20, text="退出", command=tuichu)
    b1.grid(row=2, column=0, padx=5, pady=5)

    b2 = tk.Button(pop_win, width=20, text="提交", command=chuli_enter)
    b2.grid(row=2, column=1, padx=5, pady=5)



if __name__ == '__main__':
    tk_window = tk.Tk()
    screenwidth = tk_window.winfo_screenwidth()
    screenheight = tk_window.winfo_screenheight()

    # 窗口居中，获取屏幕尺寸以计算布局参数，使窗口居屏幕中央
    width = 1100
    height = 580
    size_geo = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
    tk_window.title("sql数据生成器")
    tk_window.geometry(size_geo)
    # 更改左上角窗口的的icon图标
    tk_window.iconphoto(False, tk.PhotoImage(file=get_resource_path("icon.png")))
    # 设置主窗口的背景颜色 #214283蓝色
    tk_window["background"] = "#FFFFFF"

    host = tk.StringVar()
    port = tk.IntVar()
    user = tk.StringVar()
    password = tk.StringVar()
    data_base = tk.StringVar()
    table = tk.StringVar()
    count = tk.IntVar()

    tk.Label(tk_window, text="主机：").grid(row=0, column=0)
    tk.Label(tk_window, text="端口：").grid(row=1, column=0)
    tk.Label(tk_window, text="用户名：").grid(row=2, column=0)
    tk.Label(tk_window, text="密码：").grid(row=3, column=0)
    tk.Label(tk_window, text="数据库：").grid(row=4, column=0)
    tk.Label(tk_window, text="表名：").grid(row=5, column=0)
    tk.Label(tk_window, text="生成数据条数：").grid(row=6, column=0)

    tk.Entry(tk_window, textvariable=host).grid(row=0, column=1, padx=5)
    tk.Entry(tk_window, textvariable=port).grid(row=1, column=1, padx=5)
    tk.Entry(tk_window, textvariable=user).grid(row=2, column=1, padx=5)
    tk.Entry(tk_window, textvariable=password).grid(row=3, column=1, padx=5)
    tk.Entry(tk_window, textvariable=data_base).grid(row=4, column=1, padx=5)
    tk.Entry(tk_window, textvariable=table).grid(row=5, column=1, padx=5)
    tk.Entry(tk_window, textvariable=count).grid(row=6, column=1, padx=5)

    tk.Button(tk_window, text="执行", command=do_execute).grid(row=7, column=1, columnspan=2, ipady=5, ipadx=10,
                                                               pady=15)
    tk.Button(tk_window, text="预览SQL", command=pop_win_command).grid(row=7, column=3, columnspan=2, ipady=5, ipadx=10,
                                                                       pady=15)
    # 加载图片LOGO
    photo = tk.PhotoImage(file=get_resource_path("icon.png"))
    tk.Label(tk_window, image=photo).grid(row=0, column=4, rowspan=7, padx='20px', pady='30px')
    tk_window.mainloop()
