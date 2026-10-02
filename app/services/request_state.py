from enum import Enum

class RequestState(str, Enum):
    CREATED = 'CREATED'
    IN_PROGRESS = 'IN_PROGRESS'
    DONE = "DONE"
    CANCELLED = "CANCELLED"

class RequestStateMachine:
    ALLOWED_TRANSITIONS = {
        RequestState.CREATED: {
            RequestState.IN_PROGRESS,
             RequestState.CANCELLED
        },
        RequestState.IN_PROGRESS:{
            RequestState.DONE,
             RequestState.CANCELLED
        },
        RequestState.DONE: set(),
        RequestState.CANCELLED: set(),
    }

    @classmethod
    def can_transition(
            cls,
            current_status: RequestState,
            new_status: RequestState,
    ) -> bool:
        if (
                current_status not in cls.ALLOWED_TRANSITIONS or
                new_status not in cls.ALLOWED_TRANSITIONS
        ):
            raise ValueError("Unknown status.")

        return new_status in cls.ALLOWED_TRANSITIONS[current_status]
