import boto3
from termcolor import colored
import datetime

session = boto3.Session()

class Core: 
    """
    Class to interact with various AWS services, providing functions for:
        - Listing and retrieving information about EC2 instances
        - Listing S3 buckets and their details
        - Listing RDS instances
        - Listing VPCs
        - Listing Lambda functions
    """
    ec2_client = boto3.client('ec2')
    s3 = boto3.client('s3')
    lambda_ = boto3.client('lambda')
    show_ui=True

    # Desc: set to print result to console or not
    def set_show_ui(self, val):
        self.show_ui = val

    # Desc: get all aws services available
    def get_all_resources(self):
        services = session.get_available_services()
        return services
    
    # Desc: get ec2 instances in a region
    def get_ec2_in_single_region(self, region_name='us-east-1', instance_state=['pending', 'running', 'shutting-down', 'terminated', 'stopping', 'stopped']):
        ec2_instances = boto3.resource('ec2', region_name)
        return ec2_instances.instances.all()  
    
    # Desc: get regions work with ec2
    def get_ec2_regions(self):
        regions = self.ec2_client.describe_regions()['Regions']
        return regions
    
    # Desc: get ec2 instance details
    def get_ec2_instance_details(self, instance_id, region):
        ec2 = boto3.resource('ec2', region)
        instance_details = ec2.Instance(instance_id)
        return instance_details

    # Desc: CHECK EC2
    def get_all_ec2_instances(self, type=['pending', 'running', 'shutting-down', 'terminated', 'stopping', 'stopped'], region='all'):
        regions = [region]
        if region == 'all':
            regions = self.get_ec2_regions()
        csv_content = "Region, Name, Id, Type, State, Launch Time"
        for region in regions:
            if self.show_ui:
                print(colored('🌍 - ', 'cyan') + region['RegionName'])
            ec2_instances = self.get_ec2_in_single_region(region['RegionName'])
            for instance in ec2_instances:
                try:
                    instance = self.get_ec2_instance_details(instance.id, region['RegionName'])
                    instance_name = None
                    if instance.tags is not None:
                        for tag in instance.tags:
                            if tag['Key'] == 'Name':
                                instance_name = tag['Value']
                    instance_id = instance.id
                    instance_type = instance.instance_type
                    instance_state = instance.state['Name']
                    instance_launch_time = instance.launch_time
                    csv_content += f"{region}, {instance_name},{instance_id},{instance_type},{instance_state},{instance_launch_time}\n"
                    print(colored('⚠️(warning):', 'red'), instance_name, instance_id, instance_type, instance_state, instance_launch_time)
                except Exception as e:
                    print(f"Error processing instance {instance.id}: {e}")
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        self.s3.put_object(
            Body=csv_content,
            Bucket='vuongbach-checking-services',
            Key=f"ec2/{timestamp}/instance_info.csv"
        )

    # Desc: get s3 bucket details
    def get_s3_buckets_with_details(self, bucket):
        csv_content = ""
        csv_content += ""
        bucket_name = bucket['Name']
        creation_date = bucket['CreationDate'].strftime("%Y-%m-%d %H:%M:%S")
        try:
            owner_id = bucket['Owner']['ID']
        except KeyError:
            print(f"Owner information not directly available for bucket: {bucket_name}")
            owner_id = None
        try:
            objects = self.s3.list_objects(Bucket=bucket_name)['Contents']
            object_count = len(objects)
        except KeyError:
            objects = []
            object_count = 0
        csv_row = f"{bucket_name},{creation_date},{owner_id},{object_count}"
        csv_content += csv_row + "\n"
        return csv_content
    
    # Desc: put object to S3 bucket
    def put_object_to_S3(self, content, bucket_name, key):
        self.s3.put_object(
            Body=content,
            Bucket=bucket_name, 
            Key=key 
        )

    # Desc: list all bucket
    def get_s3_buckets(self):
        print(colored('Checking S3 buckets ', 'yellow')) 
        s3 = boto3.client('s3')
        buckets = s3.list_buckets()
        return buckets['Buckets']

    # Desc: get rds instances
    def get_rds_instances(self):
        print(colored('Checking RDS ', 'yellow')) 
        rds = boto3.client('rds')
        return rds.describe_db_instances()['DBInstances']
    
    # Desc: get rds instance details
    def get_rds_instance_detail(self, instance):
        status_indicator = colored('⚠️ (running)', 'red') if instance['DBInstanceStatus'] == 'available' else 'Instance:'
        print(status_indicator, instance['DBInstanceIdentifier'], instance['DBInstanceClass'], instance['Engine'])
        return f"{instance['DBInstanceIdentifier']}, {instance['DBInstanceClass']}, {instance['Engine']}\n"

    # Desc: get all VPC
    def get_vpcs(self):
        print(colored('Checking VPCs', 'yellow')) 
        all_vpcs = []
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
                all_vpcs.append(vpc_info)
        return all_vpcs
    
    # Desc: list all lambda function
    def list_lambda(self):
        print(colored('Checking Lambda', 'yellow')) 
        allLambda = ""
        response = self.lambda_.list_functions()
        for function in response['Functions']:
            function_name = function['FunctionName']
            function_runtime = function['Runtime']
            function_handler = function['Handler']
            function_memory = function['MemorySize']
            function_timeout = function['Timeout']
            function_role = function['Role']
            allLambda += f"{function_name}, {function_runtime}, {function_handler}, {function_memory}, {function_timeout}, {function_role}\n"
            print(f"{function_name}, {function_runtime}, {function_handler}, {function_memory}, {function_timeout}, {function_role}")
        return allLambda
    

   