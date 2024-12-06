from typing import Dict

from pydantic import BaseModel


class EndpointConfig(BaseModel):
    incident: str
    change_record: str

class SnowBrokerConfig(BaseModel):
    hostname: str
    endpoint: EndpointConfig

class ECSS3Config(BaseModel):
    region: str
    endpoint_url: str
    access_key_var: str
    secret_key_var: str

class ArtifactoryConfig(BaseModel):
    spa_pattern: str

class ProfileConfig(BaseModel):
    prod_buckets: str
    artifactory: ArtifactoryConfig
    snow_broker: SnowBrokerConfig
    ecs_s3: ECSS3Config

class AppConfig(BaseModel):
    profiles: Dict[str, ProfileConfig]