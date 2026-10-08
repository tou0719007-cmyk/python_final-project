import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont

white=(255,255,255)
red=(0,0,255)
orange=(0,165,255)
yellow=(0,255,255)

import task

def add_chinese(image_bgr, text, position, textColor, textSize):
    
    image = Image.fromarray(cv2.cvtColor(image_bgr, cv2.COLOR_BGR2RGB)) #转换pil适用的环境
    draw = ImageDraw.Draw(image) #创建文本对象
    font = ImageFont.truetype("simsun.ttc", textSize)  # 使用系统自带的宋体字体
    draw.text(position, text, fill=textColor, font=font, weight="bold") #写入
    bbox = draw.textbbox(position, text, font=font) #位置

    image_bgr = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR) #转换opencv适用的环境
    return image_bgr ,bbox

def add_text(image_bgr, x, y, pos, i):
    cv2.putText(image_bgr, i.num, (x,y+15), cv2.FONT_HERSHEY_SIMPLEX, 1, white, 1, cv2.LINE_8, False)
    image_bgr, pos=add_chinese(image_bgr, i.title, (x,y), white, 30)
    y=pos[3]
    y+=10
    cv2.putText(image_bgr, i.deadline, (x,y+15), cv2.FONT_HERSHEY_SIMPLEX, 1, white, 1, cv2.LINE_8, False)
    (w,l),bsl=cv2.getTextSize(i.deadline, cv2.FONT_HERSHEY_SIMPLEX, 1, 1)
    y+=l
    image_bgr, pos=add_chinese(image_bgr, i.status, (x,y), white, 30)
    y=pos[3]
    y+=10
    return image_bgr


def chart(task_list):
    n=len(task_list)

    image_bgr = np.zeros((800, 250*n, 3), dtype=np.uint8)
    x_h,x_m,x_l=10,10,10
    pos=[0,0,0,0]

    for i in task_list:

        if i.priority == "高":
            cv2.rectangle(image_bgr, (x_h,100), (x_h+250,120), red, -1)
            image_bgr=add_text(image_bgr, x_h, 10, pos, i)
            x_h+=260
        elif i.priority == "中":
            cv2.rectangle(image_bgr, (x_l,300), (x_l+250,320), orange, -1)
            image_bgr=add_text(image_bgr, x_l, 210, pos, i)
            x_l+=260
        elif i.priority == "低":
            cv2.rectangle(image_bgr, (x_m,500), (x_m+250,520), yellow, -1)
            image_bgr=add_text(image_bgr, x_m, 410, pos, i)
            x_m+=260
    
    cv2.imshow("image", image_bgr)
    cv2.imwrite("chart.png", image_bgr)