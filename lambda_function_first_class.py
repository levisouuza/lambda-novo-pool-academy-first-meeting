import boto3
import json
from datetime import datetime


def _get_current_date() -> str:
    now_sp = datetime.now()
    return now_sp.strftime("%Y%m%d")


def _build_dest_key_to_copy_files(key: str) -> str:
    list_key_elements_names = key.split("/")
    terms_file_name = list_key_elements_names[1].split(".")
    new_file_name = f"{list_key_elements_names[0]}/" \
                    f"{terms_file_name[0]}_" \
                    f"{_get_current_date()}" \
                    f".{terms_file_name[1]}"

    return new_file_name


def lambda_handler(event, context):
    real_event = event.get('Records')[0]
    s3_event = real_event.get("s3")
    event_object_from_s3 = s3_event.get("object")
    bucket_name = s3_event.get("bucket").get("name")
    object_file = event_object_from_s3.get("key")

    s3_client = boto3.client("s3")

    print(f"Renomeando objeto coloca a data atual de PUT no s3. Arquivo Incluido: {object_file}")
    dest_key = _build_dest_key_to_copy_files(object_file)

    copy_source = {
        "Bucket": bucket_name,
        "Key": object_file
    }
    s3_client.copy_object(
        CopySource=copy_source,
        Bucket=bucket_name,
        Key=dest_key,
    )

    print(f"Objeto renomeado de: {object_file} para {dest_key}")

    print(f"Delentando objeto {object_file}")
    s3_client.delete_object(
        Bucket=bucket_name, Key=object_file
    )

    # O boto3, SDK AWS Python, não possui função nativa de renomeação de objetos.
    # É preciso fazer o copy alterando o nome da chave final e deletar o arquivo original

    response = {
        'statusCode': 200,
        'body': {
            "bucket_name": bucket_name,
            "new_file": dest_key
        }
    }

    print(response)

    return response
