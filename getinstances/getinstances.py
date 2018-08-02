"""
   AWS Lambda function to return a list of the active EC2 instances running
   in an account.
"""
import json
import datetime
import boto3

CLIENT = boto3.client('ec2')

RESPONSE = CLIENT.describe_instances(
    Filters=[
        {
            'Name': 'instance-state-name',
            'Values': [
                'running'
            ]
        }
    ],
    MaxResults=100
)

def get_id(instances):
    """
    returns a list of EC2 instances that are in the 'running'
    state, return object is a list of dicts
    """
    running_instances = []
    for instance in instances["Reservations"][0]["Instances"]:
        running_instances.append({'Instance ID': instance['InstanceId']})
    if not running_instances:
        print("No running instances detected!")
    else:
        return running_instances

def dt_converter(d):
    """
    converts datetime objects to string objects
    """
    if isinstance(d, datetime.datetime):
        return d.__str__()

def encoder(j):
    """
    dumps json objects to strings so any datetime objects
    can be converted to compatible strings before reloading
    as json again
    """
    return json.loads(json.dumps(j, default=dt_converter))

def my_handler(event, context):
    """
    lambda event handler that returns the list of instances
    """
    return encoder(get_id(RESPONSE))
