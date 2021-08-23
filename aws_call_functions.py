import boto3
import requests
import json


def get_config():
    """
    Read JSON containing configurations
    Returns
    -------
    dict which contains details of configuration
    """
    with open('sensitive_estate_config.json') as f:
        config_file = json.load(f)
    return config_file




def get_aws_s3_list():
    """
    Return list of bucket names which contain name "dev-gdlk" as string
    Returns
    -------
    List : Returns names of bucket available in s3
    """
    l = []
    s3 = boto3.resource('s3')
    for bucket in s3.buckets.all():
        if "dev-gdlk" in bucket:
            l .append(bucket)
    return l



def get_holidays():
    """
    Return response for API 
    Returns
    -------
    Dict 
    """

    r = requests.get('http://localhost/api/holidays')
    if r.status_code == 200:
        return r.json()
    return None





def check_vpc_service_exists(config_file, service):
    """
    checks whether VPC endpoint has been created in the AWS Account
    
    Parametes
    -------
    config_file : dict
    A dict containing all the configurations

    service : str
    name of the aws service

    Returns
    -------
    tuple :(str,str) 
    tuple[0] Returns str which take value service_exists or service_does_not_exist
    tuple[1] Returns str which give security group or default ""
    """
    securitygroup = None
    client = boto3.client(
        'ec2', region_name=config_file["Deployment"]["Region"])
    response = client.describe_vpc_endpoints(
        Filters=[
            {
                'Name': 'vpc-id',
                'Values': [
                    config_file["Deployment"]["VPC"],
                ]
            },
        ],
        MaxResults=123
    )
    for services in response['VpcEndpoints']:
        service_name = services['ServiceName'].split(".")[3]
        if service in service_name:
            try:
                securitygroup = services['Groups'][0]["GroupId"]
            except:
                securitygroup = ''
    if securitygroup != None:
        return "service_exists", securitygroup
    else:
        return "service_does_not_exist", ""

