import importlib
import queue
import os
import random
from time import sleep
from threading import Thread
import threading
from datetime import datetime
import time



# configuration Variables

Queue_Size = 3
tasks_path = './tasks'
all_tasks = dict()  # completed and uncompleted {'name_of_the_file':[status,'name_of_the_file']}
main_lock = threading.Lock()
time_to_run = 3
t_end = time.time() + 60 * time_to_run

processing_queue = queue.Queue(Queue_Size)  # creating global instance of the queue


#this function is responsible for executing the tasks in the queue
def process_next_task(myQueue,tasks_list,lock):#consumer
    try:
        while time.time() < t_end:
            if not myQueue.empty():
                #critical section
                lock.acquire()
                task_function = myQueue.get()  # poping the top of the queue
                tasks_list[task_function][0]=1
                lock.release()
                if task_function:
                    now = datetime.now()

                    current_time = now.strftime("%H:%M:%S")
                    print(task_function,' started at ',current_time)
                    task_to_process(task_function)
                    now = datetime.now()
                    current_time = now.strftime("%H:%M:%S")
                    print(task_function,' completed ',current_time)
                    myQueue.task_done()
        return 0
    except:
        print("error on processing task")
        return -1             

#this function is responsible for importing the new tasks or already one from tasks folder
def get_all_tasks(myQueue,tasks_list,lock): #producer
    try:
        while time.time() < t_end:
            for file_path in os.listdir(tasks_path):
                # check if current file_path is a file
                if os.path.isfile(os.path.join(tasks_path, file_path)):
                    # add filename to list
                    if not tasks_list.get(file_path):  # it's new uncompleted task
                        lock.acquire()
                        tasks_list[file_path] = [0, file_path]
                        lock.release()
                        myQueue.put(file_path)
        return 0
    except:
        print("error on task to process unable to open file")
        return -1

def task_to_process(taskname):
    try:
        
        with open(os.path.join(tasks_path, taskname)) as f:
            exec(f.read())
    except OSError:
        print("error on task to process unable to open file")


def main():
    try:
        # two threads one for importing the tasks from the file and the other to execute
        importing_thread = Thread(target=get_all_tasks, args=(processing_queue,all_tasks,main_lock,))
        importing_thread.start()

        processing_thread = Thread(target=process_next_task, args=(processing_queue,all_tasks,main_lock,))

        processing_thread.start()
        #killing the threads after two minutes
        importing_thread.join(time_to_run*60)
        processing_thread.join(time_to_run*60)
        
        if importing_thread.is_alive():
            importing_thread.join()
        if processing_thread.is_alive():
            processing_thread.join()
        
        print('done')
        print(all_tasks)

        return 0
    except:
        print('error')
        return -1


if __name__ == '__main__':
    main()
