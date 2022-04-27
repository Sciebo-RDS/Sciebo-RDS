from enum import Enum

class ProcessStatus(int, Enum):
    START: int = 0
    FINISHED: int = 1
    PROJECT_CREATED: int = 2
    METADATA_SYNCHRONIZED: int = 3
    FILEDATA_SYNCHRONIZED: int = 4
