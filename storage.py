import pickle
import task

def save_task():
    temp=open("data.txt", 'wb') 
    data=task.task_list
    pickle.dump(data, temp)  #覆盖式更新文件
    temp.close()

def load_task():
    temp=open("data.txt", 'rb')
    data=pickle.load(temp)
    temp.close()
    return data
