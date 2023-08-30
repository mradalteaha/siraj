import importlib
import queue
import os
import random
from time import sleep
from threading import Thread
import threading
from datetime import datetime
import time
import logging
from config import  tasks_path ,consumers_num , Queue_Size , time_to_run

# configuration Variables
all_tasks = dict()
main_lock = threading.Lock()

t_end = time.time() + 60 * time_to_run


processing_queue = queue.Queue(Queue_Size)  # creating global instance of the queue




def process_next_task(myQueue,tasks_list,lock):#consumer
    '''this function is responsible for executing the tasks in the queue'''
    while time.time() < t_end:
        if not myQueue.empty():
            #critical section
            lock.acquire()
            thread_local_data = threading.local()
            thread_local_data.task = myQueue.get()  # poping the top of the queue
            tasks_list[thread_local_data.task][0]=1
            lock.release()
            if thread_local_data.task:
                lock.acquire()
                thread_local_data.now = datetime.now()
                thread_local_data.current_time = thread_local_data.now.strftime("%H:%M:%S")
                print(thread_local_data.task,' started at ',thread_local_data.current_time)
                lock.release()
                task_to_process(thread_local_data.task)
                lock.acquire()
                thread_local_data.now = datetime.now()
                thread_local_data.current_time = thread_local_data.now.strftime("%H:%M:%S")
                print(thread_local_data.task,' completed ',thread_local_data.current_time)
                lock.release()

                myQueue.task_done()
       
        
            

#this function is responsible for importing the new tasks or already one from tasks folder
def get_all_tasks(myQueue,tasks_list,lock): #producer
    '''this function import the scripts from the directory and put it in the queue if there is 
    available spot'''
    while time.time() < t_end:
        for file_path in os.listdir(tasks_path):
            if os.path.isfile(os.path.join(tasks_path, file_path)):
                if not tasks_list.get(file_path):  # it's new uncompleted task
                    tasks_list[file_path] = [0, file_path]
                    myQueue.put(file_path)
        
                    

def task_to_process(taskname):
    '''this function takes the script name and execute it '''
    try:
        
        with open(os.path.join(tasks_path, taskname)) as f:
            exec(f.read())
    except OSError:
        logging.error("error on task to process unable to open file")


def main():
    try:
        # two threads one for importing the tasks from the file and the other to execute
        importing_thread = Thread(target=get_all_tasks, args=(processing_queue,all_tasks,main_lock,)) # producer
        importing_thread.start()
        threads = []
        for _ in range(consumers_num): #consumers
            thread = Thread(target=process_next_task, args=(processing_queue,all_tasks,main_lock,))
            threads.append(thread)
            thread.start()
            
        #killing the threads after two minutes
        importing_thread.join(time_to_run*60)
        # Wait for all threads to complete
        for thread in threads:
            thread.join(time_to_run*120)



        print('\ndone ! all tasks completed !!',all_tasks)


        return 0
    except:
        print('error')
        return -1


if __name__ == '__main__':
    main()
