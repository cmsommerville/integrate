import pandas as pd
from app.extensions import db
from ..models import (
    Model_ConfigAgeDistribution,
    Model_ConfigProduct,
    Model_ConfigRatingMapperDetail,
    Model_ConfigRatingMapperSet,
)
from ..schemas.Config_RateTable import DFSchema_RateTableCohorts


class RateTableCohorts:
    @classmethod
    def get_rating_mappers(cls, rating_mapper_collections):
        """
        Query all of a product's rating mapper details
        """
        SET = Model_ConfigRatingMapperSet
        DETAIL = Model_ConfigRatingMapperDetail
        collections = [
            coll for coll in rating_mapper_collections.values() if coll is not None
        ]

        attributes = (
            db.session.query(SET, DETAIL)
            .filter(SET.config_rating_mapper_collection_id.in_(collections))
            .join(
                DETAIL,
                SET.config_rating_mapper_set_id == DETAIL.config_rating_mapper_set_id,
            )
            .with_entities(
                SET.config_rating_mapper_collection_id,
                SET.config_rating_mapper_set_id,
                DETAIL.rate_table_attribute_detail_id,
            )
            .distinct()
        )

        return pd.DataFrame(attributes)

    @classmethod
    def get_age_distribution(cls, age_distribution_set_id: int):
        """
        Query a product's age distribution
        """
        AGE = Model_ConfigAgeDistribution
        age_data = (
            db.session.query(AGE)
            .filter(AGE.config_age_distribution_set_id == age_distribution_set_id)
            .with_entities(
                AGE.config_age_distribution_set_id,
                AGE.config_age_distribution_id,
                AGE.rate_table_age_value,
            )
            .distinct()
        )
        return pd.DataFrame(age_data)

    @classmethod
    def cross_join_age_attrs(
        cls, rating_mapper_collection_dict, df_attributes, df_age_distribution
    ):
        """
        Create all rating cohorts. This is a cross join between the age distribution
        and all the rating mappers attached to a product.
        """
        df = df_age_distribution.copy()
        for coll_suffix, coll_id in rating_mapper_collection_dict.items():
            if coll_id is None:
                continue

            df_coll = df_attributes.query(
                "config_rating_mapper_collection_id == @coll_id"
            )[
                [
                    "config_rating_mapper_set_id",
                    "rate_table_attribute_detail_id",
                ]
            ].rename(
                columns={
                    "config_rating_mapper_set_id": f"config_rating_mapper_set_id{coll_suffix}",
                    "rate_table_attribute_detail_id": f"rate_table_attribute_detail_id{coll_suffix}",
                }
            )

            if df_coll.shape[0] == 0:
                continue

            df = df.merge(df_coll, how="cross")

        return df.pipe(DFSchema_RateTableCohorts)

    @classmethod
    def create_cohorts(cls, product_id: int, *args, **kwargs):
        product = Model_ConfigProduct.find_one(product_id)
        if not product:
            return None

        rating_mapper_collections = {
            "1": product.rating_mapper_collection_id1,
            "2": product.rating_mapper_collection_id2,
            "3": product.rating_mapper_collection_id3,
            "4": product.rating_mapper_collection_id4,
            "5": product.rating_mapper_collection_id5,
            "6": product.rating_mapper_collection_id6,
        }

        df_attributes = cls.get_rating_mappers(rating_mapper_collections)
        df_age_dist = cls.get_age_distribution(product.age_distribution_set_id)
        df = cls.cross_join_age_attrs(
            rating_mapper_collections, df_attributes, df_age_dist
        )

        return df
