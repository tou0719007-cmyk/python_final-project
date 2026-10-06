from datetime import datetime

def generate_html_report(task_list):
    #获取统计数据
    total = len(task_list)
    completed = sum(1 for t in task_list if t._status == "已完成")
    completion_rate = (completed / total * 100) #if total > 0 else 0
    
    #获取当前日期
    today_str = datetime.now().strftime("%Y-%m-%d")

    #准备 HTML 的头部（表头之前的部分）
    html_head = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <title>任务报告 - {today_str}</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 40px; color: #333; }}

        .header {{ border-bottom: 2px solid #eee; padding-bottom: 20px; margin-bottom: 20px; }}

        .progress-bar {{ width: 300px; margin-top: 10px; }}

        table {{ width: 100%; border-collapse: collapse; }}

        th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}

        th {{ background-color: #f2f2f2; }}

        .overdue {{ color: red; font-weight: bold; }} /* 逾期标红 */
    </style>
</head>
<body>
    <div class="header">
        <p><strong>生成日期：</strong>{today_str}</p >
        <p><strong>任务总数：</strong>{total}</p >
        <p><strong>已完成数：</strong>{completed}</p >
        <p><strong>完成率：</strong>{completion_rate:.1f}%</p >
        <progress class="progress-bar" value="{completion_rate:.1f}" max="100"></progress>
    </div>

    <table>
        <thead>
            <tr>
                <th>编号</th>
                <th>优先级</th>
                <th>截止日期</th>
                <th>状态</th>
                <th>标题</th>
            </tr>
        </thead>
        <tbody>
"""

    #HTML的尾部
    html_tail = """
        </tbody>
    </table>
</body>
</html>
"""

    #使用for循环遍历并拼接表格行
    rows_html = []  # 创建一个空列表用来存每一行数据
    
    for task in task_list:
        #判断是否逾期
        if task._status == "未完成" and task.deadline < today_str:
            tr_class = ' class="overdue"' #如果是逾期，加上红色的类名
        else:
            tr_class = '' #否则不加类名

        #HTML代码追加到列表里
        row = f"""
            <tr{tr_class}>
                <td>{task.num}</td>
                <td>{task.priority}</td>
                <td>{task.deadline}</td>
                <td>{task._status}</td>
                <td>{task.title}</td>
            </tr>
        """
        rows_html.append(row)

    # "".join(rows_html)把列表里的所有字符串无缝连接在一起
    final_html = html_head + "".join(rows_html) + html_tail
    filename = f"report_{today_str}.html"
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(final_html)
        print(f"报告已成功导出为：{filename}")
    except Exception as e:
        print(f"导出失败，错误信息：{e}")