import importlib
import queue
import os
import random
from time import sleep
from threading import Thread
import threading
from datetime import datetime


# configuration Variables

Queue_Size = 3
tasks_path = './tasks'
all_tasks = dict()  # completed and uncompleted
completed_task = dict()
main_lock = threading.Lock()

processing_queue = queue.Queue(Queue_Size)  # creating global instance of the queue


#this function is responsible for executing the tasks in the queue
def process_next_task(myQueue,tasks_list):#consumer
    while True:
        if not myQueue.empty():
            #print('performing a task')
            #print(list(myQueue.task_queue.queue))
            #critical section
            main_lock.acquire()
            task_function = myQueue.get()  # poping the top of the queue
            tasks_list[task_function][0]=1
            main_lock.release()
            if task_function:
                task_to_process(task_function)
                myQueue.task_done()
            


#this function is responsible for importing the new tasks or already one from tasks folder
def get_all_tasks(myQueue,tasks_list): #producer
    while True:
        for file_path in os.listdir(tasks_path):
            # check if current file_path is a file
            if os.path.isfile(os.path.join(tasks_path, file_path)):
                # add filename to list
                if not tasks_list.get(file_path):  # it's new uncompleted task
                    #print("adding the task to queue for the first time" , file_path)
                    main_lock.acquire()
                    tasks_list[file_path] = [0, file_path]
                    main_lock.release()
                    myQueue.put(file_path)
                    print("tasks in queue")
                    print(list(myQueue.queue))
                    

       





def task_to_process(taskname):
    try:
        
        with open("./tasks/" + taskname) as f:
            exec(f.read())
    except:
        print("error on task to process")


def main():
    try:
        # two threads one for importing the tasks from the file and the other to execute
        importing_thread = Thread(target=get_all_tasks, args=(processing_queue,all_tasks,))
        importing_thread.start()

        processing_thread = Thread(target=process_next_task, args=(processing_queue,all_tasks,))

        processing_thread.start()
        #killing the threads after two minutes
        importing_thread.join(120)
        processing_thread.join(120)
        
        print('done')
        print(all_tasks)

        return 0
    except:
        print('error')
        return -1


if __name__ == '__main__':
    main()
