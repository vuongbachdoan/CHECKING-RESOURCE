from termcolor import colored
from core import Core

coreServices = Core()  # Highlighted in blue for clarity
resources = coreServices.getAllResources()

for resource in resources:
    if resource == 'ec2':
        coreServices.getEC2Instances(['running'])  # Applied yellow for visibility
        pass
    elif resource == 's3':
        buckets = coreServices.listS3Buckets()
        for bucket in buckets:
            print(colored('🪣 Found: ', 'green') + bucket['Name'])  # Green for positive findings
        pass
    elif resource == 'rds':
        rdsInstances = coreServices.listRDSInstances()
        for instance in rdsInstances:
            status_indicator = colored('⚠️ (running)', 'red') if instance['DBInstanceStatus'] == 'available' else 'Instance:'
            print(status_indicator, instance['DBInstanceIdentifier'], instance['DBInstanceClass'], instance['Engine'])
