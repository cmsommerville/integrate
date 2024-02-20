from app.extensions import db
from app.shared import BaseModel

from ..tables import TBL_NAMES

CONFIG_AGE_DISTRIBUTION_SET = TBL_NAMES["CONFIG_AGE_DISTRIBUTION_SET"]
CONFIG_ATTRIBUTE_DETAIL = TBL_NAMES["CONFIG_ATTRIBUTE_DETAIL"]
CONFIG_BENEFIT = TBL_NAMES["CONFIG_BENEFIT"]
CONFIG_RATE_TABLE = TBL_NAMES["CONFIG_RATE_TABLE"]
CONFIG_RATE_TABLE_SET = TBL_NAMES["CONFIG_RATE_TABLE_SET"]
CONFIG_RATING_MAPPER_COLLECTION = TBL_NAMES["CONFIG_RATING_MAPPER_COLLECTION"]
REF_MASTER = TBL_NAMES["REF_MASTER"]


class Model_ConfigRateTableSet(BaseModel):
    __tablename__ = CONFIG_RATE_TABLE_SET

    config_rate_table_set_id = db.Column(db.Integer, primary_key=True)
    config_benefit_id = db.Column(
        db.ForeignKey(
            f"{CONFIG_BENEFIT}.config_benefit_id",
            onupdate="CASCADE",
            ondelete="CASCADE",
        ),
        nullable=False,
    )
    config_rate_table_set_label = db.Column(db.String(100), nullable=False)

    age_distribution_set_id = db.Column(
        db.ForeignKey(f"{CONFIG_AGE_DISTRIBUTION_SET}.config_age_distribution_set_id"),
        comment="Default distribution of ages at issue",
    )
    rating_mapper_collection_id1 = db.Column(
        db.ForeignKey(
            f"{CONFIG_RATING_MAPPER_COLLECTION}.config_rating_mapper_collection_id"
        ),
        comment="Indicates which rating mapper sets can be used with this product. Also specifies distributions.",
        nullable=True,
    )
    rating_mapper_collection_id2 = db.Column(
        db.ForeignKey(
            f"{CONFIG_RATING_MAPPER_COLLECTION}.config_rating_mapper_collection_id"
        ),
        comment="Indicates which rating mapper sets can be used with this product. Also specifies distributions.",
        nullable=True,
    )
    rating_mapper_collection_id3 = db.Column(
        db.ForeignKey(
            f"{CONFIG_RATING_MAPPER_COLLECTION}.config_rating_mapper_collection_id"
        ),
        comment="Indicates which rating mapper sets can be used with this product. Also specifies distributions.",
        nullable=True,
    )
    rating_mapper_collection_id4 = db.Column(
        db.ForeignKey(
            f"{CONFIG_RATING_MAPPER_COLLECTION}.config_rating_mapper_collection_id"
        ),
        comment="Indicates which rating mapper sets can be used with this product. Also specifies distributions.",
        nullable=True,
    )
    rating_mapper_collection_id5 = db.Column(
        db.ForeignKey(
            f"{CONFIG_RATING_MAPPER_COLLECTION}.config_rating_mapper_collection_id"
        ),
        comment="Indicates which rating mapper sets can be used with this product. Also specifies distributions.",
        nullable=True,
    )
    rating_mapper_collection_id6 = db.Column(
        db.ForeignKey(
            f"{CONFIG_RATING_MAPPER_COLLECTION}.config_rating_mapper_collection_id"
        ),
        comment="Indicates which rating mapper sets can be used with this product. Also specifies distributions.",
        nullable=True,
    )

    rates = db.relationship("Model_ConfigRateTable")


class Model_ConfigRateTable(BaseModel):
    __tablename__ = CONFIG_RATE_TABLE

    config_rate_table_id = db.Column(db.Integer, primary_key=True)
    config_rate_table_set_id = db.Column(
        db.ForeignKey(
            f"{CONFIG_RATE_TABLE_SET}.config_rate_table_set_id",
            onupdate="CASCADE",
            ondelete="CASCADE",
        ),
        nullable=True,
    )
    rating_age = db.Column(db.Integer, nullable=False)

    rating_attr_id1 = db.Column(
        db.ForeignKey(
            f"{CONFIG_ATTRIBUTE_DETAIL}.config_attr_detail_id",
            onupdate="NO ACTION",
            ondelete="NO ACTION",
        )
    )
    rating_attr_id2 = db.Column(
        db.ForeignKey(
            f"{CONFIG_ATTRIBUTE_DETAIL}.config_attr_detail_id",
            onupdate="NO ACTION",
            ondelete="NO ACTION",
        )
    )
    rating_attr_id3 = db.Column(
        db.ForeignKey(
            f"{CONFIG_ATTRIBUTE_DETAIL}.config_attr_detail_id",
            onupdate="NO ACTION",
            ondelete="NO ACTION",
        )
    )
    rating_attr_id4 = db.Column(
        db.ForeignKey(
            f"{CONFIG_ATTRIBUTE_DETAIL}.config_attr_detail_id",
            onupdate="NO ACTION",
            ondelete="NO ACTION",
        )
    )
    rating_attr_id5 = db.Column(
        db.ForeignKey(
            f"{CONFIG_ATTRIBUTE_DETAIL}.config_attr_detail_id",
            onupdate="NO ACTION",
            ondelete="NO ACTION",
        )
    )
    rating_attr_id6 = db.Column(
        db.ForeignKey(
            f"{CONFIG_ATTRIBUTE_DETAIL}.config_attr_detail_id",
            onupdate="NO ACTION",
            ondelete="NO ACTION",
        )
    )

    rate_per_unit = db.Column(db.Numeric(12, 5), nullable=False)
    rate_frequency_id = db.Column(db.ForeignKey(f"{REF_MASTER}.ref_id"), nullable=False)
    rate_unit_value = db.Column(db.Numeric(12, 2), nullable=False)

    rating_attr1 = db.relationship(
        "Model_ConfigAttributeDetail",
        primaryjoin="Model_ConfigRateTable.rating_attr_id1 == Model_ConfigAttributeDetail.config_attr_detail_id",
    )
    rating_attr2 = db.relationship(
        "Model_ConfigAttributeDetail",
        primaryjoin="Model_ConfigRateTable.rating_attr_id2 == Model_ConfigAttributeDetail.config_attr_detail_id",
    )
    rating_attr3 = db.relationship(
        "Model_ConfigAttributeDetail",
        primaryjoin="Model_ConfigRateTable.rating_attr_id3 == Model_ConfigAttributeDetail.config_attr_detail_id",
    )
    rating_attr4 = db.relationship(
        "Model_ConfigAttributeDetail",
        primaryjoin="Model_ConfigRateTable.rating_attr_id4 == Model_ConfigAttributeDetail.config_attr_detail_id",
    )
    rating_attr5 = db.relationship(
        "Model_ConfigAttributeDetail",
        primaryjoin="Model_ConfigRateTable.rating_attr_id5 == Model_ConfigAttributeDetail.config_attr_detail_id",
    )
    rating_attr6 = db.relationship(
        "Model_ConfigAttributeDetail",
        primaryjoin="Model_ConfigRateTable.rating_attr_id6 == Model_ConfigAttributeDetail.config_attr_detail_id",
    )
