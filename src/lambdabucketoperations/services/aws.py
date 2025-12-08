import boto3


class AwsService:
    @classmethod
    def get_client(cls, service: str):
        return boto3.client(service)
