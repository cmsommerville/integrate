import pandas as pd
from dateutil.relativedelta import relativedelta
from flask import request
from sqlalchemy import column
from app.shared import BaseCRUDResource, BaseCRUDResourceList, upload_file, NoFileProvidedException
from ..models import Model_SelectionCensusSet, Model_SelectionPlan, \
    Model_ConfigAttributeDetail, Model_ConfigAttributeDistributionSet_Gender, \
    Model_ConfigAttributeDistributionSet_SmokerStatus
from ..schemas import Schema_SelectionCensusSet, Schema_ConfigAttributeDetail


class Census: 
    def __init__(self, plan_id: int, df_census: pd.DataFrame, *args, **kwargs):
        self.df_census = df_census.copy()
        self.plan_id = plan_id
        self.plan = Model_SelectionPlan.find_one(plan_id)
        self.product = self.plan.product 
        self.gender_attr_set = self.product.gender_attr_set
        self.smoker_status_attr_set = self.product.smoker_status_attr_set
        self.gender_list = self.gender_attr_set.attributes
        self.smoker_status_list = self.smoker_status_attr_set.attributes
        self.composite_gender = next(g for g in self.gender_list if g.is_composite_id)
        self.composite_smoker_status = next(s for s in self.smoker_status_list if s.is_composite_id)

        self.df_gender = pd.DataFrame([
            {
                'gender_code': row.config_attr_detail_code, 
                'gender_id': row.config_attr_detail_id, 
            }
            for row in self.gender_list
        ])

        self.df_smoker_status = pd.DataFrame([
            {
                'smoker_status_code': row.config_attr_detail_code, 
                'smoker_status_id': row.config_attr_detail_id, 
            }
            for row in self.smoker_status_list
        ])

    def _get_default_smoker_status_distribution(self) -> pd.DataFrame:
        """
        Return the default smoker status distribution with a `_dummy` column
        """
        return pd.DataFrame([
            {
                '_dummy': 1, 
                'smoker_status_id': dist.config_attr_detail_id, 
                '_weight_smoker_status': dist.weight, 
            }
            for dist in self.product.smoker_status_distribution_set.smoker_status_distribution
        ])

    def _get_default_gender_distribution(self) -> pd.DataFrame:
        """
        Return the default gender distribution with a `_dummy` column
        """
        return pd.DataFrame([
            {
                '_dummy': 1, 
                'gender_id': dist.config_attr_detail_id, 
                '_weight_gender': dist.weight, 
            }
            for dist in self.product.gender_distribution_set.gender_distribution
        ])

    def _get_default_age_distribution(self) -> pd.DataFrame:
        """
        Return the default age distribution with a `_dummy` column
        """
        return pd.DataFrame([
            {
                '_dummy': 1, 
                'age_value': dist.age_value, 
                '_weight_age': dist.weight, 
            }
            for dist in self.product.age_distribution_set.age_distribution
        ])



    def _process_file(self):
        """
        Read the file into a Pandas dataframe. Conform values to database IDs. Filter and aggregate data as needed.
        """
        # calculate age value
        if 'age_value' in self.df_census.columns:
            pass
        elif 'date_of_birth' in self.df_census.columns:
            self.df_census['age_value'] = (int(self.plan.plan_effective_date.strftime('%Y%m%d')) - 
                self.df_census['date_of_birth'].dt.strftime('%Y%m%d').astype(int)) // 10000
        else: 
            raise Exception("Please provide either an `age_value` column or `date_of_birth` column")

        # exclude prohibited issue ages
        min_issue_age = self.product.min_issue_age
        max_issue_age = self.product.max_issue_age
        self.df_census = self.df_census.query("age_value >= @min_issue_age & age_value <= @max_issue_age")

        # get gender attribute IDs
        self.df_census = self.df_census.merge(self.df_gender, how='left', on='gender_code')
        if self.df_census['gender_id'].isna().sum() > 0:
            raise Exception("Gender codes provided in census which are not configured for this product")
        
        # get smoker status attributee IDs
        self.df_census = self.df_census.merge(self.df_smoker_status, how='left', on='smoker_status_code')
        if self.df_census['smoker_status_id'].isna().sum() > 0:
            raise Exception("Smoker status codes provided in census which are not configured for this product")
        
        # add weight if not provided
        if 'weight' not in self.df_census.columns:
            self.df_census['weight'] = 1

        # aggregate census
        self.df_census = self.df_census.groupby(
            ['gender_id', 'smoker_status_id', 'age_value']
        ).agg({'weight': 'sum'})

        self.df_census['_dummy'] = 1

        return self.df_census
        

    def _handle_no_census(self) -> pd.DataFrame:
        """
        Handler for no census provided. Generate census from default distributions if composite assumptions are provided.
        """
        census_strategy = self.product.employer_paid_census_strategy if self.plan.is_employer_paid else self.product.voluntary_census_strategy

        if census_strategy.ref_attr_code.upper() == 'REQUIRED':
            raise Exception("A census is required for this product but was not provided. Please provide a census.")

        # get default smoker status distribution
        df_ss_dist = self._get_default_smoker_status_distribution()

        # get default gender distribution
        df_g_dist = self._get_default_gender_distribution()

        # get default age distribution
        df_age_dist = self._get_default_age_distribution()

        df_census = df_ss_dist.merge(df_g_dist, how='inner', on='_dummy')
        df_census = df_census.merge(df_age_dist, how='inner', on='_dummy')
        df_census['weight'] = df_census['_weight_age'] * df_census['_weight_ss'] * df_census['_weight_gender']

        self.df_census = df_census[['age_value', 'smoker_status_id', 'gender_id', 'weight']]
        return self.df_census


    def _handle_census_provided(self) -> pd.DataFrame: 
        """
        Handler for census provided. Use default gender/smoker status distributions if composite assumptions are provided in census.
        """

        self.df_census['_dummy'] = 1
        cols = self.df_census.columns
        # if census is missing smoker status, merge default SS distribution
        smoker_status_id_set = set(self.df_census['smoker_status_id'].tolist())
        if len(smoker_status_id_set) > 1: 
            pass
        if smoker_status_id_set[0] == self.composite_smoker_status.config_attr_detail_id:
            df_ss_dist = self._get_default_smoker_status_distribution()
            self.df_census = self.df_census.merge(df_ss_dist, how='inner', on='_dummy')
            self.df_census['weight'] = self.df_census['weight'] * self.df_census['_weight_smoker_status']
            self.df_census = self.df_census[cols]

        # if census is missing gender, merge default gender distribution
        gender_id_set = set(self.df_census['gender_id'].tolist())
        if len(gender_id_set) > 1: 
            pass
        if gender_id_set[0] == self.composite_gender.config_attr_detail_id:
            df_g_dist = self._get_default_gender_distribution()
            self.df_census = self.df_census.merge(df_g_dist, how='inner', on='_dummy')
            self.df_census['weight'] = self.df_census['weight'] * self.df_census['_weight_gender']
            self.df_census = self.df_census[cols]

        self.df_census = self.df_census.drop(columns=['_dummy'])

        return self.df_census


    def process(self):
        if len(self.df_census) == 0: 
            self._handle_no_census()

        self._process_file()
        self._handle_census_provided()

    def to_census_set_dict(self, *args, **kwargs): 
        return {
            'selection_plan_id': self.plan_id,
            'selection_census_description': kwargs.get('selection_census_description'), 
            'selection_census_filename': kwargs.get('selection_census_filename'), 
            'census_details': self.df_census.to_dict('records')
        }



class CRUD_SelectionCensusSet(BaseCRUDResource): 
    model = Model_SelectionCensusSet
    schema = Schema_SelectionCensusSet

    @classmethod
    def post(cls, id: int): 
        try: 
            df, filename = upload_file(request)
        except NoFileProvidedException:
            df = pd.DataFrame() 
            filename = None
        except Exception as e:
            return {'error': str(e)}, 400

        # init census instance and return a dictionary of the census set
        census = Census(id, df)
        census.process()
        dict_census_set = census.to_census_set_dict(selection_census_filename=filename)
        
        # validate census set and load model instance
        _schema_instance = cls.schema()
        dict_census_set = _schema_instance.dump(dict_census_set)
        model_instance = _schema_instance.load(dict_census_set)

        # save to database
        model_instance.save_to_db()

        return _schema_instance.dump(model_instance), 200

class CRUD_SelectionCensusSet_List(BaseCRUDResourceList): 
    model = Model_SelectionCensusSet
    schema = Schema_SelectionCensusSet