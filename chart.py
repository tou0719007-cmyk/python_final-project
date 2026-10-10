import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from datetime import date

white=(255,255,255)
red=(0,0,255)
orange=(0,165,255)
yellow=(0,255,255)
#常用颜色bgr,下面里不直接使用的一般为rgb

#import get_time

import task

def add_chinese(image_bgr, text, position, textColor, textSize):#中文写入
    
    image = Image.fromarray(cv2.cvtColor(image_bgr, cv2.COLOR_BGR2RGB)) #转换pil适用的环境
    draw = ImageDraw.Draw(image) #创建文本对象
    font = ImageFont.truetype("simsun.ttc", textSize)  # 使用系统自带的宋体字体
    draw.text(position, text, fill=textColor, font=font, weight="bold") #写入
    bbox = draw.textbbox(position, text, font=font) #位置

    image_bgr = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR) #转换opencv适用的环境
    return image_bgr ,bbox

def add_text(image_bgr, x, y, pos, i):#读取任务内容并打印
    
    cv2.putText(image_bgr, i.num, (x,y+25), cv2.FONT_HERSHEY_SIMPLEX, 1, white, 1, cv2.LINE_8, False) #手动调节格式对齐
    #序号
    
    (w,_),_=cv2.getTextSize(i.num,cv2.FONT_HERSHEY_SIMPLEX,1,1)
    image_bgr, pos=add_chinese(image_bgr, i.title, (x+w,y), white, 30)
    #标题
    y=pos[3]
    y+=10
    
    cv2.putText(image_bgr, i.deadline, (x,y+15), cv2.FONT_HERSHEY_SIMPLEX, 1, white, 1, cv2.LINE_8, False)
    #日期
    (_,l),_=cv2.getTextSize(i.deadline, cv2.FONT_HERSHEY_SIMPLEX, 1, 1)
    y+=l

    if i._status== "已完成":
        image_bgr, pos=add_chinese(image_bgr, i._status, (x,y), (0,255,0), 30)
    elif i._status=="未完成":
        image_bgr, pos=add_chinese(image_bgr, i._status, (x,y), (255,0,0), 30)
    #用绿色展示已完成任务，用红色展示未完成任务
    y=pos[3]
    y+=10
    
    return image_bgr

def chushihua(task_list):#初始化

    #统计各类任务个数
    task_count=[0,0,0]
    for i in task_list:
        if i.priority == "高":
            task_count[0]+=1
        elif i.priority == "中":
            task_count[1]+=1
        elif i.priority == "低":
            task_count[2]+=1
    
    length=max(task_count[0],task_count[1],task_count[2])*260+100
    #动态长度调节

    image_bgr = np.full((650, length, 3), 64, dtype=np.uint8)
    #灰色背景

    cv2.line(image_bgr,(50,100),(50,650),white,2)
    cv2.line(image_bgr,(0,50),(length,50),white,2)
    cv2.line(image_bgr,(0,100),(length,100),white,2)
    #基准线打印

    D=date.today()
    d=str(D)
    image_bgr,_=add_chinese(image_bgr,"生成日期：",(0,0),white,50)
    cv2.putText(image_bgr,d,(255,45),cv2.FONT_HERSHEY_SIMPLEX,2.0,white,1)
    #上方日期打印

    image_bgr,_=add_chinese(image_bgr,"高",(0,120),white,50)
    image_bgr,_=add_chinese(image_bgr,"中",(0,320),white,50)
    image_bgr,_=add_chinese(image_bgr,"低",(0,520),white,50)
    #左侧固定标准打印

    cv2.putText(image_bgr,str(task_count[0]),(10,210),cv2.FONT_HERSHEY_SIMPLEX,2.0,red,1)
    cv2.putText(image_bgr,str(task_count[1]),(10,410),cv2.FONT_HERSHEY_SIMPLEX,2.0,orange,1)
    cv2.putText(image_bgr,str(task_count[2]),(10,610),cv2.FONT_HERSHEY_SIMPLEX,2.0,yellow,1)
    #左侧任务数统计打印

    x=60
    count=0
    while x<=length:
        cv2.putText(image_bgr,str(count),(x-10,90),cv2.FONT_HERSHEY_SIMPLEX,1.0,white,1)
        count+=1
        if count==1:
            x+=255
            continue
        cv2.line(image_bgr,(x,100),(x,650),white,2)
        x+=260
    #上方动态任务数

    return image_bgr

def chart(task_list):

    image_bgr=chushihua(task_list)
    
    x_h,x_m,x_l=60,60,60
    pos=[0,0,0,0]

    for i in task_list:
        
        if i.priority == "高":
            cv2.rectangle(image_bgr, (x_h,110), (x_h+250,130), red, -1)
            image_bgr=add_text(image_bgr, x_h, 130, pos, i)
            x_h+=260
        elif i.priority == "中":
            cv2.rectangle(image_bgr, (x_l,310), (x_l+250,330), orange, -1)
            image_bgr=add_text(image_bgr, x_l, 330, pos, i)
            x_l+=260
        elif i.priority == "低":
            cv2.rectangle(image_bgr, (x_m,510), (x_m+250,530), yellow, -1)
            image_bgr=add_text(image_bgr, x_m, 530, pos, i)
            x_m+=260

    cv2.imwrite("chart.png", image_bgr)

#chart(task_list) 测试用