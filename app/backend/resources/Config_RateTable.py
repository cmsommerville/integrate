import pandas as pd
from app.extensions import db
from app.shared import BaseCRUDResource, BaseCRUDResourceList
from ..classes.RateTableCohorts import RateTableCohorts
from ..models import (
    Model_ConfigAgeDistribution,
    Model_ConfigRateTable,
    Model_ConfigProduct,
    Model_ConfigRatingMapperDetail,
    Model_ConfigRatingMapperSet,
)
from ..schemas import Schema_ConfigRateTable
from ..schemas.Config_RateTable import DFSchema_RateTableCohorts


class CRUD_ConfigRateTable(BaseCRUDResource):
    model = Model_ConfigRateTable
    schema = Schema_ConfigRateTable()


class CRUD_ConfigRateTable_List(BaseCRUDResourceList):
    model = Model_ConfigRateTable
    schema = Schema_ConfigRateTable(many=True)


class RateTableCohortsResource(BaseCRUDResource):
    @classmethod
    def retrieve(cls, *args, **kwargs):
        product_id = kwargs.get("product_id")
        df_cohorts = RateTableCohorts.create_cohorts(product_id)
        if isinstance(df_cohorts, pd.DataFrame):
            return df_cohorts.to_dict("records")

        return []
