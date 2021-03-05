from bson.decimal128 import Decimal128
from djongo.models import DecimalField


# https://github.com/nesdis/djongo/issues/82
# https://github.com/nesdis/djongo/issues/378

# https://github.com/nesdis/djongo/pull/525/commits/86dbe3918ac4b2299d6aa3249a4509996f53920c
# edit the djongo/operations.py file

class MongoDecimalField(DecimalField):
    def to_python(self, value):
        if isinstance(value, Decimal128):
            value = self.format_number(value.to_decimal())
        return super().to_python(value)

    def get_prep_value(self, value):
        value = super().get_prep_value(value)
        return Decimal128(value)
