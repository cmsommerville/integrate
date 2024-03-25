from sqlalchemy import Table
from sqlalchemy.ext.hybrid import hybrid_property
from app.extensions import db
from app.shared import BaseReflectedModel
from .Config_RatingMapperDetail import Model_ConfigRatingMapperDetail


vw_config_product_default_rating_mapper_sets = Table(
    "vw_config_product_default_rating_mapper_sets",
    db.metadata,
    autoload_with=db.engine,
)


class Model_DefaultProductRatingMapperSet(BaseReflectedModel):
    __table__ = vw_config_product_default_rating_mapper_sets
    __mapper_args__ = {
        "primary_key": [
            vw_config_product_default_rating_mapper_sets.c.config_product_id,
            vw_config_product_default_rating_mapper_sets.c.selection_rating_mapper_set_type,
            vw_config_product_default_rating_mapper_sets.c.default_config_rating_mapper_set_id,
        ]
    }

    @hybrid_property
    def mapper_details(self):
        """
        This returns the rating mapper details for the default rating mapper set
        """
        DETAIL = Model_ConfigRatingMapperDetail
        return (
            db.session.query(DETAIL)
            .filter(
                DETAIL.config_rating_mapper_set_id
                == self.default_config_rating_mapper_set_id
            )
            .all()
        )

    @classmethod
    def find_by_parent(cls, parent_id: int, *args, **kwargs):
        return cls.query.filter_by(config_product_id=parent_id).all()
