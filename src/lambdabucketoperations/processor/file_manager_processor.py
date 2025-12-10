import pytz
from datetime import datetime

from lambdabucketoperations.model.config_variables import ConfigVariables
from lambdabucketoperations.services.s3_service import S3Service
from lambdabucketoperations.services.sqs_service import SqsService


class FileManagerProcessor:
    def __init__(self, event: dict, config_variables: ConfigVariables):
        self._event = event
        self._s3_event = self._event.get("s3")
        self._config_variables = config_variables
        self._s3_service = S3Service()
        self._sqs_service = SqsService(
            self._config_variables.queue_url_sqs
        )

    def process(self) -> dict:
        event_object_from_s3 = self._s3_event.get("object")
        bucket_name = self._s3_event.get("bucket").get("name")
        dest_key = self._build_dest_key_to_copy_files(
            event_object_from_s3
        )

        print("Iniciando processo")
        self._s3_service.copy_object(
            source_bucket=bucket_name,
            source_key=event_object_from_s3.get("key"),
            dest_bucket=bucket_name,
            dest_key=dest_key
        )

        print(f"Objeto original renomeado para {dest_key}")

        self._s3_service.delete_object(
            bucket_name=bucket_name,
            key=event_object_from_s3.get("key")
        )

        print(f"Objeto original deletado "
              f"{event_object_from_s3.get('key')}"
              )

        payload_to_queue = {
            "file_path": self._build_file_path_full(
                bucket_name, dest_key
            ),
            "scope": "novo-pool",
            "chapter": "dados"
        }

        response = self._sqs_service.send_message(payload_to_queue)

        return {"status_code": 200, "response": response}

    def _build_dest_key_to_copy_files(
            self, event_object_s3: dict
    ) -> str:
        list_key_elements_names = event_object_s3.get("key").split("/")
        terms_file_name = list_key_elements_names[1].split(".")
        new_file_name = f"{list_key_elements_names[0]}/" \
                        f"{terms_file_name[0]}_" \
                        f"{self._get_current_date_sp()}" \
                        f".{terms_file_name[1]}"

        return new_file_name

    @staticmethod
    def _get_current_date_sp() -> str:
        tz_sp = pytz.timezone("America/Sao_Paulo")
        now_sp = datetime.now(tz_sp)
        return now_sp.strftime("%Y%m%d")

    @staticmethod
    def _build_file_path_full(bucket_name: str, filename: str) -> str:
        return f"s3://{bucket_name}/{filename}"
