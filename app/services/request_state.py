
class RequestStateMachine:
    ALLOWED_TRANSITIONS = {
        "CREATED": {"IN_PROGRESS", "CANCELLED"},
        "IN_PROGRESS": {"DONE", "CANCELLED"},
        "DONE": set(),
        "CANCELLED": set(),
    }

    @classmethod
    def can_transition(
            cls,
            current_status: str,
            new_status: str,
    ) -> bool:
        if (
                current_status not in cls.ALLOWED_TRANSITIONS or
                new_status not in cls.ALLOWED_TRANSITIONS
        ):
            raise ValueError("Unknown status.")

        return new_status in cls.ALLOWED_TRANSITIONS[current_status]



