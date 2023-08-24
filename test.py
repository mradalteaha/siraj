import unittest
import threading
from main import TaskQueue, get_all_tasks, task_to_process ,process_next_task


class TestTaskQueue(unittest.TestCase):
    def setUp(self):
        self.task_queue = TaskQueue()

    def test_enqueue_task(self):
        self.task_queue.enqueue_task("task1.py")
        self.assertEqual(self.task_queue.task_queue.qsize(), 1)

    def test_process_next_task(self):
        self.task_queue.enqueue_task("task1.py")
        self.task_queue.enqueue_task("task2.py")

        def mock_task_function():
            pass

        self.task_queue.task_queue.get = lambda: mock_task_function

        process_thread = threading.Thread(target=process_next_task)
        process_thread.start()
        process_thread.join()

        self.assertEqual(self.task_queue.task_queue.qsize(), 1)


# Define more tests for other functions/classes

if __name__ == '__main__':
    unittest.main()
