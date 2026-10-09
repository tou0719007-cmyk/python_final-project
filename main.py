from task_manager import SystemManager
from report import generate_html_report

def main():#主函数，提供任务管理系统的菜单界面
    manager = SystemManager()

    while True:
        print("\n===== Python任务管理系统 =====")
        print("1. 添加任务")
        print("2. 查看任务")
        print("3. 标记完成")
        print("4. 删除任务")
        print("5. 搜索任务")
        print("6. 筛选任务")
        print("7. 统计任务")
        print("8. 导出报告")
        print("9.  保存   ")
        print("0.  退出   ")
        print("===============================")
        
        choice = input("请选择要执行的操作，输入0~9：")
        match choice:
            case "1":#添加任务
                manager.add_task()
            case "2":#查看任务
                manager.view_tasks()
            case "3":#标记完成
                manager.complete_task()
            case "4":#删除任务
                manager.delete_task()
            case "5":#搜索任务
                manager.search_task()
            case "6":#筛选任务
                manager.filter_tasks()
            case "7":#统计任务
                manager.statistics()
            case "8":#导出报告
                generate_html_report(manager._task_list)
            case "9":#保存任务
                manager.save_task()
                print("任务已保存。")
            case "0":
                print("程序已退出。")
                break
            case _:#其他情况
                print("输入无效，请重新选择!")


if __name__ == "__main__":
    main()