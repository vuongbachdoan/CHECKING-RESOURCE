import boto3

# Create a session using your AWS credentials
session = boto3.Session()

class Core:
    def getAllResources(self):
        # Get the list of available services
        services = session.get_available_services()
        return services

    def getEC2Instances(self, type=['pending' , 'running' , 'shutting-down' , 'terminated' , 'stopping' , 'stopped']):
        ec2 = boto3.client('ec2')

        # Retrieves all regions/endpoints that work with EC2
        response = ec2.describe_regions()

        print('Checking EC2 instances 🔎')
        for region in response['Regions']:
            print('🌐 -', region['RegionName'])
            for instance in boto3.resource('ec2', region_name=region['RegionName']).instances.all().filter(
                Filters=[
                    {
                        'Name': 'instance-state-name',
                        'Values': type
                    }
                ]
            ):
                print('⚠️ Warning: ',instance.id)
    
    def listS3Buckets(self):
        print('Checking S3 bucket 🔎')
        s3 = boto3.client('s3')
        buckets = s3.list_buckets()
        return buckets['Buckets']
    
    def listS3Objects(self, bucketName):
        print(bucketName)

    def listRDSInstances(self):
        rds = boto3.client('rds')
        return rds.describe_db_instances()['DBInstances']