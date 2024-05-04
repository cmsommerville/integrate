from app.extensions import db
from app.shared import BaseModel
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy import or_

from ..tables import TBL_NAMES
from .Config_BenefitDurationDetail import (
    Model_ConfigBenefitDurationDetail,
    Model_ConfigBenefitDurationDetailAuth_ACL,
)

CONFIG_BENEFIT = TBL_NAMES["CONFIG_BENEFIT"]
CONFIG_BENEFIT_DURATION_SET = TBL_NAMES["CONFIG_BENEFIT_DURATION_SET"]


class Model_ConfigBenefitDurationSet(BaseModel):
    __tablename__ = CONFIG_BENEFIT_DURATION_SET

    config_benefit_duration_set_id = db.Column(db.Integer, primary_key=True)
    config_benefit_id = db.Column(
        db.ForeignKey(
            f"{CONFIG_BENEFIT}.config_benefit_id",
            onupdate="CASCADE",
            ondelete="CASCADE",
        ),
        nullable=False,
    )
    config_benefit_duration_set_code = db.Column(db.String(30), nullable=False)
    config_benefit_duration_set_label = db.Column(db.String(100), nullable=False)
    default_config_benefit_duration_detail_id = db.Column(db.Integer, nullable=True)

    parent = db.relationship("Model_ConfigBenefit")
    _duration_items = db.relationship(
        "Model_ConfigBenefitDurationDetail", back_populates="parent"
    )
    default_item = db.relationship(
        "Model_ConfigBenefitDurationDetail",
        foreign_keys=[default_config_benefit_duration_detail_id],
        primaryjoin="Model_ConfigBenefitDurationSet.default_config_benefit_duration_detail_id == Model_ConfigBenefitDurationDetail.config_benefit_duration_detail_id",
    )

    @hybrid_property
    def duration_items(self):
        DD = Model_ConfigBenefitDurationDetail
        ACL = Model_ConfigBenefitDurationDetailAuth_ACL
        data = (
            db.session.query(DD)
            .filter(
                DD.config_benefit_duration_set_id
                == self.config_benefit_duration_set_id,
                or_(
                    DD.is_restricted == False,
                    db.session.query(ACL)
                    .filter(
                        ACL.config_benefit_duration_detail_id
                        == DD.config_benefit_duration_detail_id
                    )
                    .count()
                    > 0,
                ),
            )
            .all()
        )
        return data

    @duration_items.setter
    def duration_items(self, values):
        self._duration_items = values
