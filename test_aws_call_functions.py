
from os import path
import unittest

from unittest.mock import Mock,MagicMock
from unittest.mock import patch

from aws_call_functions import get_aws_s3_list,get_config,check_vpc_service_exists

# boto3 = Mock()


class TestAwsS3(unittest.TestCase):
    @patch('aws_call_functions.boto3.resource')
    def test_aws_s3(self,mock_bucket):
        # test case
        bucket_value = ["ccs-dpgrp-dev-gdlk-backupzone","ccs-dpgrp-dev-gdlk-enrichedzone"]
        mock_bucket.return_value.buckets.all.return_value = bucket_value
        assert get_aws_s3_list()[1] == "ccs-dpgrp-dev-gdlk-enrichedzone"


class TestVPCServic(unittest.TestCase):
    @patch('builtins.open')
    @patch('aws_call_functions.json')
    def setUp(self,mock_json,mock_open):
        mock_json.load.return_value = {"Deployment" : {"Region" :"test-location","VPC" : "tests" }}
        self.config = get_config()

    @patch('aws_call_functions.boto3.client')
    def test_check_vpc_service_exists(self,mock_client):
        val ={"VpcEndpoints": [{'VpcEndpointId': 'vpce-0b1108f7a0cf8ea0f',
               'VpcEndpointType': 'Interface',
               'VpcId': 'vpc-09fecf7c02fc1d726',
               'ServiceName': 'com.amazonaws.eu-west-1.secretsmanager',
               'State': 'available',
                'Groups': [{'GroupId': 'sg-0d7437994f10e162e',
                'GroupName': 'Vpc Security Group secretsmanager'}],
                'CreationTimestamp': "datetime.datetime(2021, 5, 5, 9, 13, 41, 101000, tzinfo=tzutc())",
                'Tags': [],
                'OwnerId': '859272658101'}]}
        mock_client.return_value.describe_vpc_endpoints.return_value = val
        response = check_vpc_service_exists(self.config,"secretsmanager")
        assert response[0] == "service_exists"
        response = check_vpc_service_exists(self.config,"test")
        assert response[0] == "service_does_not_exist"




if __name__ == '__main__':
    unittest.main()