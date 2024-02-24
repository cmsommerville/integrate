import datetime
from app.extensions import db
from app.shared import BaseModel

from ..tables import TBL_NAMES

CONFIG_AGE_DISTRIBUTION_SET = TBL_NAMES["CONFIG_AGE_DISTRIBUTION_SET"]
CONFIG_ATTRIBUTE_SET = TBL_NAMES["CONFIG_ATTRIBUTE_SET"]
CONFIG_PRODUCT = TBL_NAMES["CONFIG_PRODUCT"]
CONFIG_RATING_MAPPER_COLLECTION = TBL_NAMES["CONFIG_RATING_MAPPER_COLLECTION"]
REF_MASTER = TBL_NAMES["REF_MASTER"]


class Model_ConfigProduct(BaseModel):
    __tablename__ = CONFIG_PRODUCT
    __table_args__ = (
        db.UniqueConstraint("config_product_code", "config_product_effective_date"),
    )

    config_product_id = db.Column(db.Integer, primary_key=True)
    config_product_code = db.Column(db.String(30), nullable=False)
    config_product_label = db.Column(db.String(100), nullable=False)
    config_product_effective_date = db.Column(db.Date, nullable=False)
    config_product_expiration_date = db.Column(
        db.Date, default=datetime.date(9999, 12, 31)
    )

    product_issue_date = db.Column(db.Date)
    master_product_code = db.Column(db.String(30))
    form_code = db.Column(db.String(30))

    age_rating_strategy_id = db.Column(
        db.ForeignKey(f"{REF_MASTER}.ref_id"),
        comment="Indicates whether age is used for rating, underwriting, or not at all. Allows for other strategies to be created.",
    )

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

    allow_employer_paid = db.Column(db.Boolean, default=False)
    voluntary_census_strategy_id = db.Column(
        db.ForeignKey(f"{REF_MASTER}.ref_id"),
        comment="Indicates a specific strategy for handling custom censuses for voluntary quotes",
    )
    employer_paid_census_strategy_id = db.Column(
        db.ForeignKey(f"{REF_MASTER}.ref_id"),
        comment="Indicates a specific strategy for handling custom censuses for employer paid quotes",
    )

    age_distribution_set = db.relationship(
        "Model_ConfigAgeDistributionSet",
        primaryjoin="Model_ConfigProduct.age_distribution_set_id == Model_ConfigAgeDistributionSet.config_age_distribution_set_id",
    )
    age_rating_strategy = db.relationship(
        "Model_RefRatingStrategy",
        primaryjoin="Model_ConfigProduct.age_rating_strategy_id == Model_RefRatingStrategy.ref_id",
    )

    rating_mapper_collection1 = db.relationship(
        "Model_ConfigRatingMapperCollection",
        primaryjoin="Model_ConfigProduct.rating_mapper_collection_id1 == Model_ConfigRatingMapperCollection.config_rating_mapper_collection_id",
    )
    rating_mapper_collection2 = db.relationship(
        "Model_ConfigRatingMapperCollection",
        primaryjoin="Model_ConfigProduct.rating_mapper_collection_id2 == Model_ConfigRatingMapperCollection.config_rating_mapper_collection_id",
    )
    rating_mapper_collection3 = db.relationship(
        "Model_ConfigRatingMapperCollection",
        primaryjoin="Model_ConfigProduct.rating_mapper_collection_id3 == Model_ConfigRatingMapperCollection.config_rating_mapper_collection_id",
    )
    rating_mapper_collection4 = db.relationship(
        "Model_ConfigRatingMapperCollection",
        primaryjoin="Model_ConfigProduct.rating_mapper_collection_id4 == Model_ConfigRatingMapperCollection.config_rating_mapper_collection_id",
    )
    rating_mapper_collection5 = db.relationship(
        "Model_ConfigRatingMapperCollection",
        primaryjoin="Model_ConfigProduct.rating_mapper_collection_id5 == Model_ConfigRatingMapperCollection.config_rating_mapper_collection_id",
    )
    rating_mapper_collection6 = db.relationship(
        "Model_ConfigRatingMapperCollection",
        primaryjoin="Model_ConfigProduct.rating_mapper_collection_id6 == Model_ConfigRatingMapperCollection.config_rating_mapper_collection_id",
    )

    voluntary_census_strategy = db.relationship(
        "Model_RefCensusStrategy",
        primaryjoin="Model_ConfigProduct.voluntary_census_strategy_id == Model_RefCensusStrategy.ref_id",
    )
    employer_paid_census_strategy = db.relationship(
        "Model_RefCensusStrategy",
        primaryjoin="Model_ConfigProduct.employer_paid_census_strategy_id == Model_RefCensusStrategy.ref_id",
    )

    states = db.relationship("Model_ConfigProductState")
    config_rate_groups = db.relationship("Model_ConfigRateGroup")
