import storage
import get_time    #导入模块
import task
import datetime

def to_date_str(value):
    """把截止日期统一成可比较的 "YYYY-MM-DD" 字符串。

    get_time.get_datetime() 返回的是 datetime 对象，而字符串才能按
    "YYYY-MM-DD" 直接比大小（定长、大单位在前、有补零）。
    这里做一次转换，筛选和逾期判断就都能正常工作。
    """
    if value is None:
        return ""
    if hasattr(value, "strftime"):        # datetime / date 对象
        return value.strftime("%Y-%m-%d")
    return str(value).strip()             # 已经是字符串, 原样返回


class SystemManager:
    #定义类名,属性
    version = 1.0
    name ="任务管理系统"
        # 初始化任务管理系统
    def __init__(self):
        self._task_list = storage.load_task()
    #添加任务
    def add_task(self,):
        while True:
            try:
                #输入基本信息
                new_task= input("请输入任务的编号:")
                num_condition= False

                for tasks in self._task_list:  # 遍历列表找到目标任务
                    if tasks.num == new_task:
                        print("该任务编号已存在,请重新输入")
                        num_condition = True
                        break

                if not num_condition:#如果编号重复,则不执行后续代码,重新输入
                    continue
                new_num = new_task
                new_title = input("请输入任务的标题:")
                new_priority = input("请输入任务的优先级(低/中/高):")
                new_deadline=get_time.get_datetime()       #命令有点长,放进get_time.py文件了
                new_status = input("请输入任务当前状态(未完成/已完成):")
                # 检查用户的输入是否规范,不规范则重新输入(while True循环)
                if (new_priority not in ["低", "中","高"]
                    or new_status not in ["未完成", "已完成"]):
                    print("输入错误,请重新输入")
                # 添加一个任务对象
                else:
                    new_task = task.Task(new_num, new_title, new_priority, new_deadline, new_status)
                    self._task_list.append(new_task)
                    print("添加成功")
                    break
            except Exception:
                print("输入错误,请重试")
    #输出所有的任务
    def view_tasks(self):
        if not self._task_list:         #判断列表是否为空
            print("暂时没有可管理的任务")
            return
        else:
            for tasks in self._task_list:
                print(tasks)

     #更改任务状态为完成
    def complete_task(self):
        while True:
            try:
                target_task = input("请输入想更改的任务编号:")
                for tasks in self._task_list:     #遍历列表找到目标任务
                    if tasks.num == target_task:
                        tasks.change_status()
                        return
                print("该任务不存在")      #如果存在该任务,遍历列表时会触发return,没有则进入print语句
            except Exception:
                print("输入错误,请重新输入")
    #删除任务
    def delete_task(self):
        while True:
            try:
                target_task=input("请输入想删除的任务编号:")
                for tasks in self._task_list:      #遍历列表
                    if tasks.num==target_task:
                        self._task_list.remove(tasks)
                        print("删除成功")
                        return
                print("该任务不存在,删除失败")
            except Exception:
                print("输入错误,请重新输入")
    # 获取任务列表
    def get_tasks(self):
        return self._task_list
    # 保存任务
    def save_task(self):
        storage.save_task(self._task_list)



    


    def search_tasks(self, keyword):
        result = []         
        if not keyword:             #没输入关键词就直接返回空
            return result
        key = keyword.lower()       # 统一小写,搜索时忽略大小写
        for t in self._task_list:
            if key in t.title.lower():  #关键词包含在标题里即命中
                result.append(t)     
        return result                # 不修改原列表，只返回筛选结果
    

    def statistics(self):
        """统计任务整体情况，返回固定键名的字典。

        返回：总数、已完成、未完成、完成率、逾期数、高/中/低优先级数量
        注意：report.py、chart.py 也用这个字典，三处数字保证一致
        """
        today = datetime.date.today().strftime("%Y-%m-%d")  # 今天，带补零 
        stat = {
            "total": len(self._task_list),
            "done": 0,
            "undone": 0,
            "overdue": 0,
            "rate": 0.0,
            "high": 0,
            "mid": 0,
            "low": 0,
        }

        for t in self._task_list:
            # 1) 完成/未完成（Task 类里状态保存在 _status）
            if t._status == "已完成":
                stat["done"] += 1
            else:
                stat["undone"] += 1

            # 2) 逾期：未完成 且 截止日期早于今天
            #    先转成 "YYYY-MM-DD" 文本再比较，兼容 get_time 返回的 datetime 对象
            if t._status != "已完成" and to_date_str(t.deadline) < today:
                stat["overdue"] += 1

            # 3) 按优先级计数（附加任务图表就用这三个数）
            if t.priority == "高":
                stat["high"] += 1
            elif t.priority == "中":
                stat["mid"] += 1
            elif t.priority == "低":
                stat["low"] += 1

        # 4) 完成率：乘100.0保证是小数，空列表时不除零
        if stat["total"] > 0:
            stat["rate"] = stat["done"] * 100.0 / stat["total"]

        return stat

    def filter_tasks(self, priority=None, status=None,
                    due_before=None, due_after=None, overdue_only=None):
        """按多个条件筛选任务，返回满足全部条件的新列表。

        参数为 None 表示这一项不限制（不影响筛选结果）。
        priority     : "高"/"中"/"低"      —— 只看该优先级
        status       : "已完成"/"未完成"     —— 只看该状态
        due_before   : "2026-10-10"        —— 截止日在该日期及以前
        due_after    : "2026-10-01"        —— 截止日在该日期及以后
        overdue_only : True                —— 只看已逾期的任务
        """
        # 获取今天的日期
        today = datetime.date.today().strftime("%Y-%m-%d")
        result = []

        for t in self._task_list:
            keep = True                      # 先假设保留，任一条件不满足就置 False
            due = to_date_str(t.deadline)    # 截止日期统一转成文本再比较

            # 条件1：优先级
            if priority is not None:
                if t.priority != priority:
                    keep = False

            # 条件2：状态
            if keep and status is not None:
                if t._status != status:
                    keep = False

            # 条件3：截止日不晚于 due_before（YYYY-MM-DD 定长，可直接比字符串）
            if keep and due_before is not None:
                if due > due_before:
                    keep = False

            # 条件4：截止日不早于 due_after
            if keep and due_after is not None:
                if due < due_after:
                    keep = False

            # 条件5：只看逾期（未完成 且 截止日早于今天）
            if keep and overdue_only:
                is_over = (t._status != "已完成") and (due < today)
                if not is_over:
                    keep = False

            if keep:
                result.append(t)             # 全部条件通过才收集

        return result

     #按优先级排序查看（高→中→低，同级按截止日期升序）
    def view_by_priority(self):
        if not self._task_list:                     #判断列表是否为空
            print("暂时没有可管理的任务")
            return

        # 用字典把中文优先级映射成数字，便于排序（高=1 在前）
        rank = {"高": 1, "中": 2, "低": 3}
        today = datetime.date.today().strftime("%Y-%m-%d")

        # sorted 返回新列表，不改动 self._task_list
        # key 用元组：先按优先级排名，再按截止日期；优先级相同的截止早的在前
        sorted_tasks = sorted(
            self._task_list,
            key=lambda t: (rank.get(t.priority, 99),
                           to_date_str(t.deadline))
        )

        print("--- 按优先级排序（高→中→低） ---")
        for t in sorted_tasks:
            print(t)

    #按截止日期排序查看（早→晚，相同日期按优先级高→低）
    def view_by_deadline(self):
        if not self._task_list:                     #判断列表是否为空
            print("暂时没有可管理的任务")
            return

        # 优先级作为第二排序键，让截止日相同的任务也能区分先后
        rank = {"高": 1, "中": 2, "低": 3}
        today = datetime.date.today().strftime("%Y-%m-%d")

        # 空截止日（""）排到最后：用 ("1", "") 这种哨兵值
        # 实际就是把没有截止日的任务丢到列表尾
        sorted_tasks = sorted(
            self._task_list,
            key=lambda t: (
                "1" if to_date_str(t.deadline) == "" else "0",
                to_date_str(t.deadline) if to_date_str(t.deadline) != "" else "9999-12-31",
                rank.get(t.priority, 99),
            )
        )

        print("--- 按截止日期排序（早→晚） ---")
        for t in sorted_tasks:
            print(t)