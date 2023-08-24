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
consumers_num = 5
all_tasks = dict()  # completed and uncompleted
completed_task = dict()


class TaskQueue:
    def __init__(self):
        self.task_queue = queue.Queue()
        self.is_processing = False
        self.max_size = Queue_Size
        self.current_tasks = 0
        self.waiting_queue = queue.Queue()
        self.lock = threading.Lock()

    def enqueue_task(self, task_function):
        with self.lock:

            if self.current_tasks < self.max_size:
                self.task_queue.put(task_function)
                self.current_tasks = self.current_tasks + 1
                print("\nprinting task on queue")
                print(list(self.task_queue.queue))
            elif self.current_tasks >= self.max_size:
                self.waiting_queue.put(task_function)
                print("\nprinting task on waiting")
                print(list(self.waiting_queue.queue))

    def enqueue_waiting_task(self, task_function):
        with self.lock:
            self.waiting_queue.put(task_function)


processing_queue = TaskQueue()  # creating global instance of the queue


#this function is responsible for executing the tasks in the queue
def process_next_task(myQueue):
    print('\nprocessing tasks\n')
    if not myQueue.task_queue.empty():
        with threading.Lock():
            task_function = myQueue.task_queue.get()  # poping the top of the queue
            myQueue.current_tasks = myQueue.current_tasks - 1
            if task_function:
                task_to_process(task_function)

            # the task in the top of the queue is done

        if not myQueue.waiting_queue.empty():
            myQueue.enqueue_task(myQueue.waiting_queue.get())
        process_next_task(myQueue)


#this function is responsible for importing the new tasks or already one from tasks folder
def get_all_tasks(myQueue):
    while True:
        for file_path in os.listdir(tasks_path):
            # check if current file_path is a file
            if os.path.isfile(os.path.join(tasks_path, file_path)):
                # add filename to list
                if not all_tasks.get(file_path):  # it's new uncompleted task

                    all_tasks[file_path] = [0, file_path]
                if all_tasks.get(file_path) and all_tasks.get(file_path)[0] == 0:
                    all_tasks[file_path][0] = 1

                    myQueue.enqueue_task(file_path)  # the task either being handled or in waiting queue
                    #print(list(processing_queue.task_queue.queue))

        sleep(5)


def task_to_process(taskname):
    with open("./tasks/" + taskname) as f:
        exec(f.read())
    all_tasks[taskname][0] = 1


def main():
    try:
        # two threads one for importing the tasks from the file and the other to execute
        importing_thread = Thread(target=get_all_tasks, args=(processing_queue,)) # producer
        importing_thread.start()
        threads = []
        for _ in range(consumers_num): #consumers
            thread = Thread(target=process_next_task, args=(processing_queue,))
            threads.append(thread)
            thread.start()

        # Wait for all threads to complete
        for thread in threads:
            thread.join(130)


        #killing the threads after two minutes
        importing_thread.join(120)
        print('\ndone')

        return 0
    except:
        print('error')
        return -1


if __name__ == '__main__':
    main()
