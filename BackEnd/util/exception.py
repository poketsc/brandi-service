class CustomError(Exception):
    def __init__(self, message, status_code):
        self.message = message
        self.status_code = status_code

class ValidationError(CustomError):
    pass

class ProductIdExistError(CustomError):
    pass

class ProductOptionSoldOutError(CustomError):
    pass

class CartIdError(CustomError):
    pass

class ChangeTimeError(CustomError):
    pass

class ChangeHistoryInformationError(CustomError):
    pass

class InsertOrderProductInformationError(CustomError):
    pass

class InsertOrderProductHistoryInformationError(CustomError):
    pass

class InsertShipmentInformationError(CustomError):
    pass

class InsertOrderInformationError(CustomError):
    pass

class InsertOrderHistoryInformationError(CustomError):
    pass

class CartIdTypeError(CustomError):
    pass

class ProductIdTypeError(CustomError):
    pass

class ProductOptionIdTypeError(CustomError):
    pass

class PriceTypeError(CustomError):
    pass

class DiscountedPriceTypeError(CustomError):
    pass

class QuantityTypeError(CustomError):
    pass

class UpdateAddressHistoryEndTimeError(CustomError):
    pass

class InsertAddressHistoryInformationError(CustomError):
    pass

class InsertAddressInformationError(CustomError):
    pass

class GetAddressIdError(CustomError):
    pass

class MaximumShipmentInformationError(CustomError):
    pass

class InvalidRequest(CustomError):
    pass

class DeleteAddressInformationError(CustomError):
    pass

class InvalidAccessError(CustomError):
    pass

class LoginRequiredError(CustomError):
    pass

class CartQuantityError(CustomError):
    pass

class ProductOptionStockError(CustomError):
    pass

class OrderIdTypeError(CustomError):
    pass