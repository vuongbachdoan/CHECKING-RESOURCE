import boto3
from termcolor import colored

session = boto3.Session()

class Core:
    def getAllResources(self):
        # Get the list of available services
        services = session.get_available_services()
        return services

    def getEC2Instances(self, type=['pending', 'running', 'shutting-down', 'terminated', 'stopping', 'stopped']):
        ec2_client = boto3.client('ec2')

        # Retrieves all regions/endpoints that work with EC2
        regions = ec2_client.describe_regions()['Regions']

        print(colored('Checking EC2 instances ', 'yellow'))  # Yellow for visibility
        for region in regions:
            print(colored(' - ', 'cyan') + region['RegionName'])  # Cyan for region names
            ec2_resource = boto3.resource('ec2', region_name=region['RegionName'])
            for instance in ec2_resource.instances.all().filter(
                Filters=[
                    {
                        'Name': 'instance-state-name',
                        'Values': type
                    }
                ]
            ):
                try:
                    instance_name = next((tag['Value'] for tag in instance.tags if tag['Key'] == 'Name'), None)
                    print(colored('⚠️ Warning: ', 'red'), instance.id, instance.instance_type, instance.state['Name'], instance_name)
                except Exception as e:
                    print(f"Error processing instance {instance.id}: {e}")

    def listS3Buckets(self):
        print(colored('Checking S3 buckets ', 'yellow'))  # Yellow for visibility
        s3 = boto3.client('s3')
        buckets = s3.list_buckets()
        return buckets['Buckets']

    def listS3Objects(self, bucketName):
        print(bucketName)

    def listRDSInstances(self):
        print(colored('Checking RDS ', 'yellow'))  # Yellow for visibility
        rds = boto3.client('rds')
        return rds.describe_db_instances()['DBInstances']
