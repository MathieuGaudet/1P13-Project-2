## ----------------------------------------------------------------------------------------------------------
## TEMPLATE
## Please DO NOT change the naming convention within this template. Some changes may
## lead to your program not functioning as intended.

import sys
import random
sys.path.append('../')

from Common_Libraries.p2_sim_lib import *

import os
from Common_Libraries.repeating_timer_lib import repeating_timer

def update_sim ():
    try:
        arm.ping()
    except Exception as error_update_sim:
        print (error_update_sim)

arm = qarm()
update_thread = repeating_timer(2, update_sim)

#---------------------------------------------------------------------------------
# STUDENT CODE BEGINS
#---------------------------------------------------------------------------------
numberOfBlocks = 1

#global variables and constants
containerID = [1,2,3,4,5,6]
random.shuffle(containerID)
gripperOpened = True
#the coordinates for 6 different positions of autoclaves that can be accessed (x,y,z)
RedSmall = [-0.596,0.241,0.412] 
GreenSmall = [-0.001,-0.644,0.467] 
BlueSmall = [0.001, 0.644, 0.467]
RedLarge = [-0.395,0.143,0.308] 
GreenLarge = [0.0, -0.42,0.308]
BlueLarge = [0.0,0.42,0.308]
PickUp = [0.532,0.0,0.06]


def move_end_effector(xPosition, yPosition, zPosition):
  endEffectorMoved = False
  while(not endEffectorMoved): # Wait for the user to input the left arm up for the function to run
    if((arm.emg_left()>0.2)and(arm.emg_right()<0.2)):
      arm.move_arm(xPosition,yPosition,zPosition) # Move the end effector to the enclave position
      endEffectorMoved = True

def activate_control_gripper():
  commandExecuted = False
  global gripperOpened
  while(not commandExecuted): # Wait for the user to input right arm up for the function to run
    if((arm.emg_left()<0.2)and(arm.emg_right()>0.2)):
      if(gripperOpened): # if the gripper is opened, close it.
        arm.control_gripper(35)  
        gripperOpened = False
      else: # if it isn't opened, then it is closed so open it
        arm.control_gripper(-35)
        gripperOpened = True
      commandExecuted = True

def open_autoclave_bin_drawer(containerID):
  if(containerID==4 or containerID==5 or containerID==6): # If it's not a large container, skip this function
    autoclaveOpened = False
    while(not autoclaveOpened):
    # Wait for the user to input right arm up and left arm up for the function to run
    
      if((arm.emg_left()>0.2)and(arm.emg_right()>0.2)): 
        # Open enclave corresponding to container ID
        if(containerID==4):
          arm.open_red_autoclave(True)
        elif(containerID==5):
          arm.open_green_autoclave(True)
        elif(containerID==6):
          arm.open_blue_autoclave(True)
        autoclaveOpened = True

def identify_autoclave(a):
    
    if a == 1: #Check if container ID is 1
        return RedSmall  
    elif a == 2:
        return GreenSmall
    elif a == 3:
        return BlueSmall
    elif a == 4:
        return RedLarge
    elif a == 5:
        return GreenLarge
    elif a == 6:
        return BlueLarge #each elif statement just runs the same three functions for each a value
    else: #if the value isn't a container ID, simply state that it is invalid
        print("Container ID invalid.") 

while(numberOfBlocks<=6): #runs once for each container
    arm.home()
    time.sleep(1)
    gripperOpened = True 
    arm.spawn_cage(containerID[numberOfBlocks-1]) # generates a container
    time.sleep(1)
    xCoordinate, yCoordinate, zCoordinate = identify_autoclave(containerID[numberOfBlocks-1])
    arm.move_arm(PickUp[0],PickUp[1],PickUp[2]) #not sure if this should be move_ende effector instead
    time.sleep(1)
    activate_control_gripper()
    open_autoclave_bin_drawer(containerID[numberOfBlocks-1])#opens the drawer to let the block drop in
    move_end_effector(xCoordinate,yCoordinate,zCoordinate) # move to enclave
    activate_control_gripper() #drop in enclave
    time.sleep(1)
    if(containerID[numberOfBlocks-1]==4):
        arm.open_red_autoclave(False)
    if(containerID[numberOfBlocks-1]==5):
        arm.open_green_autoclave(False)
    if(containerID[numberOfBlocks-1]==6):
        arm.open_blue_autoclave(False)
    numberOfBlocks+=1
#close each enclave





#---------------------------------------------------------------------------------
# STUDENT CODE ENDS
#---------------------------------------------------------------------------------
