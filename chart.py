import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import datetime

white=(255,255,255)
red=(0,0,255)
orange=(0,165,255)
yellow=(0,255,255)

import task

#中文
def add_chinese(image_bgr, text, position, color, size):
    imge = Image.fromarray(cv2.cvtColor(image_bgr, cv2.COLOR_BGR2RGB))
    draw = ImageDraw.Draw(imge)
    font = ImageFont.truetype("simsun.ttc", size)
    draw.text(position, text, fill=color, font=font)
    return cv2.cvtColor(np.array(imge), cv2.COLOR_RGB2BGR)

#核心图表函数
def chart(task_list):
    #统计各优先级数量
    counts = [
        sum(1 for t in task_list if t.priority == "高"),
        sum(1 for t in task_list if t.priority == "中"),
        sum(1 for t in task_list if t.priority == "低"),
    ]
    labels = ["高", "中", "低"]
    colors = [red, orange, yellow]

    #创建画布和标题
    image = np.zeros((850, 900, 3), dtype=np.uint8) + 50
    today = datetime.date.today().strftime("%Y-%m-%d")
    image = add_chinese(image, f"任务优先级统计图 - 生成日期: {today}", (120, 30), white, 30)

    #绘制柱状图
    max_count = max(counts) if max(counts) > 0 else 1
    for i in range(3):
        x1 = 150 + i * 200           #柱子左边界
        x2 = x1 + 100                #柱子右边界
        y2 = 500                     #底边
        bar_height = int(counts[i] / max_count * 350)
        y1 = y2 - bar_height

        cv2.rectangle(image, (x1, y1), (x2, y2), colors[i], -1)
        cv2.putText(image, str(counts[i]), (x1 + 25, y1 - 15),
                    cv2.FONT_HERSHEY_SIMPLEX, 1.2, white, 2)
        image = add_chinese(image, labels[i], (x1 + 35, y2 + 15), white, 25)

    #分隔线
    cv2.line(image, (60, 570), (740, 570), (120, 120, 120), 1)

    legend_top = 550
    box= 30
    row_gap = 50
    x = 80

    for i in range(3):
        y = legend_top + 45 + i * row_gap
        cv2.rectangle(image, (x, y), (x + box, y + box),
                      colors[i], -1)
        if labels[i] == "高":
            tasks = [t.title for t in task_list if t.priority == "高"]
        elif labels[i] == "中":
            tasks = [t.title for t in task_list if t.priority == "中"]
        else:
            tasks = [t.title for t in task_list if t.priority == "低"]

        tasks_str = "、".join(tasks) if tasks else "无"
        text = f"{labels[i]}优先级: {tasks_str}"
        image = add_chinese(image, text, (x + box + 20, y + 3), white, 20)

    # 显示并保存
    cv2.imshow("Task Statistics Chart", image)
    cv2.waitKey()
    cv2.destroyAllWindows()
    cv2.imwrite("chart.png", image)
    print("图表已成功保存为 chart.png")