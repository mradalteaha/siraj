from time import sleep
import random
from datetime import datetime

def task():

    now = datetime.now()

    current_time = now.strftime("%H:%M:%S")
    print('task 3 started at',current_time)
    sleeptime = random.randint(5,20)
    print('approximate time to complete ', str(sleeptime), ' seconds')
    sleep(sleeptime)
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")

    print('task 3 compleated at',current_time)

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    task()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
