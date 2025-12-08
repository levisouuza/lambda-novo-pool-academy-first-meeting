from typing import Dict, Any, List
from botocore.exceptions import ClientError

from lambdabucketoperations.services.aws import AwsService


class S3Service:
    def __init__(self):
        self.s3_client = AwsService.get_client("s3")

    def list_objects(
            self, bucket_name: str, prefix: str = ""
    ) -> List[Dict[str, Any]]:
        try:
            paginator = self.s3_client.get_paginator(
                "list_objects_v2"
            )
            page_iterator = paginator.paginate(
                Bucket=bucket_name, Prefix=prefix
            )

            objects = []
            for page in page_iterator:
                contents = page.get("Contents", [])
                objects.extend(contents)

            return objects

        except ClientError as e:
            raise RuntimeError(
                f"Erro ao listar objetos no bucket "
                f"'{bucket_name}': {e}"
            )

    def delete_object(
            self, bucket_name: str, key: str
    ) -> Dict[str, Any]:
        try:
            print(f"Deletando arquivo {key}")

            return self.s3_client.delete_object(
                Bucket=bucket_name, Key=key
            )
        except ClientError as e:
            raise RuntimeError(
                f"Erro ao deletar '{bucket_name}/{key}': {e}"
            )

    def copy_object(
        self,
        source_bucket: str,
        source_key: str,
        dest_bucket: str,
        dest_key: str,
    ) -> Dict[str, Any]:

        try:
            copy_source = {
                "Bucket": source_bucket,
                "Key": source_key
            }
            return self.s3_client.copy_object(
                CopySource=copy_source,
                Bucket=dest_bucket,
                Key=dest_key,
            )
        except ClientError as e:
            raise RuntimeError(
                f"Erro ao copiar '{source_bucket}/{source_key}' "
                f"para '{dest_bucket}/{dest_key}': {e}"
            )
