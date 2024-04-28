from enum import StrEnum, auto

# DWH Airflow Module
from exness_airflow.types import ImageEnum

class ImageName(ImageEnum):
    COMMON_TAG = "ubuntu:mantic"
