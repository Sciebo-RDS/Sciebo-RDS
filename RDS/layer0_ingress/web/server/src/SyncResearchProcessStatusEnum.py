from enum import Enum

class ProcessStatus(Enum):
    START = 0
    FINISHED = 1
    PROJECT_CREATED = 2
    METADATA_SYNCHRONIZED = 3
    FILEDATA_SYNCHRONIZED = 4
