class LoginAlreadyExistsError(Exception):
    pass


class EmailAlreadyExistsError(Exception):
    pass


class EmployeeAlreadyRegisteredError(Exception):
    pass


class EmployeeNotFoundError(Exception):
    pass


class InvalidCredentialsError(Exception):
    pass

class InvalidRefreshTokenError(Exception):
    pass