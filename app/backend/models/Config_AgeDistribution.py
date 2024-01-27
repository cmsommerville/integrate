from app.extensions import db
from app.shared import BaseModel

from ..tables import TBL_NAMES

CONFIG_AGE_DISTRIBUTION = TBL_NAMES["CONFIG_AGE_DISTRIBUTION_DETAIL"]
CONFIG_AGE_DISTRIBUTION_SET = TBL_NAMES["CONFIG_AGE_DISTRIBUTION_SET"]


class Model_ConfigAgeDistribution(BaseModel):
    __tablename__ = CONFIG_AGE_DISTRIBUTION
    __table_args__ = (
        db.UniqueConstraint("config_age_distribution_set_id", "age_value"),
    )

    config_age_distribution_id = db.Column(db.Integer, primary_key=True)
    config_age_distribution_set_id = db.Column(
        db.ForeignKey(
            f"{CONFIG_AGE_DISTRIBUTION_SET}.config_age_distribution_set_id",
            onupdate="CASCADE",
            ondelete="CASCADE",
        )
    )
    age_value = db.Column(db.Integer, nullable=False)
    weight = db.Column(db.Numeric(12, 5), nullable=False)
