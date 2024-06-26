from sqlalchemy import Table
from sqlalchemy.ext.hybrid import hybrid_property
from app.extensions import db
from .Config_RatingMapperDetail import Model_ConfigRatingMapperDetail


class Model_DefaultProductRatingMapperSet(db.Model):
    # __local_table__ = Table(
    #     "vw_config_product_default_rating_mapper_sets",
    #     db.metadata,
    #     autoload_with=db.engine,
    #     info={"skip_autogenerated": True},
    # )
    __tablename__ = "vw_config_product_default_rating_mapper_sets"
    __table_args__ = ({"info": {"skip_autogenerated": True}},)
    __mapper_args__ = {
        "primary_key": [
            "config_product_id",
            "selection_rating_mapper_set_type",
            "default_config_rating_mapper_set_id",
        ]
    }

    config_product_id = db.Column(db.Integer, nullable=False)
    config_rating_mapper_collection_id = db.Column(db.Integer, nullable=False)
    selection_rating_mapper_set_type = db.Column(db.String(50), nullable=False)
    default_config_rating_mapper_set_id = db.Column(db.Integer, nullable=False)

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
