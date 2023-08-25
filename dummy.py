import threading
import time
import random
def worker_function(thread_id):
    a= random.randint(2,10)
    print(f"Thread {thread_id} - value of a = {a}")
    time.sleep(5)
    print(f"Thread {thread_id} - value of a = {a}")
    
    

# Create two threads, each working on the same function
thread1 = threading.Thread(target=worker_function, args=(1,))
thread2 = threading.Thread(target=worker_function, args=(2,))

# Start the threads
thread1.start()
thread2.start()

# Wait for both threads to finish
thread1.join()
thread2.join()

print("Both threads have finished.")
