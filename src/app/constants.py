MAX_RECURSION = 3
SEC_BEFORE_NEXT_REQUEST = 86400
SUBJECT = "Сервис ИПР"
EXAMPLE_403 = {
    "content": {"application/json": {"example": {"detail": "Permission denied"}}}
}
EXAMPLE_429 = {
    "content": {
        "application/json": {
            "example": {"detail": "You cant send more than 1 request per day"}
        }
    }
}
EXAMPLE_TASK_404 = {
    "content": {"application/json": {"example": {"detail": "Task not found"}}}
}
EXAMPLE_IDP_404 = {
    "content": {"application/json": {"example": {"detail": "IDP not found"}}}
}
EXAMPLE_EMPLOYEE_404 = {
    "content": {"application/json": {"example": {"detail": "Employee not found"}}}
}
EXAMPLE_ACTIVE_IDP_400 = {
    "content": {
        "application/json": {"example": {"detail": "Employee already has active IDP"}}
    }
}
EXAMPLE_ERROR_SENDING_400 = {
    "content": {"application/json": {"example": {"detail": "Mail didnt sent"}}}
}
EXAMPLE_SUCCESS_SENDING_200 = {
    "content": {
        "application/json": {
            "example": {
                "title": "IDP request",
                "letter": "Wanna learn something new.",
                "director_id": 22007,
                "file": "reasons.doc",
            }
        }
    }
}
