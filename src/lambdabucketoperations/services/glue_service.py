import json
from typing import Dict, Any
from botocore.exceptions import ClientError
from lambdabucketoperations.model.config_variables import ConfigVariables
from lambdabucketoperations.services.aws import AwsService


class GlueService:
    def __init__(self, config: ConfigVariables):
        self.config = config
        self.glue_client = AwsService.get_client("glue")

    def run_job(self, arguments: dict) -> Dict[str, Any]:

        params = self._build_params_to_execute_glue_job(
            arguments
        )

        try:
            self.glue_client.start_job_run(**params)
            return params

        except ClientError as e:
            raise RuntimeError(
                f"Erro ao executar Glue Job '{params.get('JobName')}': {e}"
            )

    def _build_params_to_execute_glue_job(
            self, arguments: dict
    ) -> Dict[str, Any]:
        return {
            "JobName": self.config.glue_job_name,
            "Arguments": arguments,
            "WorkerType": self.config.worker_type,
            "NumberOfWorkers": self.config.number_of_workers
        }
