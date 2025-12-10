from pydantic import BaseSettings


class ConfigVariables(BaseSettings):
    glue_job_name: str | None
    worker_type: str | None
    number_of_workers: int | None
    queue_url_sqs: str
