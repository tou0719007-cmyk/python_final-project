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

                keyword = input("请输入要搜索的任务标题关键词：").strip()#删去输入的内容首位所含空格
                result = manager.search_tasks(keyword)

                #输出搜索结果
                if result:
                    print("搜索结果：")
                    for t in result:
                        print(t)
                else:
                    print("没有找到符合条件的任务。")

            
            case "6":  # 筛选任务

                print("\n===== 筛选任务 =====")
                print("1. 只看未完成任务")
                print("2. 只看已完成任务")
                print("3. 只看已逾期任务")
                print("4. 按关键字搜索")
                print("5. 按优先级排序查看")
                print("6. 按截止日期排序查看")
                print("0. 返回主菜单")

                # 获取用户选择
                choice = input("请选择操作（0~6）：").strip()

                # 只看未完成任务
                if choice == "1":
                    result = manager.filter_tasks(status="未完成")

                # 只看已完成任务
                elif choice == "2":
                    result = manager.filter_tasks(status="已完成")

                # 只看已逾期任务
                elif choice == "3":
                    result = manager.filter_tasks(overdue_only=True)

                # 按关键字搜索
                elif choice == "4":
                    keyword = input("请输入任务标题关键词：").strip()
                    result = manager.search_tasks(keyword)

                # 按优先级排序查看
                elif choice == "5":
                    result = manager.filter_tasks()
                    priority_order = {"高": 0, "中": 1, "低": 2}
                    result.sort(key=lambda t: priority_order.get(t.priority, 3))

                # 按截止日期排序查看
                elif choice == "6":
                    result = manager.filter_tasks()
                    result.sort(key=lambda t: t.deadline)

                # 返回主菜单
                elif choice == "0":
                    continue

                # 处理无效输入
                else:
                    print("输入无效，请重新选择！")
                    continue

                # 显示结果
                if result:
                    print("\n处理结果：")
                    for t in result:
                        print(t)
                else:
                    print("没有符合条件的任务。")


            case "7":#统计任务

                stat = manager.statistics()
                print(f"任务总数：{stat['total']}")
                print(f"已完成：{stat['done']}")
                print(f"未完成：{stat['undone']}")
                print(f"已逾期：{stat['overdue']}")
                print(f"完成率：{stat['rate']:.2f}%")
                print(f"高优先级：{stat['high']}")
                print(f"中优先级：{stat['mid']}")
                print(f"低优先级：{stat['low']}")

            case "8":#导出报告

             
                generate_html_report(manager.get_tasks())

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