## Delete Snapshots not attached to AMI
import boto3
from pprint import pprint
## AWS Console Session and EC2 client
aws_console = boto3.Session(profile_name='boto3-user')
ec2_client = aws_console.client(service_name='ec2', region_name='us-east-1')

## Created Empty Set to store all the SNAPSHOTS attached to AMI's
ami_snapshots = set()

## listing all SNAPSHOTS ID's attahed to AMI which are can not be deleted
ami_response = ec2_client.describe_images(Owners=['self'])['Images']
for value in ami_response:
    AMI_ID = value['ImageId']
    for ebs in value['BlockDeviceMappings']:
        ## Here we ate iterating the distoinary KEY VALUE pair
        for key, value in ebs.items():
            if key == 'Ebs':
                snapshot_Id = value['SnapshotId']
                ami_snapshots.add(snapshot_Id)

## Created Empty Set to store all the Available SNAPSHOTS in us-east-1 region
available_snapshots = set()

## listing all Available SNAPSHOTS ID's in us-east-1 region
snapshots_list = ec2_client.describe_snapshots(OwnerIds=['self'])['Snapshots']
for value in snapshots_list:
     available_snapshorts_id = value['SnapshotId']
     volume_id = value['VolumeId']
     available_snapshots.add(available_snapshorts_id)

## Finding differnce in 2 sets (available_snapshots and ami_snapshots) to get Unattached to AMI snapshots
unattached_snapshots = available_snapshots.difference(ami_snapshots)
print('Unattached Snapshots to AMI: ', type(unattached_snapshots))

## Iteratting the unattached_snapshots ID's to find the Volume ID and check whether this volume is attachec to ec2 or not
for unattached_snapshots_id in unattached_snapshots:
    snap_Id = unattached_snapshots_id
    unattached_snap__response = ec2_client.describe_snapshots(
        SnapshotIds=[
            snap_Id
        ]
        )['Snapshots']
    for values in unattached_snap__response:
        volume_id = values['VolumeId']
        if not volume_id:
            ## Deleting Snapshot
            ec2_client.delete_snapshot(SnapshotID = snap_Id)
            print(f"Deleted EBS snapshot {snap_Id} as it was not attached to any volume.")
        else:
           ## Checking if Volume is attached ec2 or not 
           try:
                volume_response = ec2_client.describe_volumes(
                     VolumeIds= [
                          volume_id
                        ]
                    )
                if not volume_response['Volumes'][0]['Attachments']:
                      ec2_client.delete_snapshot(SnapshotID = snap_Id)
                      print(f"Deleted EBS snapshot {snap_Id} as it was taken from a volume not attached to any running instance.")
           except ec2_client.exceptions.ClientError as e:
                if e.response['Error']['Code'] == 'InvalidVolume.NotFound':
                    ec2_client.delete_snapshot(SnapshotId=snap_Id)
                    print(f"Deleted EBS snapshot {snap_Id} as its associated volume was not found.")



