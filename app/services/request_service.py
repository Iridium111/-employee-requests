from app.services.request_state import RequestStateMachine
from app.schemas.request import RequestChangeStatus

class RequestService:
    @classmethod
    def change_status(
            cls,
            request,
            new_status: RequestChangeStatus
    ):
        current_status = request.status
        if not RequestStateMachine.can_transition(current_status, new_status.status):
            raise ValueError(f"Transition from {current_status} "
                             f"to {new_status.status} is not allowed.")

        request.status = new_status.status
        return request
