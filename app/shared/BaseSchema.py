import decimal 
from app.extensions import ma
from marshmallow import post_dump, ValidationError

class BaseSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        load_instance = True
    
    @post_dump(pass_many=True)
    def formatDecimal(self, data, many, **kwargs):
        if many:
            return [{k: v if type(v) != decimal.Decimal else float(v) for k, v in item.items()}
                    for item in data]
        else:
            new_data = {k: v if type(v) != decimal.Decimal else float(v)
                        for k, v in data.items()}
            return new_data


class PrimitiveField(ma.Field):
    def _deserialize(self, value, attr, data, **kwargs):
        if isinstance(value, (str, int, float, bool,)):
            return value
        else:
            raise ValidationError('Field should be str, int, float, or bool')
