import pickle
import task
import task_manager

def save_task(task_list):
    temp=open("data.txt", 'wb') 
    data=task_list
    pickle.dump(data, temp)  #覆盖式更新文件
    temp.close()

def load_task():
    temp=open("data.txt", 'rb')
    data=pickle.load(temp)
    temp.close()
    return data
