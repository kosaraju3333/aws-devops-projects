import boto3
import time
from datetime import date
from pprint import pprint

def lambda_handler(event, context):
    # Get today's date
    today_date = date.today().strftime('%d-%m-%Y')

    ## Open AWS console session
    iam_console = boto3.Session(profile_name='boto3-user')

    ## Connect to EC2 Console
    ec2_console_client = iam_console.client(service_name='ec2',region_name='us-east-1')

    # Define tag filter
    filters = [
        {
            'Name': 'tag:Expiry_Date',  # Replace with your tag key
            'Values': ['*']            # Replace with your tag value
        },
        {
            'Name': 'instance-state-name',
            'Values': ['running']
        }
    ]

    expired_ec2 = []
    expire_ec2_tomorrow = []
    list_ec2_instances = ec2_console_client.describe_instances(Filters=filters)['Reservations']
    for ec2_instance in list_ec2_instances:
        for instance_id in ec2_instance['Instances']:
            vm_id = instance_id['InstanceId']
            for tag in instance_id['Tags']:
                if tag['Key'] == 'Expiry_Date':
                    vm_expirey_date = tag['Value']
                    if vm_expirey_date == today_date:
                        expire_ec2_tomorrow.append(vm_id)
                    if vm_expirey_date < today_date:
                        expired_ec2.append(vm_id)

    if expired_ec2 == []:
        print(f"Currently There are No Expired Instance....")
    else:
        for ec2_id in expired_ec2:
            print(f"Terminating Expired {ec2_id} EC2 Instance...")
            ec2_console_client.terminate_instances(InstanceIds=[vm_id])
            time.sleep(100)
        print(f"Here is the list of Terminated Expired Instancees...")
        print(expired_ec2)
            
    print(f"*** Warning below list of EC2 Instances are not available form Tomorrow 10AM IST ***")
    print(expire_ec2_tomorrow)