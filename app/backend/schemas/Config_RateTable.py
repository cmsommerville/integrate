from app.shared import BaseSchema
import pandera as pa
from ..models import Model_ConfigRateTable


class Schema_ConfigRateTable(BaseSchema):
    class Meta:
        model = Model_ConfigRateTable
        load_instance = True
        include_relationships = True
        include_fk = True


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
