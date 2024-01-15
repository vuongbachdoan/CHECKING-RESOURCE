import boto3
from termcolor import colored

session = boto3.Session()

class Core:
    def getAllResources(self):
        # Get the list of available services
        services = session.get_available_services()
        return services

    def getEC2Instances(self, type=['pending', 'running', 'shutting-down', 'terminated', 'stopping', 'stopped']):
        ec2 = boto3.client('ec2')

        # Retrieves all regions/endpoints that work with EC2
        response = ec2.describe_regions()

        print(colored('Checking EC2 instances ', 'yellow'))  # Yellow for visibility
        for region in response['Regions']:
            print(colored('🌍 - ', 'cyan') + region['RegionName'])  # Cyan for region names
            for instance in boto3.resource('ec2', region_name=region['RegionName']).instances.all().filter(
                Filters=[
                    {
                        'Name': 'instance-state-name',
                        'Values': type
                    }
                ]
            ):
                print(colored('⚠️ Warning: ', 'red') + instance.id)  # Red for warnings

    def listS3Buckets(self):
        print(colored('Checking S3 buckets ', 'yellow'))  # Yellow for visibility
        s3 = boto3.client('s3')
        buckets = s3.list_buckets()
        return buckets['Buckets']

    def listS3Objects(self, bucketName):
        print(bucketName)

    def listRDSInstances(self):
        rds = boto3.client('rds')
        return rds.describe_db_instances()['DBInstances']
