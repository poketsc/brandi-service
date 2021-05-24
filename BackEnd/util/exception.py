class CustomError(Exception):
    def __init__(self, message, status_code):
        self.message = message
        self.status_code = status_code
class ValidationError(CustomError):
    pass
class ProductOptionExistError(CustomError):
    pass
class ProductOptionSoldOutError(CustomError):
    pass
class CartIdError(CustomError):
    pass
class ChangeTimeError(CustomError):
    pass
class ChangeHistoryInformationError(CustomError):
    pass