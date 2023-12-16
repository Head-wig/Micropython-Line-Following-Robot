import task_share
import cotask
import gc

from appa_brain import appa_brain # controller Task
# from appa_return import appa_return # Predicting what path to take

Appa_Mode = task_share.Share('f',"Appa's Mode")
Left_Wheel_RPM = task_share.Share('f',"RPM of the left wheel")
Right_Wheel_RPM = task_share.Share('f',"RPM of the Right wheel")
X_Distance = task_share.Share('f',"appa x distance away form the finish line")
Y_Distance = task_share.Share('f',"appa x distance away form the finish line")
DEBUG_VAL = task_share.Share('f', "Intertask Debug Value") # Giv Debug


# Create an object to pass in the cotask
CONT = appa_brain(Appa_Mode, Left_Wheel_RPM, Right_Wheel_RPM, X_Distance, Y_Distance, DEBUG_VAL)
# RETURN = appa_return(Appa_Mode, Left_Wheel_RPM, Right_Wheel_RPM, X_Distance, Y_Distance, DEBUG_VAL)

# Put the object into the cotask 
CONT_cotask = cotask.Task(CONT.run, "appa's brain", priority = 1, period = 25)
# RETURN_cotask = cotask.Task(RETURN.run, "appa returns home", priority = 0, period = 2)

# Append the newly created task to the task list

cotask.task_list.append(CONT_cotask)
# cotask.task_list.append(RETURN_cotask)

# Run the scheduler
while True:
    cotask.task_list.pri_sched()
        




