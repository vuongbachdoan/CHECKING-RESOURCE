from termcolor import colored
from core import Core
import datetime

# Create an instance of the Core service
core_service = Core() 

# Get all resources from the Core service
resources = core_service.get_all_resources()

# Iterate over each resource
for resource in resources:
    # If the resource is an EC2 instance
    if resource == 'ec2':
        print(colored('Checking EC2 instances ', 'yellow')) 
        # Get all EC2 instances
        core_service.get_all_ec2_instances() 
        
    # If the resource is an S3 bucket
    elif resource == 's3':
        # Get all S3 buckets
        buckets = core_service.get_s3_buckets()
        # Prepare the header for the bucket information
        bucket_information = "Bucket Name,Creation Date,Owner ID,Objects,Object Key,Object Size,Object Last Modified\n"
        # Iterate over each bucket
        for bucket in buckets:
            # Get the details of the bucket and append it to the bucket information
            bucket_information += core_service.get_s3_buckets_with_details(bucket)
        # Get the current timestamp
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        # Write the bucket information to an S3 bucket
        core_service.put_object_to_S3(bucket_information, "vuongbach-checking-services", f"s3/{timestamp}/s3_bucket_info.csv")

    # If the resource is an RDS instance
    elif resource == 'rds':
        # Get all RDS instances
        rds_instances = core_service.get_rds_instances()
        # Prepare the header for the RDS information
        rds_informations = "Instance ID,Instance Type,DB Engine\n"
        # Iterate over each RDS instance
        for instance in rds_instances:
            # Get the details of the RDS instance and append it to the RDS information
            rds_informations += core_service.get_rds_instance_detail(instance)
        # Get the current timestamp
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        # Write the RDS information to an S3 bucket
        core_service.put_object_to_S3(
            rds_informations,
            "vuongbach-checking-services",
            f"rds/{timestamp}/instance_info.csv"
        )

    # If the resource is a VPC
    elif resource == 'vpc-lattice':
        # Get all VPCs
        vpcs = core_service.get_vpcs()
        # Prepare the header for the VPC information
        vpc_informations = "Region,VPC ID,CIDR Block,State,Is Default\n"
        # Iterate over each VPC
        for vpc in vpcs:
            # Get the details of the VPC and append it to the VPC information
            vpc_informations += f"{vpc['Region']}, {vpc['VPC ID']}, {vpc['CIDR Block']}, {vpc['State']}, {vpc['Is Default']}\n"
            print(f"Region: {vpc['Region']}, VPC ID: {vpc['VPC ID']}, CIDR Block: {vpc['CIDR Block']}, State: {vpc['State']}, Is Default: {vpc['Is Default']}")
        # Get the current timestamp
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        # Write the VPC information to an S3 bucket
        core_service.put_object_to_S3(
            vpc_informations,
            "vuongbach-checking-services",
            f"vpc/{timestamp}/vpc_info.csv"
        )

    # If the resource is a Lambda function
    elif resource == 'lambda':
        # List all Lambda functions
        lambdas = core_service.list_lambda()
        # Prepare the header for the Lambda information
        lambda_informations = "Function Name,Runtime,Handler,Memory Size,Timeout,Role\n"
        # Get the current timestamp
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        # Write the Lambda information to an S3 bucket
        core_service.put_object_to_S3(
            lambdas,
            "vuongbach-checking-services",
            f"lambda/{timestamp}/vpc_info.csv"
        )