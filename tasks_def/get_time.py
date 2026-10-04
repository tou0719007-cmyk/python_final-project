from datetime import datetime  #引入模块

def get_datetime():
    while True:
        #捕捉错误,通过while True循环输入
        try:
            #deadtime.strptime用于检查输入的日期是否规范,第一个参数为输入的日期,第二个参数为输入格式
            deadline=datetime.strptime(input("请输入截止日期(YYYY-MM-DD):"),"%Y-%m-%d")
            return deadline
        except ValueError:
            print("输入错误,请重新输入")


if __name__=="__main__":    #测试代码
    get_datetime()