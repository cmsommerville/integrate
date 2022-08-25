import decimal 
from app.extensions import ma
from marshmallow import post_dump

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
