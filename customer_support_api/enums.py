import enum


class CompletedRejected(str, enum.Enum):
    COMPLETED = "COMPLETED"
    REJECTED = "REJECTED"


class RequestStatus(str, enum.Enum):
    PENDING = "PENDING"
    IN_PROGRESS = "IN_PROGRESS"
    COMPLETED = "COMPLETED"
    REJECTED = "REJECTED"
    ARCHIVED = "ARCHIVED"
