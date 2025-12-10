from typing import Dict, Any
from botocore.exceptions import ClientError

from lambdabucketoperations.services.aws import AwsService


class SqsService:
    def __init__(self, queue_url: str):
        self.sqs_client = AwsService.get_client("sqs")
        self._queue_url = queue_url

    def send_message(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """
        Envia uma mensagem para uma fila SQS.

        :param queue_url: URL da fila SQS
        :param payload: Dicionário contendo os dados a serem enviados
        :return: Dict com o status da operação, message_id ou erro
        """
        try:
            response = self.sqs_client.send_message(
                QueueUrl=self._queue_url,
                MessageBody=str(payload)  # pode trocar por json.dumps se preferir
            )

            return {
                "status": "success",
                "message_id": response.get("MessageId"),
                "response": response
            }

        except ClientError as e:
            return {
                "status": "error",
                "error_message": str(e),
                "operation": "send_message"
            }
