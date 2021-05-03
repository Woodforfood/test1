import boto3
import pandas as pd
import time

ec2 = boto3.resource('ec2')
client = boto3.client('ec2')
waiter = client.get_waiter('instance_running')

def list_of_instances():
    row_list = []
    for instance in ec2.instances.all():
        for tag in instance.tags:
          row = {'Name': [tag['Value']], 'InstanceID': [instance.id], 'Status': [instance.state.get('Name')], 'IP': [instance.public_ip_address]}
          df = pd.DataFrame(row)
          row_list.append(row)
          state = instance.state.get('Name')

    df = pd.DataFrame(row_list)
    print(df)

def stop_instance():
    while True:
      if action.lower().startswith('stop'):
        try:
          user_input = input('Select instance: ')
          response = client.describe_instances(InstanceIds=[user_input])
          for r in response['Reservations']:
            for inst in r['Instances']:
              print('stopping...')
              if inst['State']['Name'] == 'running':
                return client.stop_instances(InstanceIds=[user_input])
              else:
                print('Instance has been stopped already. Choose another one.')
        except:
          print('Incorrect Instance ID')
          break

def start_instance():
    while True:
      if action.lower().startswith('start'):
        try:
          user_input = input('Select instance: ')
          response = client.describe_instances(InstanceIds=[user_input])
          for r in response['Reservations']:
            for inst in r['Instances']:
              print('starting...')
              if inst['State']['Name'] == 'stopped':
                client.start_instances(InstanceIds=[user_input])
                waiter.wait(InstanceIds=[user_input])
                publicip = client.describe_instances(InstanceIds=[user_input])['Reservations'][0]['Instances'][0]['PublicIpAddress']
                print(publicip)
                return None
              else:
                print('Instance is in running state. Choose another one.')
        except:
          print('Incorrect Instance ID')
          break

all_functions = {
    'start': start_instance, 'stop': stop_instance
}
list_of_instances()
action = input('START OR STOP: ')

try:
  all_functions[action]()
except KeyError:
  print('Incorrect command')
