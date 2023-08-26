import unittest
from unittest.mock import patch
import os
from io import StringIO
import sys
import threading
import queue
from threading import Thread
from time import sleep
from datetime import datetime

# Import functions from your script
from main import get_all_tasks, process_next_task, task_to_process
Queue_Size = 3
tasks_path ='./tasks'
class TestScript(unittest.TestCase):
    
    def test_get_all_tasks(self):

        myQueue = queue.Queue(Queue_Size)
        tasks_list = {}
        lock = threading.Lock()



        # Create some mock files in the tasks folder for testing
        os.makedirs(tasks_path, exist_ok=True)
        with open(os.path.join(tasks_path, 'test_task1'), 'w') as f:
            f.write("print('Task 1 executed')")
        with open(os.path.join(tasks_path, 'test_task2'), 'w') as f:
            f.write("print('Task 2 executed')")
            

        # Run the function being tested
        with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
 

            importing_thread = Thread(target=get_all_tasks, args=(myQueue,tasks_list,lock,))
            importing_thread.start()

            processing_thread = Thread(target=process_next_task, args=(myQueue,tasks_list,lock,))

            processing_thread.start()
        
            importing_thread.join(30)
            processing_thread.join(30)
            
            if importing_thread.is_alive():
                importing_thread.join()
            if processing_thread.is_alive():
                processing_thread.join()    

        # Assert that tasks were added to the queue and printed to stdout
        print('done')
        self.assertEqual(myQueue.qsize(), 0)
        
        self.assertIn("test_task1  started at", mock_stdout.getvalue())
        self.assertIn("test_task2  started at", mock_stdout.getvalue())

        # Clean up: delete the mock files
        os.remove(os.path.join(tasks_path, 'test_task1'))
        os.remove(os.path.join(tasks_path, 'test_task2'))

        

    def test_task_to_process(self):
        # Capture stdout to check the printed output
        print("test_task_to_process")
        captured_output = StringIO()
        sys.stdout = captured_output

        # Create a mock task file
        task_code = "print('Task executed')"
        with open(os.path.join(tasks_path, 'mock_task'), 'w') as f:
            f.write(task_code)

        # Run the function being tested
        task_to_process('mock_task')

        # Restore stdout
        sys.stdout = sys.__stdout__
        print(captured_output.getvalue())

        # Assert that the task was executed and printed its output
        self.assertIn("Task executed", captured_output.getvalue())

        # Clean up: delete the mock task file
        os.remove(os.path.join(tasks_path, 'mock_task'))

    # Add more test cases for other functions if needed

if __name__ == '__main__':
    unittest.main()