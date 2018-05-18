import boto3
import json
import datetime

client = boto3.client('ec2')

response = client.describe_instances(
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
    return json.loads(json.dumps(j, default = dt_converter))

def my_handler(event, context):
    """
    lambda event handler that returns the list of instances
    """
    return encoder(get_id(response))
