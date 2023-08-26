# Scheduling problem

## configuration Variables

    `Queue_Size`= this variable is for the amount of tasks that can be at the queue at the same time .
    `tasks_path` = this variable for the tasks folder path where you can add the scripts for execution , you can add them while the program is running.
    `consumers_num` = this variable belongs to section B , where you can define the amount of tasks to run in parallel .
    `all_tasks` = dictionary to keep tracking of completed and uncompleted {'name_of_the_file':[status,'name_of_the_file']}
    `time_to_run` = this variable to determine for how long you want the program to listen for new changes in the tasks folder

## section A explanation

    in this section i have used multithreading , it's devided into 3 main pieces ,
    **1.**: `producer thread`
        we have the fucntion (`get_all_tasks`) which work like websocket and 
        keep searching the tasks directory for new tasks . 
        if it finds any it will add it into the queue if there is available spot if not , it will wait.

    **2.**: `consumer thread`
        the other function is `process_next_task` which responsible for dequeue task from the queue and processing it using `execv()`
        and once it done it marks it it `all_tasks` with value of `1`
        
    **3.**:
        main thread that wait's for the two other to finish and then closing them .

## section B explanation

    similar to section A but instead of using one thread for managin the queue and perform the task i'm using multiple based on configuration variable .

    i have used producer consumer design for both sections with taking care of shared resources between threads using locks and free and built in feautures
    for syncronization. 

## section C

    testing the behavior of the functions and see if it's matching the expected results using assertion.

## general idea of solution

    i have choosen this pattern to simulate CPU scheduling algorithm for first come first served.
    and choose the directory tasks option because i wanted to work on local environment for the solution but it can be extended to http request by 
    adding it to the task file it self and will be executed there .
