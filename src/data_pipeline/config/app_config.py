from dataclasses import dataclass
from pathlib import Path
from typing import Optional

import yaml
from pydantic import BaseModel


class UnityCatalogConfig(BaseModel):
    catalog_name: str
    source_schema: str
    target_schema: str
    log_path: str


class SparkConfig(BaseModel):
    app_name: str
    master: str


class DatabaseConfig(BaseModel):
    type: str
    path: str


class Config(BaseModel):
    environment: str
    unity_catalog: UnityCatalogConfig
    spark: SparkConfig
    database: DatabaseConfig


@dataclass
class AppConfig:
    _config: Config
    
    @classmethod
    def from_yaml(cls, config_path: Path) -> "AppConfig":
        with open(config_path) as f:
            config_dict = yaml.safe_load(f)
        return cls(Config(**config_dict))
    
    @property
    def unity_catalog(self) -> UnityCatalogConfig:
        return self._config.unity_catalog
    
    @property
    def spark(self) -> SparkConfig:
        return self._config.spark
    
    @property
    def database(self) -> DatabaseConfig:
        return self._config.database