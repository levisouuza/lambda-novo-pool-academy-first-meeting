from pydantic import BaseSettings


class ConfigVariables(BaseSettings):
    glue_job_name: str
    worker_type: str
    number_of_workers: int
