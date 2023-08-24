Scheduling problem : 
section A explanation , 
in this section i have used multithreading , it's devided into 3 main pieces , first we have the fucntion (get_all_tasks) which had a loop than runs 
every 5 seconds to check if there is a new files added to the folder , if it found any it will add it into a dict which responsiable to flag if the task
handled before or not and saves the file name , if it's not it will go into processing queue , where i check if it's maxed out i move it into another 
queue called waiting queue , when the processing queue get's empty place i fill it from the waiting queue , and perform the task on the head of the processing
queue based on FIFO standard .
it's using two threads , one for the (get_all_tasks ) 
and another for managing the queue and performin the relevant task . 

section B explanation : 
similar to section A but instead of using one thread for managin the queue and perform the task i'm using multiple based on configuration variable .

i have used producer consumer design for both sections with taking care of shared resources between threads using locks and free . 

section C :
testing the class of the Queue