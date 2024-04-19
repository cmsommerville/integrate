from app.extensions import ma
from app.shared import BaseSchema
import pandera as pa
from marshmallow import Schema, fields, EXCLUDE
from ..models import Model_ConfigRateTable, Model_ConfigRateTableSet


class Schema_ConfigRateTable(BaseSchema):
    class Meta:
        model = Model_ConfigRateTable
        load_instance = True
        include_relationships = True
        include_fk = True


class Schema_ConfigRateTableSet(BaseSchema):
    class Meta:
        model = Model_ConfigRateTableSet
        load_instance = True
        include_relationships = True
        include_fk = True

    rates = ma.Nested(Schema_ConfigRateTable, many=True)


class Schema_RateTableCohorts(Schema):
    rating_age = fields.Int(data_key="rate_table_age_value", allow_none=True)
    rating_attr_id1 = fields.Int(
        data_key="rate_table_attribute_detail_id1", allow_none=True
    )
    rating_attr_id2 = fields.Int(
        data_key="rate_table_attribute_detail_id2", allow_none=True
    )
    rating_attr_id3 = fields.Int(
        data_key="rate_table_attribute_detail_id3", allow_none=True
    )
    rating_attr_id4 = fields.Int(
        data_key="rate_table_attribute_detail_id4", allow_none=True
    )
    rating_attr_id5 = fields.Int(
        data_key="rate_table_attribute_detail_id5", allow_none=True
    )
    rating_attr_id6 = fields.Int(
        data_key="rate_table_attribute_detail_id6", allow_none=True
    )

    class Meta:
        unknown = EXCLUDE


DFSchema_RateTableCohorts = pa.DataFrameSchema(
    {
        "config_age_distribution_set_id": pa.Column(int),
        "config_age_distribution_id": pa.Column(int),
        "config_rating_mapper_set_id1": pa.Column(
            dtype="Int64", nullable=True, coerce=True
        ),
        "config_rating_mapper_set_id2": pa.Column(
            dtype="Int64", nullable=True, coerce=True
        ),
        "config_rating_mapper_set_id3": pa.Column(
            dtype="Int64", nullable=True, coerce=True
        ),
        "config_rating_mapper_set_id4": pa.Column(
            dtype="Int64", nullable=True, coerce=True
        ),
        "config_rating_mapper_set_id5": pa.Column(
            dtype="Int64", nullable=True, coerce=True
        ),
        "config_rating_mapper_set_id6": pa.Column(
            dtype="Int64", nullable=True, coerce=True
        ),
        "rate_table_attribute_detail_id1": pa.Column(
            dtype="Int64", nullable=True, coerce=True
        ),
        "rate_table_attribute_detail_id2": pa.Column(
            dtype="Int64", nullable=True, coerce=True
        ),
        "rate_table_attribute_detail_id3": pa.Column(
            dtype="Int64", nullable=True, coerce=True
        ),
        "rate_table_attribute_detail_id4": pa.Column(
            dtype="Int64", nullable=True, coerce=True
        ),
        "rate_table_attribute_detail_id5": pa.Column(
            dtype="Int64", nullable=True, coerce=True
        ),
        "rate_table_attribute_detail_id6": pa.Column(
            dtype="Int64", nullable=True, coerce=True
        ),
        "rate_table_age_value": pa.Column(dtype="Int64", nullable=True, coerce=True),
    },
    index=pa.Index(int),
    strict=True,
    coerce=True,
    add_missing_columns=True,
)
