import boto3
import json
import time
from datetime import date
from pprint import pprint

def lambda_handler(event, context):
    # Get today's date
    today_date = date.today().strftime('%d-%m-%Y')

    ## Open AWS console session
    iam_console = boto3.Session()
    # iam_console = boto3.Session(profile_name='boto3-user')
    

    ## Connect to EC2 Console
    ec2_console_client = iam_console.client(service_name='ec2',region_name='us-east-1')

    ## Connect to SNS Console
    sns_console_client = iam_console.client(service_name='sns',region_name='us-east-1')

    sns_topic_arn = 'arn:aws:sns:us-east-1:Account-ID:spontansolutions-EMAIL'


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
    terminated_ec2 = []
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

    print(f"Here is the list of Expired Instances That are going to terminate ...")
    print(expired_ec2)


    if expired_ec2 == []:
        print(f"Currently There are No Expired Instance....")
    else:
        for ec2_id in expired_ec2:
            print(f"Terminating Expired {ec2_id} EC2 Instance...")
            ec2_console_client.terminate_instances(InstanceIds=[ec2_id])
            time.sleep(10)
            terminated_ec2.append(ec2_id)
        time.sleep(100)
        print(f"Here is the list of Terminated Expired Instancees...")
        print(terminated_ec2)
            
    print(f"*** Warning below list of EC2 Instances are not available form Tomorrow 12AM IST ***")
    print(expire_ec2_tomorrow)

    # Create a detailed message
    message = f"""🚨 EC2 Termination Report – {today_date}

    ✅ Terminated Instances:
    {chr(10).join(terminated_ec2) if terminated_ec2 else 'None'}

    ⚠️ Expiring Soon (Today at Midnight):
    {chr(10).join(expire_ec2_tomorrow) if expire_ec2_tomorrow else 'None'}

    Regards,
    EC2 Auto-Termination Lambda
    """

    # Publish message to SNS topic
    sns_message=sns_console_client.publish(
        TopicArn=sns_topic_arn,
        Subject='[AWS Alert] EC2 Termination & Expiry Report',
        Message=message
    )

    return {
        'statusCode': 200,
        'body': json.dumps('Message sent to SNS')
    }
