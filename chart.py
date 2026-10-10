import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from datetime import date
# =========================
# 常用颜色（OpenCV使用BGR）
# =========================
white = (255, 255, 255)
red = (0, 0, 255)
orange = (0, 165, 255)
yellow = (0, 255, 255)
green = (0, 255, 0)       # 已完成
blue = (255, 0, 0)        # 未完成
# =========================
# 添加中文文字
# =========================
def add_chinese(image_bgr, text, position, color, size):
    image = Image.fromarray(
        cv2.cvtColor(image_bgr, cv2.COLOR_BGR2RGB)
    )
    draw = ImageDraw.Draw(image)
    font = ImageFont.truetype("simsun.ttc", size)
    draw.text(
        position,
        str(text),
        fill=color,
        font=font
    )
    image_bgr = cv2.cvtColor(
        np.array(image),
        cv2.COLOR_RGB2BGR
    )
    return image_bgr
# =========================
# 获取截止日期字符串
# =========================
def get_deadline_str(deadline):
    if hasattr(deadline, "strftime"):
        return deadline.strftime("%Y-%m-%d")
    return str(deadline)
# =========================
# 生成任务统计图
# =========================
def chart(task_list):
    # =========================
    # 统计各优先级任务数量
    # 统计全部任务，不受显示数量限制
    # =========================
    counts = [
        sum(1 for t in task_list if t.priority == "高"),
        sum(1 for t in task_list if t.priority == "中"),
        sum(1 for t in task_list if t.priority == "低")
    ]
    labels = ["高", "中", "低"]
    colors = [red, orange, yellow]
    # =========================
    # 图片布局设置
    # =========================
    columns = 2
    task_height = 100
    # 每种优先级最多显示6个任务详情
    max_display = 6
    high_count, mid_count, low_count = counts
    # 实际显示的任务数量
    high_display = min(high_count, max_display)
    mid_display = min(mid_count, max_display)
    low_display = min(low_count, max_display)
    # 计算各优先级详情需要的行数
    high_rows = (high_display + columns - 1) // columns
    mid_rows = (mid_display + columns - 1) // columns
    low_rows = (low_display + columns - 1) // columns
    # 图片高度根据显示的任务数量计算
    height = (
        350
        + 60
        + (high_rows + mid_rows + low_rows) * task_height
        + 3 * 55
        + 80
    )
    # 图片宽度固定
    width = 1000
    # 创建纯黑色背景
    image = np.zeros(
        (height, width, 3),
        dtype=np.uint8
    )
    # =========================
    # 标题和生成日期
    # =========================
    today = date.today().strftime("%Y-%m-%d")
    image = add_chinese(
        image,
        "任务优先级统计图",
        (40, 15),
        white,
        30
    )
    image = add_chinese(
        image,
        f"生成日期：{today}",
        (40, 55),
        white,
        20
    )
    # =========================
    # 绘制柱状图
    # =========================
    max_count = max(counts) if max(counts) > 0 else 1
    bar_x = 100
    bar_width = 120
    bar_bottom = 260
    max_bar_height = 120
    for i in range(3):
        x1 = bar_x + i * 250
        x2 = x1 + bar_width
        bar_height = int(
            counts[i] / max_count * max_bar_height
        )
        y1 = bar_bottom - bar_height
        # 绘制柱子
        cv2.rectangle(
            image,
            (x1, y1),
            (x2, bar_bottom),
            colors[i],
            -1
        )
        # 显示任务数量
        cv2.putText(
            image,
            str(counts[i]),
            (x1 + 40, y1 - 10),
            cv2.FONT_HERSHEY_SIMPLEX,
            1.0,
            white,
            2
        )
        # 显示优先级名称
        image = add_chinese(
            image,
            labels[i],
            (x1 + 35, bar_bottom + 10),
            white,
            22
        )
    # =========================
    # 分隔线
    # =========================
    cv2.line(
        image,
        (30, 310),
        (width - 30, 310),
        (120, 120, 120),
        1
    )
    # =========================
    # 任务详细信息
    # =========================
    y = 330
    priority_colors = {
        "高": red,
        "中": orange,
        "低": yellow
    }
    for priority in ["高", "中", "低"]:
        # 找出当前优先级的全部任务
        tasks = [
            t for t in task_list
            if t.priority == priority
        ]
        # 实际显示的任务
        display_tasks = tasks[:max_display]
        # 显示优先级标题
        image = add_chinese(
            image,
            f"{priority}优先级（共{len(tasks)}个任务）",
            (40, y),
            white,
            22
        )
        y += 35
        # 每行显示两个任务
        for index, t in enumerate(display_tasks):
            row = index // columns
            column = index % columns
            x = 40 + column * 480
            task_y = y + row * task_height
            # 优先级颜色条
            cv2.rectangle(
                image,
                (x, task_y),
                (x + 420, task_y + 6),
                priority_colors[priority],
                -1
            )
            # 编号和标题
            image = add_chinese(
                image,
                f"编号：{t.num}  标题：{t.title}",
                (x, task_y + 12),
                white,
                17
            )
            # 截止日期
            deadline = get_deadline_str(t.deadline)
            image = add_chinese(
                image,
                f"截止日期：{deadline}",
                (x, task_y + 38),
                white,
                16
            )
            # 完成状态
            if t._status == "已完成":
                status_color = green
            else:
                status_color = blue
            image = add_chinese(
                image,
                f"状态：{t._status}",
                (x, task_y + 63),
                status_color,
                16
            )
        # 根据实际显示数量计算行数
        display_count = len(display_tasks)
        rows = (display_count + columns - 1) // columns
        # 超过显示上限时提示剩余数量
        if len(tasks) > max_display:
            image = add_chinese(
                image,
                f"还有 {len(tasks) - max_display} 个任务未显示",
                (40, y + rows * task_height),
                white,
                16
            )
            y += 25
        # 移动到下一种优先级的区域
        y += rows * task_height + 20
    # =========================
    # 保存图片
    # =========================
    cv2.imwrite("chart.png", image)
    print("图表已成功保存为 chart.png")
