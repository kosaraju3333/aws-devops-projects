#########################################################################################################
#                                                                                                       #
#   Script: ASG Scale-Up and Scheduled Scale-Down Automation                                            #
#                                                                                                       #
#   Description:                                                                                        #
#   This script automates the process of scaling up an AWS Auto Scaling Group (ASG) for a release       #
#   and schedules it to scale back down after a defined time (default: 10 minutes).                     #
#                                                                                                       #
#   Workflow:                                                                                           #
#   1. Fetches the current MaxSize, MinSize, and DesiredCapacity of the target ASG                      #
#      and stores them in a dictionary called `asg_current_state`.                                      #
#   2. Calculates doubled values for these parameters and stores them in `asg_new_state`.               #
#   3. Updates the ASG with values from `asg_new_state` to scale up the group immediately.              #
#   4. Creates a scheduled action that will scale the ASG back down to its original                     #
#      values (from `asg_current_state`) after 5 minutes, using the TimeZone 'Asia/Kolkata'.            #
#                                                                                                       #
#   Use Case:                                                                                           #
#   Ideal for temporarily scaling up an ASG during deployments or high-traffic periods,                 #
#   then reverting automatically to save cost and maintain performance efficiency.                      #
#                                                                                                       #
#########################################################################################################

import boto3
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
from pprint import pprint

## Add ASG names to the below list
asg_list = ['Bnak-app-ASG', 'portal-app-ASG']

# Get the current date and time
current_datetime = datetime.now(ZoneInfo("Asia/Kolkata"))
start_time_after_10_min = current_datetime + timedelta(minutes=10)

def asg_scaleUp(asg_names):
    client = boto3.client('autoscaling')
    for asg_name in asg_names:
        response = client.describe_auto_scaling_groups(
            AutoScalingGroupNames=[
                asg_name
            ]
        )['AutoScalingGroups']

        ### Get the current state of ASG
        for asg_state in response:
            asg_current_state = {"Desired_count" : asg_state['DesiredCapacity'], "Max_count" : asg_state['MaxSize'], "Min_count" : asg_state['MinSize'] }
            # print(f'{asg_name} ASG curent state {asg_current_state}')
            ### Get the new state of ASG
            asg_new_state = {}
            for key, value in asg_current_state.items():
                # print(f'{key} : {value}')
                asg_new_state[key] = value *2
            # print(f'{asg_name} ASG NEW state {asg_new_state}')
            # print()

            ### Update the ASG with New state
            response = client.update_auto_scaling_group(
                AutoScalingGroupName=asg_name,
                MinSize=asg_new_state['Min_count'],
                MaxSize=asg_new_state['Max_count'],
                DesiredCapacity=asg_new_state['Desired_count']
            )

            ### Adding Scheduled Action to ASG
            response = client.put_scheduled_update_group_action(
                AutoScalingGroupName=asg_name,
                ScheduledActionName=f"{asg_name}_ScheduleAction",
                StartTime=start_time_after_10_min,
                MinSize=asg_current_state['Min_count'],
                MaxSize=asg_current_state['Max_count'],
                DesiredCapacity=asg_current_state['Desired_count'],
                TimeZone='Asia/Kolkata'
            )

run_flag = True
if run_flag:
    asg_scaleUp(asg_list)
else:
    print("asg_scaleUp() was skipped.")
