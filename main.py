from core import Core

coreServices = Core()
resources = coreServices.getAllResources()

for resource in resources:
    if resource == 'ec2':
        coreServices.getEC2Instances(['running'])
        pass
    elif resource == 's3':
        buckets = coreServices.listS3Buckets()
        for bucket in buckets:
            print('🪣 Found: ', bucket['Name'])
        pass
    elif resource == 'rds':
        rdsInstances = coreServices.listRDSInstances()
        for instance in rdsInstances:
            print('⚠️ (running)' if instance['DBInstanceStatus'] == 'available' else 'Instance:', instance['DBInstanceIdentifier'], instance['DBInstanceClass'], instance['Engine'])

        

