import csv
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
        response = ec2_client.describe_regions()

        print(colored('Checking EC2 instances ', 'yellow'))  # Yellow for visibility
        for region in response['Regions']:
            print(colored('🌍 - ', 'cyan') + region['RegionName'])  # Cyan for region names
        
            instances = boto3.resource('ec2', region_name=region['RegionName']).instances.filter(
                Filters=[
                    {
                        'Name': 'instance-state-name',
                        'Values': type
                    }
                ]
            )

            for instance in instances:
                instance_name = self.get_instance_name(instance)
                print(colored(f'Instance Name: {instance_name}, Instance ID: {instance.id}, Status: {type}', 'green'))

    def get_instance_name(self, instance):
        # Extract the 'Name' tag value from the instance
        for tag in instance.tags or []:
            if tag['Key'] == 'Name':
                return tag['Value']
        return "N/A"

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

    def listVPCs(self):
        # ec2_resource = boto3.resource('ec2')
        print(colored('Checking VPCs', 'yellow'))  # Yellow for visibility

        allVpcs = []
        
        for region_info in boto3.client('ec2').describe_regions()['Regions']:
            region_name = region_info['RegionName']
            ec2_client = boto3.client('ec2', region_name=region_name)
            vpcs = ec2_client.describe_vpcs()['Vpcs']

            for vpc in vpcs:
                vpc_info = {
                    "Region": region_name,
                    "VPC ID": vpc['VpcId'],
                    "CIDR Block": vpc['CidrBlock'],
                    "State": vpc['State'],
                    "Is Default": vpc['IsDefault']
                }
                allVpcs.append(vpc_info)

        return allVpcs
    
    def listLambda(self):
        print(colored('Checking Lambda', 'yellow'))  # Yellow for visibility
        
        allLambda = []
       
        for region_info in boto3.client('ec2').describe_regions()['Regions']:
            region_name = region_info['RegionName']
            lambda_client = boto3.client('lambda', region_name=region_name)

            # List all Lambda functions in the current region
            response = lambda_client.list_functions()

            for function in response['Functions']:
                functionName = function['FunctionName']

                allLambda.append({
                    'Region': region_name,
                    'FunctionName': functionName
                })

        return allLambda
    

   