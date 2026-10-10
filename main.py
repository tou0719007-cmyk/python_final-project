from task_manager import SystemManager
from report import generate_html_report
import chart

def main():#主函数，提供任务管理系统的菜单界面
    manager = SystemManager()
    whether_changed=False #定义一个变量来跟踪任务列表是否已保存，初始值为False，表示未保存
    while True:
        print("\n===== Python任务管理系统 =====")
        print("         1. 添加任务            ")
        print("         2. 查看任务            ")
        print("         3. 标记完成            ")
        print("         4. 删除任务            ")
        print("         5. 搜索任务            ")
        print("         6. 筛选任务            ")
        print("         7. 统计任务            ")
        print("         8. 导出报告            ")     
        print("         9.  保存               ")
        print("        10. 生成图表            ")
        print("         0.  退出               ")
        print("===============================")
        
        choice = input("请选择要执行的操作，输入0~10：").strip()#去掉首尾空格
        match choice:
            case "1":#添加任务

                manager.add_task()

                whether_changed=True

            case "2":#查看任务

                manager.view_tasks()

                whether_changed=True

            case "3":#标记完成

                manager.complete_task()

                whether_changed=True

            case "4":#删除任务

                manager.delete_task()

                whether_changed=True

            case "5":#搜索任务

                keyword = input("请输入要搜索的任务标题关键词：").strip()#删去输入的内容首位所含空格
                result = manager.search_tasks(keyword)

                #输出搜索结果
                if result:#如果搜索结果不为空
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
                    elif choice == "4":#其实就是搜索功能
                        keyword = input("请输入任务标题关键词：").strip()#删去输入的内容首位所含空格
                        result = manager.search_tasks(keyword)

                    # 按优先级排序查看
                    elif choice == "5":
                        manager.view_by_priority()
                        continue # 直接返回主菜单，不需要再显示结果

                    # 按截止日期排序查看
                    elif choice == "6":
                        manager.view_by_deadline()
                        continue # 直接返回主菜单，不需要再显示结果

                    # 返回主菜单
                    elif choice == "0":
                        continue

                    # 处理无效输入
                    else:
                        print("你输的不对，重输！")
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
                whether_changed=False

            case "10":#生成图表
                chart.chart(manager.get_tasks())

            case "0":
                if whether_changed:#如果任务列表有修改但未保存，提示用户是否保存
                    print("貌似还没有保存任务，是否保存？(yes/no)")
                    save_choice = input().strip().lower()
                    if save_choice == 'yes':
                        manager.save_task()
                        print("任务已保存。")
                
                print("欢迎下次使用，byebye~")
                break

            case _:#其他情况

                print("你输的输入有误，请重输!")


if __name__ == "__main__":
    main()