from lambdabucketoperations.processor.file_manager_processor import (
    FileManagerProcessor
)
from lambdabucketoperations.model.config_variables import ConfigVariables


def lambda_handler(event, context):

    real_event = event.get('Records')[0]
    print(f"Evento Recebido: {real_event}")

    config_variables = ConfigVariables()

    file_manager_processor = FileManagerProcessor(
        real_event, config_variables
    )

    response = file_manager_processor.process()
    print(response)

    return {
        'statusCode': 200,
        'body': response
    }
