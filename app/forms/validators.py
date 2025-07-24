from wtforms import ValidationError

class HasNoSpecialChar:
    def __init__(self, symbol, message=None):
        self.symbol = symbol
        self.message = message or f'this field cannot contain symbol {symbol}'

    def __call__(self, form, field):
        if self.symbol in field.data:
            raise ValidationError(self.message)